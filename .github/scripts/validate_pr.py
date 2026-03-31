#!/usr/bin/env python3
"""Validate PR process requirements for the multi-agent workflow."""

from __future__ import annotations

import json
import os
import re
import subprocess  # nosec B404
import sys
from pathlib import Path

NON_CODE_ROOT_FILES = {
    "README.md",
    "requirements.in",
    "requirements-dev.in",
    "requirements.txt",
    "requirements-dev.txt",
    "pyproject.toml",
    "Makefile",
    ".pre-commit-config.yaml",
}
NON_CODE_TEXT_EXTENSIONS = {".md", ".rst", ".txt"}
SPEC_LINK_PATTERN = re.compile(r"docs/specs/\d{2}-[a-z0-9][a-z0-9-]*\.md", flags=re.IGNORECASE)
CHECKED_AC_PATTERN = re.compile(r"^- \[[xX]\]\s+(AC\d+)\b", flags=re.MULTILINE)
SPEC_AC_PATTERN = re.compile(r"^\s*-\s*(AC\d+):", flags=re.MULTILINE)
NUMBERED_PACKET_PATTERN = re.compile(r"^\d{2}-[a-z0-9][a-z0-9-]*\.md$", flags=re.IGNORECASE)


def run(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, text=True).strip()  # nosec B603


def changed_files(base: str, head: str) -> list[str]:
    out = run(["git", "diff", "--name-only", f"{base}...{head}"])
    if not out:
        return []
    return [line.strip() for line in out.splitlines() if line.strip()]


def is_non_code_path(path: str) -> bool:
    if path in NON_CODE_ROOT_FILES:
        return True

    suffix = Path(path).suffix.lower()
    if suffix in NON_CODE_TEXT_EXTENSIONS and path.startswith(("docs/", ".ai/", ".github/")):
        return True

    return False


def is_docs_only(files: list[str]) -> bool:
    if not files:
        return True
    for path in files:
        if is_non_code_path(path):
            continue
        return False
    return True


def has_spec_link(body: str) -> bool:
    return bool(SPEC_LINK_PATTERN.search(body))


def extract_spec_link(body: str) -> str | None:
    match = SPEC_LINK_PATTERN.search(body)
    if not match:
        return None
    return match.group(0)


def has_checked_ac(body: str) -> bool:
    return bool(CHECKED_AC_PATTERN.search(body))


def checked_ac_ids(body: str) -> set[str]:
    return {ac_id.upper() for ac_id in CHECKED_AC_PATTERN.findall(body)}


def spec_ac_ids(spec_path: str) -> set[str]:
    content = Path(spec_path).read_text(encoding="utf-8")
    return {ac_id.upper() for ac_id in SPEC_AC_PATTERN.findall(content)}


def changed_specs(files: list[str]) -> set[str]:
    return {
        path
        for path in files
        if path.startswith("docs/specs/")
        and path.endswith(".md")
        and path != "docs/specs/README.md"
    }


def has_numbered_packet_name(path: str) -> bool:
    return bool(NUMBERED_PACKET_PATTERN.match(Path(path).name))


def test_plan_path_for_spec(spec_path: str) -> str:
    return spec_path.replace("docs/specs/", "docs/test-plans/", 1)


def pr_draft_path_for_spec(spec_path: str) -> str:
    return spec_path.replace("docs/specs/", ".ai/pr-description/", 1)


def artifact_has_spec_link(path: str, spec_path: str) -> bool:
    content = Path(path).read_text(encoding="utf-8")
    return spec_path in content


def artifact_checked_ac_ids(path: str) -> set[str]:
    content = Path(path).read_text(encoding="utf-8")
    return checked_ac_ids(content)


