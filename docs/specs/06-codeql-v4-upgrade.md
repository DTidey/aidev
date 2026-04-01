# CodeQL v4 Upgrade

**Spec file:** `docs/specs/06-codeql-v4-upgrade.md`
**Spec slug:** codeql-v4-upgrade
**Status:** Done
**Owner:** Codex
**Date:** 2026-04-01

## Problem statement
- A Dependabot update to `github/codeql-action` from `v3` to `v4` is blocked by a repository test that still hard-codes the older action major version.
- The repository should be able to adopt the current CodeQL action major without breaking its own guardrail assertions.
- Without updating the pinned workflow and tests together, routine security-maintenance PRs stay noisy and harder to merge.

## Scope
In scope:
- Upgrade the CodeQL workflow actions from `v3` to `v4`.
- Update the guardrail test so it expects the new CodeQL action major version.
- Add the matching test-plan and PR-description packet files for this change.

Out of scope / non-goals:
- Changing the workflow trigger, scanned languages, or required check names.
- Reworking the broader GitHub-enforcement or Dependabot auto-management behavior.
- Creating a release or updating `CHANGELOG.md`.

## Assumptions
- The next available packet prefix is `06`.
- `github/codeql-action@v4` is the intended current major version for this repository.
- The GitHub status check name exposed by the workflow remains `CodeQL / analyze`.

## Proposed behavior / API
### Public interface
- Functions/classes/modules affected:
  - `.github/workflows/codeql.yml`
  - `tests/test_security_workflow_docs.py`
  - `docs/specs/06-codeql-v4-upgrade.md`
  - `docs/test-plans/06-codeql-v4-upgrade.md`
  - `.ai/pr-description/06-codeql-v4-upgrade.md`

### Inputs / outputs
- Inputs:
  - Pull requests or pushes that trigger the CodeQL workflow
  - Repository tests that pin the expected CodeQL workflow contents
- Outputs:
  - The CodeQL workflow uses `github/codeql-action` `v4` for `init`, `autobuild`, and `analyze`
  - The repository test suite accepts the upgraded workflow version
- Error handling:
  - If the workflow drifts away from the expected CodeQL action major, the guardrail test fails visibly
  - If the upgrade changes required check names, existing documentation and tests should catch that mismatch separately

### Examples
```yaml
- name: Initialize CodeQL
  uses: github/codeql-action/init@v4
```

## Acceptance criteria
- AC1: `.github/workflows/codeql.yml` uses `github/codeql-action` `v4` for the `init`, `autobuild`, and `analyze` steps while preserving the existing triggers, permissions, and `language: [python, actions]` matrix.
- AC2: `tests/test_security_workflow_docs.py` verifies the CodeQL workflow expects the upgraded `v4` action reference so the repository no longer fails on this Dependabot update.
- AC3: Matching packet artifacts exist at `docs/test-plans/06-codeql-v4-upgrade.md` and `.ai/pr-description/06-codeql-v4-upgrade.md`, and validation runs document `make lint`, `make test`, and `make security`.

## Security considerations
- Auth/authz impact: No repository permission changes beyond the existing CodeQL workflow permissions.
- Input handling or injection risk: Low; the change only updates pinned GitHub Action major versions and the matching structural test.
- Secrets or credential handling: No new secrets or tokens are introduced.
- Data exposure or privacy impact: No change; CodeQL continues to analyze repository contents in GitHub Actions.
- File system access impact: No local file access change beyond the existing workflow checkout and analysis behavior.
- Network or external service impact: Continues using GitHub-hosted CodeQL actions, now on `v4`.
- Dependency or supply-chain impact: Positive; the repository adopts the newer maintained major of a security-scanning action.
- Security notes for reviewers/testers: Confirm the upgrade keeps the workflow job shape and required status check name stable while allowing the Dependabot action bump to pass.

## Edge cases
- Updating only `init` without updating `autobuild` and `analyze` would leave the workflow inconsistent.
- The workflow should keep scanning both Python and GitHub Actions content after the version bump.
- Tests should keep pinning the intended major version so unexpected drift still fails clearly.

## Test guidance
- AC1 -> Content test verifies `language: [python, actions]` and `github/codeql-action/{init,autobuild,analyze}@v4` in `.github/workflows/codeql.yml`
- AC2 -> Run `pytest -q tests/test_security_workflow_docs.py::test_github_guardrails_files_exist_and_match_documented_checks`
- AC3 -> Run `make lint`, `make test`, and `make security`

## Decision log
- 2026-04-01: Chose a direct `v4` upgrade instead of loosening the test to multiple majors so the repository continues to pin an explicit expected CodeQL action version.
