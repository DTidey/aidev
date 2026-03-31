## Summary
- Add a spec for introducing security review guardrails into the spec-first workflow.
- Propose a process-first phase covering templates, reviewer/tester guidance, and repository docs.
- Leave scanner/toolchain integration as explicit future work.

## Spec
- Spec: `docs/specs/01-security-review-guardrails.md`
- Test plan: `docs/test-plans/01-security-review-guardrails.md`
- PR draft path: `.ai/pr-description/01-security-review-guardrails.md`

## Acceptance Criteria
- [x] AC1: The spec template includes a `## Security considerations` section with prompts that help authors document whether a change affects auth/authz, input handling, secrets, data exposure, file access, network access, or dependencies.
- [x] AC2: The PR description template and PR draft template include a security review section that lets authors record either "no meaningful security impact" or summarize the security-sensitive behavior that reviewers should check.
- [x] AC3: Reviewer and tester guidance explicitly instructs those roles to examine the documented security considerations and flag blockers when the security impact is unclear or inadequately tested.
- [x] AC4: Repository documentation describes security review as a required part of code-changing work and makes clear that deeper automated scanning is future work rather than current behavior.

## Validation
- [x] `make lint`
- [x] `make test`

## Changelog
- [ ] Add to `CHANGELOG.md` under `## Unreleased` if this change should be called out before the next explicit release.

## Open Risks
- This packet only proposes the workflow change; implementation details and validation depth still need to be decided when the spec is executed.
