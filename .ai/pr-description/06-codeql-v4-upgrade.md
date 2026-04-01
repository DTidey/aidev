## Summary
- Upgrade the CodeQL GitHub Action references from `v3` to `v4`.
- Update the repository guardrail test so the CodeQL Dependabot bump no longer fails on an outdated pinned assertion.
- Keep the change narrowly scoped to the workflow, tests, and matching packet artifacts.

## Spec
- Spec: `docs/specs/06-codeql-v4-upgrade.md`
- Test plan: `docs/test-plans/06-codeql-v4-upgrade.md`
- PR draft path: `.ai/pr-description/06-codeql-v4-upgrade.md`

## Acceptance criteria
- [x] AC1: `.github/workflows/codeql.yml` uses `github/codeql-action` `v4` for the `init`, `autobuild`, and `analyze` steps while preserving the existing triggers, permissions, and `language: [python, actions]` matrix.
- [x] AC2: `tests/test_security_workflow_docs.py` verifies the CodeQL workflow expects the upgraded `v4` action reference so the repository no longer fails on this Dependabot update.
- [x] AC3: Matching packet artifacts exist at `docs/test-plans/06-codeql-v4-upgrade.md` and `.ai/pr-description/06-codeql-v4-upgrade.md`, and validation runs document `make lint`, `make test`, and `make security`.

## Security review
- [x] Security considerations were reviewed and updated in the linked spec
- [ ] No meaningful security impact
- [ ] Auth/authz behavior changed
- [ ] Secrets or credential handling changed
- [x] Input validation, data exposure, file access, network access, or dependencies changed
- Reviewer focus:
  - Confirm the CodeQL workflow keeps the same job/check shape while moving all three CodeQL action references to `v4`.

## Testing
- [x] `make lint`
- [x] `make test`
- [x] `make security`
- Additional commands:
  - `pytest -q tests/test_security_workflow_docs.py::test_github_guardrails_files_exist_and_match_documented_checks`

## GitHub checks
- Required checks for `main`:
  - `CI / test`
  - `CodeQL / analyze`

## Changelog
- [ ] Add to `CHANGELOG.md` `Unreleased` if this maintenance change should be called out before the next explicit release.

## Notes / tradeoffs
- Keeping an explicit `v4` pin preserves a clear guardrail while letting the final CodeQL Dependabot upgrade merge cleanly.
