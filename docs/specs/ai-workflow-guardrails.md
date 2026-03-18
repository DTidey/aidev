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

Out of scope / non-goals:
- Changing the role order or the overall multi-agent workflow.
- Validating whether checked acceptance criteria are semantically true.

## Assumptions
- Each code-changing PR should have exactly one source-of-truth spec.
- Specs used for implementation are intended to be fully satisfied before merge.
- A matching test plan should use the same slug as the linked spec.

## Proposed behavior / API
### Public interface
- Files/modules affected:
  - `.github/scripts/validate_pr.py`
  - `.github/PULL_REQUEST_TEMPLATE.md`
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
  - Validation should explain whether the issue is missing spec linkage, incomplete AC coverage, or missing test plan files.

### Examples
```text
Spec: docs/specs/ai-workflow-guardrails.md
Test plan: docs/test-plans/ai-workflow-guardrails.md
PR body:
- Link to docs/specs/ai-workflow-guardrails.md
- [x] AC1 ...
- [x] AC2 ...
- [x] AC3 ...
```

## Acceptance criteria
- AC1: For code-changing PRs, the linked spec in the PR body must exist and must be one of the spec files changed in the PR.
- AC2: For code-changing PRs, the PR body must include checked entries for every acceptance criterion defined in the linked spec, and must not reference unknown AC IDs.
- AC3: For code-changing PRs, a test plan file must exist at `docs/test-plans/<slug>.md` and that file must be added or updated in the PR.

## Edge cases
- Docs-only PRs should not require a spec or test plan update.
- Spec files with multi-digit AC IDs such as `AC10` should validate correctly.
- The validator should report missing checked ACs separately from unknown checked ACs.

## Test guidance
- AC1 -> validator unit tests for linked spec membership in changed files
- AC2 -> validator unit tests for missing and unknown AC IDs
- AC3 -> validator unit tests for matching test plan path existence and changed-file checks

## Decision log
- 2026-03-18: Standardized test plan location as `docs/test-plans/<slug>.md` to make AI outputs discoverable and machine-checkable.
