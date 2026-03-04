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
    spec_touched = any(path.startswith("docs/specs/") and path.endswith(".md") for path in files)

    errors: list[str] = []
    if not body.strip():
        errors.append("PR body is empty. Fill in the PR template.")
    if require_spec and not spec_touched:
        errors.append("Code changes detected without a spec update/addition under docs/specs/*.md.")
    if require_spec and not has_spec_link(body):
        errors.append("PR body must include a spec link like docs/specs/<slug>.md.")
    if require_spec and not has_checked_ac(body):
        errors.append("At least one acceptance criterion checkbox must be checked (e.g., [x] AC1).")
    if require_spec and has_spec_link(body):
        linked_spec = extract_spec_link(body)
        assert linked_spec is not None
        if not Path(linked_spec).is_file():
            errors.append(f"Linked spec file not found: {linked_spec}")
        else:
            valid_acs = spec_ac_ids(linked_spec)
            selected_acs = checked_ac_ids(body)
            unknown_acs = sorted(selected_acs - valid_acs)
            if unknown_acs:
                unknown_acs_text = ", ".join(unknown_acs)
                errors.append(
                    f"Checked acceptance criteria not found in {linked_spec}: {unknown_acs_text}"
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
