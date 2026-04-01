# Test Plan: dependabot-pr-validation-exception

Path: `docs/test-plans/04-dependabot-pr-validation-exception.md`

## What changed
- Added a narrow validator exception for Dependabot PRs that only update dependency manifests or GitHub workflow files.
- Added tests to keep that exemption from expanding to normal source-code changes.
- Updated CI to create and use the repository virtualenv before invoking Makefile-based validation commands.
- Added a narrowly scoped auto-approval workflow for owner-authored `codex/` maintenance PRs.

## Acceptance criteria coverage
- AC1: Verify the validator accepts file lists containing only allowed dependency and workflow paths.
- AC2: Verify the validator rejects file lists that include application code paths.
- AC3: Verify the validator tests keep the Dependabot allowlist narrow.
- AC4: Verify `.github/workflows/ci.yml` creates `.venv` and runs `make lint`, `make security`, and `make test`.
- AC5: Verify `.github/workflows/auto-approve-own-prs.yml` only targets owner-authored `codex/` PRs to `main` and uses GitHub CLI approval with pull-request write permission.

## Edge cases
- From spec:
  - Dependabot PRs that mix allowed dependency files with application code must not bypass validation.
  - Workflow-only Dependabot PRs should still be accepted.
  - Empty file lists should not qualify for the bypass.
  - CI must create `.venv` before calling Makefile targets that activate it.
  - Auto-approval must not match arbitrary owner PR branches.
- Additional adversarial cases:
  - A future change accidentally allows `.github/scripts/` or `backend/` files.
  - A future change allows any bot PR rather than only `dependabot[bot]`.
  - A future change treats an empty diff as safe and skips validation.

## Notes
- Flaky risks: None expected; the tests are pure unit tests.
- Determinism considerations: Keep the bypass logic covered with direct file-path assertions rather than end-to-end GitHub event fixtures.
