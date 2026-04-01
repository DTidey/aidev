# Dependabot Auto Management

**Spec file:** `docs/specs/05-dependabot-auto-management.md`
**Spec slug:** dependabot-auto-management
**Status:** Done
**Owner:** Codex
**Date:** 2026-04-01

## Problem statement
- `aidev` now lets dependency-only Dependabot PRs bypass the spec validator, but those PRs can still remain blocked on approval and merge steps.
- This repository is currently maintained by a single person, so requiring a second manual reviewer for routine Dependabot updates creates unnecessary friction.
- Any automation here must stay narrow so it does not auto-approve or auto-merge arbitrary bot or owner pull requests.

## Scope
In scope:
- Add a GitHub Actions workflow that auto-approves and enables auto-merge for qualifying Dependabot PRs.
- Limit the workflow to Dependabot-authored PRs into `main` from `dependabot/` branches.
- Limit the workflow to dependency manifest and GitHub workflow file changes only.
- Add tests that pin the workflow’s safety constraints.

Out of scope / non-goals:
- Auto-merging non-Dependabot pull requests.
- Auto-merging Dependabot PRs that change application source files.
- Reworking the existing PR validator or CI workflow behavior beyond what is needed to support safe Dependabot automation.

## Assumptions
- Repository settings already allow GitHub Actions to create and approve pull requests.
- Repository settings allow auto-merge for pull requests.
- Dependabot branches follow the `dependabot/` naming pattern used by GitHub.
- The next available packet prefix is `05`.

## Proposed behavior / API
### Public interface
- Files/modules affected:
  - `docs/specs/05-dependabot-auto-management.md`
  - `docs/test-plans/05-dependabot-auto-management.md`
  - `.ai/pr-description/05-dependabot-auto-management.md`
  - `.github/workflows/auto-manage-dependabot-prs.yml`
  - `tests/test_security_workflow_docs.py`

### Inputs / outputs
- Inputs:
  - Pull request author, base branch, and head branch from the GitHub event payload
  - Changed filenames returned by the GitHub pull-request files API
- Outputs:
  - Qualifying Dependabot PRs receive an approval review from GitHub Actions
  - Qualifying Dependabot PRs have auto-merge enabled with squash merging
  - Non-qualifying Dependabot PRs are left for manual review
- Error handling:
  - Empty file lists should not qualify for automation
  - Any disallowed changed file should stop the auto-approval and auto-merge path
  - If auto-merge is unavailable in repository settings, the workflow should fail visibly rather than silently pretending to succeed

### Examples
```text
Dependabot PR not eligible for auto-management.
```

## Acceptance criteria
- AC1: `aidev` includes a workflow that runs on `pull_request_target` for `main` and only considers PRs authored by `dependabot[bot]` from `dependabot/` branches.
- AC2: The workflow only auto-manages PRs whose changed files are limited to root dependency manifests or `.github/workflows/*.yml` and `.yaml` files.
- AC3: Eligible Dependabot PRs are auto-approved and set to auto-merge using squash merging.
- AC4: Tests verify the workflow exists and pins the author, branch, permission, file-filter, approval, and auto-merge safeguards.

## Security considerations
- Auth/authz impact: Limited repository-governance impact; the workflow can approve and queue merges, so it must stay tightly scoped.
- Input handling or injection risk: Low; decisions are based on repository-controlled filenames and GitHub event metadata.
- Secrets or credential handling: Uses the repository GitHub token only.
- Data exposure or privacy impact: None beyond standard pull-request metadata access.
- File system access impact: None locally; the workflow inspects PR metadata via the GitHub API.
- Network or external service impact: Uses GitHub Actions, GitHub REST APIs, and the GitHub CLI.
- Dependency or supply-chain impact: Speeds up dependency hygiene while intentionally limiting automation to routine dependency/workflow updates.
- Security notes for reviewers/testers: Verify the workflow cannot auto-manage source-code changes or non-Dependabot branches.

## Edge cases
- Dependabot PRs that update workflow dependencies under `.github/workflows/` should still qualify.
- Dependabot PRs that mix workflow/dependency updates with `tests/`, `.github/scripts/`, or application files must not qualify.
- The workflow should not treat an empty file list as safe.

## Test guidance
- AC1 -> Content tests verify `pull_request_target`, `dependabot[bot]`, `dependabot/`, and `main` targeting
- AC2 -> Content tests verify the workflow enumerates the dependency allowlist and `.github/workflows/` file pattern
- AC3 -> Content tests verify `gh pr review --approve` and `gh pr merge --auto --squash`
- AC4 -> Run `make lint`, `make test`, and `make security`

## Decision log
- 2026-04-01: Kept Dependabot automation separate from owner-maintenance automation so each path can stay narrowly scoped and easier to review.
