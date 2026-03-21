# AI Workflow Guardrails

**Spec slug:** ai-workflow-guardrails
**Status:** In Progress
**Owner:** Codex
**Date:** 2026-03-18

## Problem statement
- The current workflow describes strong spec-first guardrails, but CI does not fully enforce them.
- AI agents are more reliable when required artifacts are easy to find and validation is explicit.

## Scope
In scope:
- Tighten PR validation so code-changing PRs are tied to the exact spec they update.
- Require PR bodies to account for every acceptance criterion in the linked spec.
- Define a canonical test plan location and require it for code-changing PRs.
- Define a canonical PR draft location and require the matching draft for code-changing PRs.

Out of scope / non-goals:
- Changing the role order or the overall multi-agent workflow.
- Validating whether checked acceptance criteria are semantically true.

## Assumptions
- Each code-changing PR should have exactly one source-of-truth spec.
- Specs used for implementation are intended to be fully satisfied before merge.
- A matching test plan should use the same slug as the linked spec.
- A matching PR draft should use the same slug as the linked spec and mirror the spec linkage and AC checklist.

## Proposed behavior / API
### Public interface
- Files/modules affected:
  - `.github/scripts/validate_pr.py`
  - `.github/PULL_REQUEST_TEMPLATE.md`
  - `.ai/templates/pr_draft_template.md`
  - `.ai/templates/test_plan_template.md`
  - `.ai/roles/03_tester.md`
  - `AGENTS.md`
  - `README.md`

### Inputs / outputs
- Inputs:
  - Pull request body
  - Changed file list for the PR
  - Linked spec file contents
- Outputs:
  - Passing validation when required workflow artifacts and PR metadata are present
  - Clear validation errors when artifacts are missing or inconsistent
- Error handling:
  - Validation should explain whether the issue is missing spec linkage, incomplete AC coverage, or missing packet artifacts such as the test plan or PR draft.

### Examples
```text
Spec: docs/specs/00-ai-workflow-guardrails.md
Test plan: docs/test-plans/00-ai-workflow-guardrails.md
PR draft: .ai/pr-description/00-ai-workflow-guardrails.md
PR body:
- Link to docs/specs/00-ai-workflow-guardrails.md
- [x] AC1 ...
- [x] AC2 ...
- [x] AC3 ...
- [x] AC4 ...
```

## Acceptance criteria
- AC1: For code-changing PRs, the linked spec in the PR body must exist and must be one of the spec files changed in the PR.
- AC2: For code-changing PRs, the PR body must include checked entries for every acceptance criterion defined in the linked spec, and must not reference unknown AC IDs.
- AC3: For code-changing PRs, a test plan file must exist at `docs/test-plans/<nn>-<slug>.md` and that file must be added or updated in the PR.
- AC4: For code-changing PRs, a PR draft file must exist at `.ai/pr-description/<nn>-<slug>.md`, must be added or updated in the PR, must link the same spec path, and must check every acceptance criterion defined in that spec without unknown AC IDs.

## Edge cases
- Docs-only PRs should not require a spec, test plan, or PR draft update.
- Spec files with multi-digit AC IDs such as `AC10` should validate correctly.
- The validator should report missing checked ACs separately from unknown checked ACs for both the PR body and the PR draft.

## Test guidance
- AC1 -> validator unit tests for linked spec membership in changed files
- AC2 -> validator unit tests for missing and unknown AC IDs
- AC3 -> validator unit tests for matching test plan path existence and changed-file checks
- AC4 -> validator unit tests for matching PR draft path derivation, existence, changed-file checks, spec linkage, and AC coverage

## Decision log
- 2026-03-18: Standardized test plan location as `docs/test-plans/<nn>-<slug>.md` to make AI outputs discoverable and machine-checkable.
- 2026-03-21: Standardized PR draft location as `.ai/pr-description/<nn>-<slug>.md` and decided CI should validate its spec link and AC checklist just like the PR body.
