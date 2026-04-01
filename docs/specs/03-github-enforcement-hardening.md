# GitHub Enforcement Hardening

**Spec file:** `docs/specs/03-github-enforcement-hardening.md`
**Spec slug:** github-enforcement-hardening
**Status:** Done
**Owner:** Codex
**Date:** 2026-04-01

## Problem statement
- The repository now has documented security review and automated checks, but GitHub-side enforcement is still too implicit.
- Without clear required checks and ownership rules, contributors can bypass or misconfigure the intended workflow protections on `main`.
- Dependency updates and code scanning should be first-class repository defaults rather than ad hoc follow-up work.

## Scope
In scope:
- Add GitHub-native security and maintenance configuration for code scanning and dependency updates.
- Add a `CODEOWNERS` file so review ownership is explicit.
- Document the recommended branch protection settings and exact required checks for `main`.
- Update templates and tests so these expectations remain visible and verifiable.

Out of scope / non-goals:
- Managing GitHub branch protection settings through Terraform or the GitHub API.
- Enforcing organization-wide policies outside this repository.
- Adding paid GitHub security features that may not be available on every plan.

## Assumptions
- `main` is the protected default branch for this repository.
- A lightweight owner model is sufficient for now because the repository currently has a single primary maintainer.
- GitHub Actions and Dependabot are available for this repository.
- Code scanning should focus on Python and GitHub Actions content in this repo.

## Proposed behavior / API
### Public interface
- Files/modules affected:
  - `.github/workflows/ci.yml`
  - `.github/workflows/codeql.yml`
  - `.github/dependabot.yml`
  - `.github/CODEOWNERS`
  - `.github/PULL_REQUEST_TEMPLATE.md`
  - `README.md`
  - `AGENTS.md`
  - `.ai/templates/pr_description_template.md`
  - `.ai/templates/pr_draft_template.md`
  - `tests/test_security_workflow_docs.py`

### Inputs / outputs
- Inputs:
  - Pull requests targeting `main`
  - Dependency manifests and GitHub workflow files
  - Repository ownership and review expectations
- Outputs:
  - GitHub can run CodeQL analysis on PRs and pushes to `main`
  - Dependabot can propose updates for Python packages and GitHub Actions
  - Review ownership is declared in `CODEOWNERS`
  - Documentation names the exact checks to require in branch protection
- Error handling:
  - Missing or broken GitHub config should fail static assertions in the test suite
  - CodeQL failures should surface as a failing GitHub Actions check

### Examples
```text
Required checks on main:
- CI / test
- CodeQL / analyze
```

```text
Recommended branch protection:
- Require a pull request before merging
- Require status checks to pass before merging
- Dismiss stale approvals when new commits are pushed
- Block force pushes and branch deletion on main
```

## Acceptance criteria
- AC1: The repository includes GitHub-native automation for code scanning and dependency update PRs.
- AC2: The repository defines explicit code ownership and a public PR template that reflects the current security workflow.
- AC3: Repository docs tell maintainers which branch protection settings and required status checks to enable on `main`.
- AC4: Tests or static assertions verify the GitHub automation, ownership, templates, and documentation remain present.

## Security considerations
- Auth/authz impact: No runtime auth change; repository maintainers get clearer review and merge controls.
- Input handling or injection risk: Low; changes are declarative GitHub configuration and documentation.
- Secrets or credential handling: Avoid workflows that require extra secrets for routine code scanning or dependency update checks.
- Data exposure or privacy impact: Low; CodeQL analyzes repository content already visible to GitHub Actions.
- File system access impact: Limited to GitHub Actions runners checking out the repository for analysis.
- Network or external service impact: Dependabot and CodeQL rely on GitHub-hosted services and package metadata sources.
- Dependency or supply-chain impact: Dependabot improves visibility into dependency drift; GitHub Actions updates are included to reduce stale action references.
- Security notes for reviewers/testers: Confirm the documented required check names match the workflow job names so branch protection does not silently point at the wrong checks.

## Edge cases
- Status check names can drift if workflow or job names change; tests and docs should keep them aligned.
- Public repositories may have feature differences depending on account plan, so guidance should avoid assuming advanced enterprise-only controls.
- Single-maintainer ownership still benefits from `CODEOWNERS` because it makes the intended reviewer path explicit and easier to scale later.

## Test guidance
- AC1 -> Tests verify CodeQL workflow and Dependabot config exist and target the expected ecosystems
- AC2 -> Tests verify `CODEOWNERS` exists and the public PR template includes security and `make security`
- AC3 -> Documentation review verifies README and AGENTS list recommended branch protection and required checks
- AC4 -> Tests verify the exact required check names documented by the repository

## Decision log
- 2026-04-01: Chose GitHub-native CodeQL and Dependabot as the default enforcement additions because they work well with the existing GitHub Actions-based workflow and require little repository-specific ceremony.
- 2026-04-01: Documented branch protection settings in-repo rather than attempting API-driven configuration so the repository stays portable across personal and organizational GitHub setups.
