# Test Plan: codeql-v4-upgrade

Path: `docs/test-plans/06-codeql-v4-upgrade.md`

## What changed
- Upgraded the CodeQL workflow action references from `v3` to `v4`.
- Updated the GitHub-guardrail test so it expects the new CodeQL action version.
- Added the matching spec/PR packet files for this maintenance change.

## Acceptance criteria coverage
- AC1: Verify `.github/workflows/codeql.yml` keeps `language: [python, actions]` and uses `github/codeql-action/{init,autobuild,analyze}@v4`.
- AC2: Verify `tests/test_security_workflow_docs.py` checks for the `v4` CodeQL action reference, then run `pytest -q tests/test_security_workflow_docs.py::test_github_guardrails_files_exist_and_match_documented_checks`.
- AC3: Run `make lint`, `make test`, and `make security`.

## Edge cases
- From spec:
  - All three CodeQL action steps should move to `v4`, not just `init`.
  - The workflow must keep the `python` and `actions` language matrix after the upgrade.
  - The required GitHub check name should remain `CodeQL / analyze`.
- Additional adversarial cases:
  - The workflow upgrades one CodeQL step but leaves another on `v3`.
  - The test still pins `v3` and blocks the Dependabot workflow bump.
  - The workflow upgrade accidentally changes triggers or permissions unrelated to the version update.

## Notes
- Flaky risks: None expected from the structural assertions; `make security` can vary slightly with vulnerability database freshness.
- Determinism considerations: The focused pytest target should provide a fast deterministic signal before the full `make` validation suite.
