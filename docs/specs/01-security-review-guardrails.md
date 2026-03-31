# Security Review Guardrails

**Spec file:** `docs/specs/01-security-review-guardrails.md`
**Spec slug:** security-review-guardrails
**Status:** Done
**Owner:** Codex
**Date:** 2026-03-31

## Problem statement
- The current workflow checks process integrity well, but it does not make security review a first-class part of change planning and review.
- Security concerns are mentioned in reviewer guidance, yet they are not consistently surfaced in specs, PR materials, or validation habits.
- Teams using AI-assisted development need lightweight, repeatable security prompts so risky changes are visible before merge.

## Scope
In scope:
- Add a required security considerations section to the spec template.
- Add a lightweight security checklist to PR templates and PR draft templates.
- Update role guidance so reviewer and tester outputs explicitly consider security-relevant change types.
- Define a minimal validation expectation for this repository: security review is documented for code-changing work even when no issue is found.

Out of scope / non-goals:
- Mandating language- or framework-specific security scanners in this phase.
- Guaranteeing that a completed checklist proves the implementation is secure.
- Replacing deeper threat modeling for high-risk systems.
- Requiring repository adopters to use a single AppSec toolchain.

## Assumptions
- This repository is a framework that other repositories may copy, so security guardrails should stay lightweight and broadly reusable.
- The smallest useful improvement is to make security review explicit in planning, implementation, testing, and review artifacts.
- Some changes have no meaningful security impact, and the workflow should allow that to be stated clearly rather than forcing artificial findings.
- Automated security scanners may be added later, but the process should still be useful in repositories where scanners are not yet configured.

## Proposed behavior / API
### Public interface
- Files/modules affected:
  - `.ai/templates/spec_template.md`
  - `.ai/templates/pr_draft_template.md`
  - `.ai/templates/pr_description_template.md`
  - `.ai/templates/review_checklist.md`
  - `.ai/roles/03_tester.md`
  - `.ai/roles/04_reviewer.md`
  - `AGENTS.md`
  - `README.md`

### Inputs / outputs
- Inputs:
  - Draft spec content for a code change
  - PR body and matching PR draft
  - Reviewer and tester outputs
- Outputs:
  - Each code-change spec includes a security considerations section
  - Each PR template and PR draft prompts for a security disposition
  - Review guidance calls out security-sensitive areas that should be checked explicitly
- Error handling:
  - If a change owner cannot determine the security impact, the workflow should surface a blocker rather than silently assuming "no impact"
  - The workflow may record "no meaningful security impact" when justified

### Examples
```md
## Security considerations
- User input reaches shell execution: No
- Auth/authz behavior changed: No
- Secrets or credentials touched: No
- File system or network access changed: Yes
- Risk notes: Added outbound webhook support; reviewer should verify allowlist handling and secret redaction.
```

```md
## Security review
- [x] Security considerations were reviewed and updated in the linked spec
- [x] No auth/authz changes
- [x] No secrets handling changes
- [ ] Security-sensitive behavior changed and needs reviewer attention
```

## Acceptance criteria
- AC1: The spec template includes a `## Security considerations` section with prompts that help authors document whether a change affects auth/authz, input handling, secrets, data exposure, file access, network access, or dependencies.
- AC2: The PR description template and PR draft template include a security review section that lets authors record either "no meaningful security impact" or summarize the security-sensitive behavior that reviewers should check.
- AC3: Reviewer and tester guidance explicitly instructs those roles to examine the documented security considerations and flag blockers when the security impact is unclear or inadequately tested.
- AC4: Repository documentation describes security review as a required part of code-changing work and makes clear that deeper automated scanning is future work rather than current behavior.

## Edge cases
- Pure documentation changes should not require invented security notes.
- A change may touch a traditionally sensitive area, such as network or file access, while still being low risk; the workflow should allow concise justification rather than forcing a fail state.
- Security-relevant uncertainty should use the existing blocker handoff format instead of being buried in free-form notes.
- Repositories adopting this framework may not yet have any security scanner installed.

## Test guidance
- AC1 -> Template tests or content checks verify the spec template includes a security considerations section with the expected prompts
- AC2 -> Template tests or content checks verify both PR templates include a security review section with a documented no-impact path
- AC3 -> Content checks verify reviewer and tester guidance references the security considerations section and unclear-impact blocker handling
- AC4 -> Documentation review verifies the README and AGENTS guidance describe security review as required workflow behavior and call automated scanning future work

## Decision log
- 2026-03-31: Chose a process-first phase so the framework gains explicit security review without prematurely binding adopters to a specific scanner stack.
