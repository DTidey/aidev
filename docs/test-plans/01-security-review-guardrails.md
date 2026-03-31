# Test Plan: security-review-guardrails

Path: `docs/test-plans/01-security-review-guardrails.md`

## What changed
- Added a proposal to make security review a first-class workflow concern in specs, PR materials, and review guidance.
- Kept this phase process-focused so repositories can adopt the guardrails before selecting specific security tools.

## Acceptance criteria coverage
- AC1: Verify the spec template includes a `## Security considerations` section with prompts for auth/authz, input handling, secrets, data exposure, file access, network access, and dependencies.
- AC2: Verify both PR templates include a security review section that supports either a no-impact statement or a concise summary of security-sensitive behavior.
- AC3: Verify tester and reviewer guidance references the documented security considerations and uses blocker language when the impact is unclear.
- AC4: Verify repository docs describe security review as required workflow behavior for code changes and describe automated scanning as future work.

## Edge cases
- From spec:
  - Docs-only changes should not require invented security notes.
  - Low-risk changes in sensitive areas should allow concise justification instead of forced failure.
  - Unclear security impact should use the existing blocker handoff format.
  - Adopting repositories may not yet have security scanners configured.
- Additional adversarial cases:
  - A template adds a vague security heading without concrete prompts, making review inconsistent.
  - PR materials mention security but provide no explicit no-impact option, encouraging empty boilerplate.
  - Reviewer guidance mentions security generally but does not tell reviewers what to do when the impact is unclear.

## Notes
- Flaky risks: None expected; these checks are static content validation or documentation review.
- Determinism considerations: Prefer file-content assertions over narrative review where practical.