def main() -> int:
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path:
        print("GITHUB_EVENT_PATH is not set.")
        return 1

    payload = json.loads(Path(event_path).read_text(encoding="utf-8"))
    pull_request = payload.get("pull_request")
    if not pull_request:
        print("No pull_request payload found; skipping PR validation.")
        return 0

    body = pull_request.get("body") or ""
    base_sha = pull_request["base"]["sha"]
    head_sha = pull_request["head"]["sha"]

    files = changed_files(base_sha, head_sha)
    require_spec = not is_docs_only(files)
    touched_specs = changed_specs(files)

    errors: list[str] = []
    if not body.strip():
        errors.append("PR body is empty. Fill in the PR template.")
    if require_spec and not touched_specs:
        errors.append("Code changes detected without a spec update/addition under docs/specs/*.md.")
    invalid_spec_paths = sorted(
        path for path in touched_specs if not has_numbered_packet_name(path)
    )
    if invalid_spec_paths:
        errors.append(
            "Spec files must use a two-digit prefix like docs/specs/03-my-change.md: "
            + ", ".join(invalid_spec_paths)
        )
    if require_spec and not has_spec_link(body):
        errors.append("PR body must include a spec link like docs/specs/03-my-change.md.")
    if require_spec and has_spec_link(body):
        linked_spec = extract_spec_link(body)
        if linked_spec is None:
            errors.append("PR body must include a valid spec link like docs/specs/03-my-change.md.")
            linked_spec = ""
        if not Path(linked_spec).is_file():
            errors.append(f"Linked spec file not found: {linked_spec}")
        else:
            if linked_spec not in touched_specs:
                errors.append(
                    "Linked spec must be added or updated in the PR when code changes are present: "
                    f"{linked_spec}"
                )
            valid_acs = spec_ac_ids(linked_spec)
            selected_acs = checked_ac_ids(body)
            missing_acs = sorted(valid_acs - selected_acs)
            unknown_acs = sorted(selected_acs - valid_acs)
            if missing_acs:
                missing_acs_text = ", ".join(missing_acs)
                errors.append(
                    f"PR body must check every acceptance criterion from {linked_spec}: "
                    f"{missing_acs_text}"
                )
            if unknown_acs:
                unknown_acs_text = ", ".join(unknown_acs)
                errors.append(
                    f"Checked acceptance criteria not found in {linked_spec}: {unknown_acs_text}"
                )
            test_plan_path = test_plan_path_for_spec(linked_spec)
            if not Path(test_plan_path).is_file():
                errors.append(f"Expected test plan file not found: {test_plan_path}")
            elif not has_numbered_packet_name(test_plan_path):
                errors.append(
                    "Matching test plans must use a two-digit prefix like "
                    "docs/test-plans/03-my-change.md: "
                    f"{test_plan_path}"
                )
            elif test_plan_path not in files:
                errors.append(
                    "Code-changing PRs must add or update the matching test plan file: "
                    f"{test_plan_path}"
                )
            pr_draft_path = pr_draft_path_for_spec(linked_spec)
            if not Path(pr_draft_path).is_file():
                errors.append(f"Expected PR draft file not found: {pr_draft_path}")
            elif not has_numbered_packet_name(pr_draft_path):
                errors.append(
                    "Matching PR drafts must use a two-digit prefix like "
                    ".ai/pr-description/03-my-change.md: "
                    f"{pr_draft_path}"
                )
            else:
                if pr_draft_path not in files:
                    errors.append(
                        "Code-changing PRs must add or update the matching PR draft file: "
                        f"{pr_draft_path}"
                    )
                if not artifact_has_spec_link(pr_draft_path, linked_spec):
                    errors.append(
                        f"PR draft must link the same spec as the PR body: {pr_draft_path}"
                    )
                draft_selected_acs = artifact_checked_ac_ids(pr_draft_path)
                draft_missing_acs = sorted(valid_acs - draft_selected_acs)
                draft_unknown_acs = sorted(draft_selected_acs - valid_acs)
                if draft_missing_acs:
                    draft_missing_acs_text = ", ".join(draft_missing_acs)
                    errors.append(
                        f"PR draft must check every acceptance criterion from {linked_spec}: "
                        f"{draft_missing_acs_text}"
                    )
                if draft_unknown_acs:
                    draft_unknown_acs_text = ", ".join(draft_unknown_acs)
                    errors.append(
                        f"Checked acceptance criteria not found in {linked_spec} "
                        f"within PR draft {pr_draft_path}: {draft_unknown_acs_text}"
                    )

    if errors:
        print("PR validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    print("PR validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
