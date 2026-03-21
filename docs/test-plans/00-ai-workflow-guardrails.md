# Test Plan: ai-workflow-guardrails

## What changed
- Tightened PR validation so code PRs must update the exact linked spec.
- Required checked PR-body coverage for every AC in the linked spec.
- Standardized test plan files at `docs/test-plans/<nn>-<slug>.md` and required them for code PRs.
- Standardized PR draft files at `.ai/pr-description/<nn>-<slug>.md` and required them for code PRs.

## Acceptance criteria coverage
- AC1: Tests verify the linked spec must be present in the PR's changed spec files.
- AC2: Tests verify all spec ACs must be checked and unknown ACs are rejected.
- AC3: Tests verify the expected test plan path is derived from the spec slug and must be changed in the PR.
- AC4: Tests verify the expected PR draft path is derived from the spec slug, must be changed in the PR, and must include the linked spec plus complete AC coverage.

## Edge cases
- From spec:
  - Docs-only PRs should not require workflow artifacts.
  - Multi-digit AC IDs should validate correctly.
  - Missing ACs and unknown ACs should be reported separately for both the PR body and the PR draft.
- Additional adversarial cases:
  - PR body links a real spec file that was not changed in the PR.
  - A matching test plan file exists on disk but was not updated in the PR.
  - A PR checks only a subset of ACs from the linked spec.
  - A matching PR draft file exists on disk but was not updated in the PR.
  - A PR draft links the wrong spec path.
  - A PR draft checks an AC that is not defined in the linked spec.

## Notes
- Flaky risks: None expected; validator tests are file- and string-based.
- Determinism considerations: Use temporary files and pure functions where possible.
