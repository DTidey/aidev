#!/usr/bin/env python3
"""Validate PR process requirements for the multi-agent workflow."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, text=True).strip()


def changed_files(base: str, head: str) -> list[str]:
    out = run(["git", "diff", "--name-only", f"{base}...{head}"])
    if not out:
        return []
    return [line.strip() for line in out.splitlines() if line.strip()]


def is_docs_only(files: list[str]) -> bool:
    if not files:
        return True
    non_code_prefixes = ("docs/", ".ai/", ".github/")
    non_code_files = {
        "README.md",
        "requirements.in",
        "requirements-dev.in",
        "requirements.txt",
        "requirements-dev.txt",
        "pyproject.toml",
        "Makefile",
        ".pre-commit-config.yaml",
    }
    for path in files:
        if path.startswith(non_code_prefixes):
            continue
        if path in non_code_files:
            continue
        return False
    return True


def has_spec_link(body: str) -> bool:
    return bool(re.search(r"docs/specs/[a-z0-9][a-z0-9-]*\.md", body, flags=re.IGNORECASE))


def has_checked_ac(body: str) -> bool:
    return bool(re.search(r"^- \[[xX]\]\s+AC\d+\b", body, flags=re.MULTILINE))


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

    if errors:
        print("PR validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    print("PR validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
