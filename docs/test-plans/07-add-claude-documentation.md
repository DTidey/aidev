# Test Plan: add-claude-documentation

Path: `docs/test-plans/07-add-claude-documentation.md`

## What changed
- Added `CLAUDE.md` at the repository root documenting development commands, numbered packet system, five-role workflow, CI enforcement rules, and blocking/handoff format.

## Acceptance criteria coverage
- AC1: `test_claude_md_exists_and_has_prefix` — asserts file exists at repo root and first line matches required heading.
- AC2: `test_claude_md_has_all_make_targets` — asserts all eight `make` targets and the single-test pattern appear in the file.
- AC3: `test_claude_md_describes_packet_system` — asserts the three artifact path patterns and the current highest prefix (`06`) are mentioned.
- AC4: `test_claude_md_describes_five_roles` — asserts all five role names appear in the file.
- AC5: `test_claude_md_documents_ci_and_handoff` — asserts `validate_pr.py` is referenced and the `Blocked on:` / `Affected AC:` handoff keywords are present.

## Edge cases
- From spec:
  - File must not be empty.
  - Content must not contradict `AGENTS.md`.
- Additional adversarial cases:
  - File exists but is missing the required Claude Code prefix — should fail AC1.
  - A `make` target is present in `Makefile` but absent from `CLAUDE.md` — should fail AC2.
  - Highest spec prefix in `CLAUDE.md` is stale (understates the current maximum) — noted as a maintenance risk; not a hard test failure but documented.

## Notes
- Flaky risks: None — all assertions are static file content checks.
- Determinism considerations: Tests read from the filesystem; deterministic as long as the file is present.
