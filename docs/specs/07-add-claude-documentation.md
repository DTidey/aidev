# Add CLAUDE.md for Claude Code

**Spec file:** `docs/specs/07-add-claude-documentation.md`
**Spec slug:** add-claude-documentation
**Status:** Done
**Owner:** DTidey
**Date:** 2026-04-16

## Problem statement
- Claude Code instances working in this repository lack a `CLAUDE.md` file, so each session must rediscover commands, workflow rules, and architecture by reading multiple files.
- A `CLAUDE.md` at the repository root is automatically loaded by Claude Code on every session, reducing ramp-up time and preventing workflow violations.

## Scope
In scope:
- Create `CLAUDE.md` at the repository root with development commands, architecture overview, workflow rules, and CI constraints.

Out of scope / non-goals:
- Changes to any workflow scripts, CI configuration, or role definitions.
- Adding new workflow rules not already present in `AGENTS.md`, `README.md`, or `.ai/roles/`.

## Assumptions
- `CLAUDE.md` is treated as a code-changing file by `validate_pr.py` because it is not in `NON_CODE_ROOT_FILES` and does not live under `docs/`, `.ai/`, or `.github/`.
- Content should faithfully reflect existing documentation; no new conventions are introduced.

## Proposed behavior / API
### Public interface
- File: `CLAUDE.md` (repository root)

### Inputs / outputs
- Inputs: none (static documentation file)
- Outputs: `CLAUDE.md` readable by Claude Code on session start
- Error handling: N/A

### Examples
N/A — documentation file only.

## Acceptance criteria
- AC1: `CLAUDE.md` exists at the repository root and begins with the required Claude Code prefix heading.
- AC2: `CLAUDE.md` documents all `make` targets: `venv`, `compile`, `sync`, `lint`, `test`, `security`, `precommit`, and the single-test invocation pattern.
- AC3: `CLAUDE.md` describes the numbered packet system, including the three artifact paths and the current highest prefix.
- AC4: `CLAUDE.md` describes the five-role workflow (Spec Writer, Orchestrator, Implementer, Tester, Reviewer) with each role's key constraint or output.
- AC5: `CLAUDE.md` documents the CI enforcement rules (what `validate_pr.py` checks) and the exact blocking/handoff format for all roles.

## Security considerations
- Auth/authz impact: None.
- Input handling or injection risk: None — static documentation, not executed.
- Secrets or credential handling: None.
- Data exposure or privacy impact: None.
- File system access impact: Adds a single read-only markdown file at the repo root.
- Network or external service impact: None.
- Dependency or supply-chain impact: None.
- Security notes for reviewers/testers: No meaningful security impact.

## Edge cases
- `CLAUDE.md` must not duplicate or contradict `AGENTS.md`; content must be consistent with existing docs.
- The next available prefix noted in `CLAUDE.md` must stay accurate as new specs are added.

## Test guidance
- AC1 -> `test_claude_md_exists_and_has_prefix`
- AC2 -> `test_claude_md_has_all_make_targets`
- AC3 -> `test_claude_md_describes_packet_system`
- AC4 -> `test_claude_md_describes_five_roles`
- AC5 -> `test_claude_md_documents_ci_and_handoff`

## Decision log
- 2026-04-16: `CLAUDE.md` placed at root (not under `docs/`) so Claude Code auto-loads it on session start.
