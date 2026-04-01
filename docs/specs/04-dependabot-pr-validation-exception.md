# Dependabot PR Validation Exception

**Spec file:** `docs/specs/04-dependabot-pr-validation-exception.md`
**Spec slug:** dependabot-pr-validation-exception
**Status:** Done
**Owner:** Codex
**Date:** 2026-04-01

## Problem statement
- The PR validator currently requires a spec, matching test plan, and PR draft for every code-changing pull request.
- Dependabot pull requests in `aidev` update dependency or workflow files automatically and do not provide spec packets or custom PR bodies.
- This causes valid dependency-maintenance pull requests to fail the validator before reviewers can evaluate the actual dependency change.
- The current CI workflow also installs Python tooling globally on the runner while `make lint`, `make test`, and `make security` expect a repository-local `.venv`, which breaks the `Security` step in GitHub Actions.
- Repository rules also prevent pull request authors from approving their own pull requests, which blocks solo maintenance updates unless the repository provides a narrowly scoped automation path for owner-authored maintenance branches.

## Scope
In scope:
- Allow Dependabot-authored pull requests to bypass spec validation when they only modify dependency manifest files or GitHub workflow files.
- Add tests that pin the allowed-file behavior so the exception stays narrow.
- Align the CI workflow with the Makefile-driven virtualenv flow so GitHub Actions creates `.venv` before invoking Make targets.
- Add a tightly scoped workflow that auto-approves owner-authored maintenance PRs from `codex/` branches so solo repository maintenance remains possible without weakening the general review rules.

Out of scope / non-goals:
- Relaxing validation for human-authored pull requests.
- Allowing Dependabot pull requests that modify application source files to bypass the spec workflow.
- Changing branch protection, CodeQL, or Dependabot configuration.
- Broadly auto-approving all owner pull requests.

## Assumptions
- Dependabot pull requests are authored as `dependabot[bot]`.
- The intended no-spec exception should cover root dependency files and `.github/workflows/*.yml` or `.yaml`.
- The next available packet prefix is `04`.

## Proposed behavior / API
### Public interface
- Files/modules affected:
  - `docs/specs/04-dependabot-pr-validation-exception.md`
  - `docs/test-plans/04-dependabot-pr-validation-exception.md`
  - `.ai/pr-description/04-dependabot-pr-validation-exception.md`
  - `.github/scripts/validate_pr.py`
  - `.github/workflows/ci.yml`
  - `.github/workflows/auto-approve-own-prs.yml`
  - `tests/test_validate_pr.py`
  - `tests/test_security_workflow_docs.py`

### Inputs / outputs
- Inputs:
  - PR author login from the GitHub pull request payload
  - Changed file paths between the PR base and head commits
- Outputs:
  - Dependabot dependency-only PRs skip spec validation successfully
  - All other PRs continue through the existing spec-validation rules
  - CI creates `.venv` before running Makefile-based lint, security, and test commands
  - Owner-authored maintenance PRs from `codex/` branches receive an automated approval review from GitHub Actions
- Error handling:
  - If a Dependabot PR changes any disallowed file, validation should continue as normal
  - Empty changed-file lists should not qualify for the Dependabot bypass

### Examples
```text
Dependabot dependency-only PR detected; skipping spec validation.
```

## Acceptance criteria
- AC1: `.github/scripts/validate_pr.py` detects Dependabot-authored PRs and skips spec validation only when every changed file is an allowed dependency or GitHub workflow file.
- AC2: Dependabot PRs that include application or other disallowed file changes continue to require normal spec validation.
- AC3: Tests cover both the allow and reject cases for the Dependabot-specific file filter.
- AC4: `.github/workflows/ci.yml` uses the repository's Makefile-based virtualenv setup so `make security` and the other Make targets run successfully in GitHub Actions.
- AC5: `.github/workflows/auto-approve-own-prs.yml` auto-approves only pull requests into `main` where the PR author matches the repository owner and the head branch starts with `codex/`.

## Security considerations
- Auth/authz impact: Limited repository-governance impact; the new workflow can submit approvals for a tightly constrained class of owner-authored maintenance PRs.
- Input handling or injection risk: Low; the new logic checks fixed GitHub payload fields and repository-controlled paths.
- Secrets or credential handling: None.
- Data exposure or privacy impact: None beyond existing PR metadata handling.
- File system access impact: No additional file access beyond the existing validator behavior.
- Network or external service impact: Uses GitHub Actions and the GitHub CLI against the repository pull request API.
- Dependency or supply-chain impact: This unblocks repository-maintenance PRs from Dependabot without weakening review requirements for source changes and ensures CI uses the same dependency installation path as local development.
- Security notes for reviewers/testers: Verify both exemptions remain narrow so bot-authored source changes cannot bypass the normal spec workflow and auto-approval cannot apply to arbitrary owner PRs.

## Edge cases
- Dependabot PRs that touch both `requirements*.txt` and application code must still fail without a spec.
- Workflow-only Dependabot PRs under `.github/workflows/` should qualify for the bypass.
- Empty file lists should not silently bypass validation.
- CI should not rely on globally installed tooling when the Makefile expects `.venv`.
- Auto-approval should not apply to non-owner PRs or to owner PRs from arbitrary branch names.

## Test guidance
- AC1 -> Unit tests verify accepted Dependabot file lists
- AC2 -> Unit tests verify disallowed source paths fail the Dependabot-only filter
- AC3 -> Unit tests verify the Dependabot bypass remains narrow
- AC4 -> Content tests verify the CI workflow creates `.venv` and runs the Makefile targets, then run `make lint`, `make test`, and `make security`
- AC5 -> Content tests verify the auto-approval workflow uses `pull_request_target`, requires `pull-requests: write`, checks for owner-authored `codex/` branches, and runs `gh pr review --approve`

## Decision log
- 2026-04-01: Kept the exemption scoped to Dependabot plus dependency/workflow-only changes so human PRs and source edits still follow the full spec-first process.
