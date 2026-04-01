## Summary
- Tighten PR validation so code-changing PRs link the exact spec they update.
- Require matching test-plan and PR-draft packet artifacts for code-changing work.
- Keep acceptance-criteria tracking machine-checkable in both the PR body and the PR draft.

## Spec
- Spec: `docs/specs/00-ai-workflow-guardrails.md`
- Test plan: `docs/test-plans/00-ai-workflow-guardrails.md`
- PR draft path: `.ai/pr-description/00-ai-workflow-guardrails.md`

## Acceptance Criteria
- [x] AC1: For code-changing PRs, the linked spec in the PR body must exist and must be one of the spec files changed in the PR.
- [x] AC2: For code-changing PRs, the PR body must include checked entries for every acceptance criterion defined in the linked spec, and must not reference unknown AC IDs.
- [x] AC3: For code-changing PRs, a test plan file must exist at `docs/test-plans/<nn>-<slug>.md` and that file must be added or updated in the PR.
- [x] AC4: For code-changing PRs, a PR draft file must exist at `.ai/pr-description/<nn>-<slug>.md`, must be added or updated in the PR, must link the same spec path, and must check every acceptance criterion defined in that spec without unknown AC IDs.

## Security Review
- [x] Security considerations were reviewed and updated in the linked spec
- [x] No meaningful security impact
- [ ] Auth/authz behavior changed
- [ ] Secrets or credential handling changed
- [x] Input validation, data exposure, file access, network access, or dependencies changed
- Reviewer focus:
  - Confirm the validator stays strict for code-changing PRs while continuing to exempt true documentation-only changes.

## Validation
- [x] `make lint`
- [x] `make test`

## Open Risks
- This packet enforces artifact presence and checklist completeness, but it does not attempt to prove whether each checked acceptance criterion is semantically true.
