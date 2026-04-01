# Repo Consistency Alignment

**Spec file:** `docs/specs/05-repo-consistency-alignment.md`
**Spec slug:** repo-consistency-alignment
**Status:** In Progress
**Owner:** Codex
**Date:** 2026-04-01

## Problem statement
- The repository's documented workflow says code-changing PRs must update a matching spec packet, but the validator currently treats several dependency and tooling files as docs-only.
- Historical workflow artifacts also drift from the current repository rules: packet `00` lacks a matching PR draft and security considerations, and packet `01` lacks the now-required security review section in its PR draft.
- These gaps make the repository pass its current tests while still contradicting its stated process.

## Scope
In scope:
- Tighten docs-only detection so dependency and tooling changes require the normal spec-first packet flow for human-authored PRs.
- Keep true documentation-only changes exempt from spec validation.
- Backfill missing or incomplete historical packet artifacts so the repository's own packets match its current workflow expectations.
- Add tests for the stricter validator classification and historical artifact alignment.

Out of scope / non-goals:
- Redesigning the overall spec-first workflow.
- Changing the narrow Dependabot exception added in packet `04`.
- Rewriting historical packet summaries beyond what is needed for consistency.

## Assumptions
- Root documentation files such as `README.md` and `CHANGELOG.md` should remain docs-only.
- Dependency manifests, `Makefile`, and automation config files are workflow-affecting changes and should require specs for human-authored PRs.
- Historical packet artifacts may be updated for accuracy without changing shipped behavior.

## Proposed behavior / API
### Public interface
- Files/modules affected:
  - `.github/scripts/validate_pr.py`
  - `tests/test_validate_pr.py`
  - `tests/test_security_workflow_docs.py`
  - `docs/specs/00-ai-workflow-guardrails.md`
  - `.ai/pr-description/00-ai-workflow-guardrails.md`
  - `.ai/pr-description/01-security-review-guardrails.md`
  - `.ai/pr-description/04-dependabot-pr-validation-exception.md`

### Inputs / outputs
- Inputs:
  - Changed file paths in PR validation
  - Historical packet files in `docs/specs/` and `.ai/pr-description/`
- Outputs:
  - Human-authored dependency and tooling PRs require the normal spec packet
  - Docs-only updates such as `README.md` or `CHANGELOG.md` remain exempt
  - Historical packets include the companion artifacts and sections required by the current repository rules
- Error handling:
  - Validator failures should continue to explain missing packet artifacts clearly
  - Historical artifact alignment should be covered by static tests so future drift is caught quickly

### Examples
```text
Changed files:
- pyproject.toml

Result:
- PR requires linked spec, matching test plan, and matching PR draft
```

```text
Changed files:
- README.md
- CHANGELOG.md

Result:
- PR is treated as docs-only
```

## Acceptance criteria
- AC1: `.github/scripts/validate_pr.py` treats dependency and tooling files such as `pyproject.toml`, `requirements*.in`, `requirements*.txt`, `Makefile`, and `.pre-commit-config.yaml` as code-changing inputs for human-authored PRs, while keeping documentation-only files exempt.
- AC2: Packet `00` includes a matching PR draft and its spec includes the security review information required by the current repository rules.
- AC3: Historical PR drafts that previously predated the current security-review workflow are updated so they include the current required security-review and validation context where applicable.
- AC4: Tests verify the stricter docs-only classification and the presence of the required historical packet artifacts and sections.

## Security considerations
- Auth/authz impact: None; this change affects workflow validation and repository documentation only.
- Input handling or injection risk: Low; validator logic remains path-based and repository-controlled.
- Secrets or credential handling: None.
- Data exposure or privacy impact: None.
- File system access impact: Read-only access to repository files in tests and validation.
- Network or external service impact: None beyond existing CI usage.
- Dependency or supply-chain impact: Tighter validation reduces the chance of unreviewed dependency/tooling changes bypassing the documented workflow.
- Security notes for reviewers/testers: Confirm the stricter classification does not accidentally force specs for ordinary documentation-only edits.

## Edge cases
- `CHANGELOG.md` updates should remain docs-only even though they live at the repo root.
- Dependabot dependency-only PRs should still use the existing exception path from packet `04`.
- Historical packet updates should not invent new behavior; they should only align stored artifacts with the current process.

## Test guidance
- AC1 -> Validator unit tests verify dependency/tooling files are not treated as docs-only and root docs files still are
- AC2 -> Static tests verify packet `00` includes both a security considerations section and a matching PR draft
- AC3 -> Static tests verify historical PR drafts include security review context and completed validation state where expected
- AC4 -> `make lint`, `make test`, and `make security`

## Decision log
- 2026-04-01: Treated dependency and tooling files as code-changing for human PRs because that matches the repository's written policy and keeps the Dependabot exception intentionally narrow.
