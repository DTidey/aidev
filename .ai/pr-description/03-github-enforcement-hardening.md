## Summary
- Add GitHub-native repository hardening with CodeQL, Dependabot, and `CODEOWNERS`.
- Align the public PR template with the repo's current security review workflow.
- Document the exact branch protection settings and required checks to enable on `main`.

## Spec
- Spec: `docs/specs/03-github-enforcement-hardening.md`
- Test plan: `docs/test-plans/03-github-enforcement-hardening.md`
- PR draft path: `.ai/pr-description/03-github-enforcement-hardening.md`

## Acceptance Criteria
- [x] AC1: The repository includes GitHub-native automation for code scanning and dependency update PRs.
- [x] AC2: The repository defines explicit code ownership and a public PR template that reflects the current security workflow.
- [x] AC3: Repository docs tell maintainers which branch protection settings and required status checks to enable on `main`.
- [x] AC4: Tests or static assertions verify the GitHub automation, ownership, templates, and documentation remain present.

## Security Review
- [x] Security considerations were reviewed and updated in the linked spec
- [x] No meaningful security impact
- [ ] Auth/authz behavior changed
- [ ] Secrets or credential handling changed
- [x] Input validation, data exposure, file access, network access, or dependencies changed
- Reviewer focus:
  - Confirm the documented required check names match the workflow names emitted by GitHub Actions.

## Validation
- [x] `make lint`
- [x] `make test`
- [x] `make security`

## Changelog
- [ ] Add to `CHANGELOG.md` under `## Unreleased` if this change should be called out before the next explicit release.

## Open Risks
- The repository-side documentation can recommend branch protection, but the final GitHub settings still need to be enabled in the repository UI.
