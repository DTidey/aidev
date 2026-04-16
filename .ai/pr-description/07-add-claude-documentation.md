## Summary
- Adds `CLAUDE.md` at the repository root so Claude Code auto-loads workflow context on every session.
- Documents all `make` targets, the numbered packet system, five-role workflow, CI enforcement rules, and blocking/handoff format.
- Content is derived entirely from existing `AGENTS.md`, `README.md`, and `.ai/roles/` — no new conventions introduced.

## Spec
- Spec: `docs/specs/07-add-claude-documentation.md`
- Test plan: `docs/test-plans/07-add-claude-documentation.md`
- PR draft path: `.ai/pr-description/07-add-claude-documentation.md`

## Acceptance Criteria
- [x] AC1: `CLAUDE.md` exists at the repository root and begins with the required Claude Code prefix heading.
- [x] AC2: `CLAUDE.md` documents all `make` targets: `venv`, `compile`, `sync`, `lint`, `test`, `security`, `precommit`, and the single-test invocation pattern.
- [x] AC3: `CLAUDE.md` describes the numbered packet system, including the three artifact paths and the current highest prefix.
- [x] AC4: `CLAUDE.md` describes the five-role workflow (Spec Writer, Orchestrator, Implementer, Tester, Reviewer) with each role's key constraint or output.
- [x] AC5: `CLAUDE.md` documents the CI enforcement rules (what `validate_pr.py` checks) and the exact blocking/handoff format for all roles.

## Security Review
- [x] Security considerations were reviewed and updated in the linked spec
- [x] No meaningful security impact
- Reviewer focus: Static documentation file only — no code execution, no secrets, no network access.

## Validation
- [x] `make lint`
- [x] `make test`
- [x] `make security`

## GitHub Checks
- Required checks for `main`:
  - `CI / test`
  - `CodeQL / analyze`

## Changelog
- [x] Add to `CHANGELOG.md` under `## Unreleased` if this change should be called out before the next explicit release.

## Open Risks
- The "current highest prefix" noted in `CLAUDE.md` will become stale as new specs are added; it should be updated when the next packet is created.
