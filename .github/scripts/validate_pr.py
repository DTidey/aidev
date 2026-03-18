#!/usr/bin/env python3
"""Validate PR process requirements for the multi-agent workflow."""

from __future__ import annotations

import json
import os
import re
import subprocess
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
SPEC_LINK_PATTERN = re.compile(r"docs/specs/[a-z0-9][a-z0-9-]*\.md", flags=re.IGNORECASE)
CHECKED_AC_PATTERN = re.compile(r"^- \[[xX]\]\s+(AC\d+)\b", flags=re.MULTILINE)
SPEC_AC_PATTERN = re.compile(r"^\s*-\s*(AC\d+):", flags=re.MULTILINE)


def run(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, text=True).strip()


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


def test_plan_path_for_spec(spec_path: str) -> str:
    return spec_path.replace("docs/specs/", "docs/test-plans/", 1)


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
    if require_spec and not has_spec_link(body):
        errors.append("PR body must include a spec link like docs/specs/<slug>.md.")
    if require_spec and has_spec_link(body):
        linked_spec = extract_spec_link(body)
        assert linked_spec is not None
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
            elif test_plan_path not in files:
                errors.append(
                    "Code-changing PRs must add or update the matching test plan file: "
                    f"{test_plan_path}"
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
