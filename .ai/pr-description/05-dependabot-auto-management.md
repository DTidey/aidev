## Summary
- Add a narrowly scoped workflow to auto-approve and auto-merge safe Dependabot PRs.
- Limit that automation to `dependabot[bot]` PRs from `dependabot/` branches that only change dependency manifests or GitHub workflow files.
- Add tests to pin the workflow’s scope and safety constraints.

## Spec
- Spec: `docs/specs/05-dependabot-auto-management.md`
- Test plan: `docs/test-plans/05-dependabot-auto-management.md`
- PR draft path: `.ai/pr-description/05-dependabot-auto-management.md`

## Acceptance Criteria
- [x] AC1: `aidev` includes a workflow that runs on `pull_request_target` for `main` and only considers PRs authored by `dependabot[bot]` from `dependabot/` branches.
- [x] AC2: The workflow only auto-manages PRs whose changed files are limited to root dependency manifests or `.github/workflows/*.yml` and `.yaml` files.
- [x] AC3: Eligible Dependabot PRs are auto-approved and set to auto-merge using squash merging.
- [x] AC4: Tests verify the workflow exists and pins the author, branch, permission, file-filter, approval, and auto-merge safeguards.

## Security Review
- [x] Security considerations were reviewed and updated in the linked spec
- [x] No meaningful security impact
- [ ] Auth/authz behavior changed
- [ ] Secrets or credential handling changed
- [x] Input validation, data exposure, file access, network access, or dependencies changed
- Reviewer focus:
  - Confirm the workflow cannot auto-manage PRs outside the intended Dependabot dependency/workflow-update path.

## Validation
- [x] `make lint`
- [x] `make test`
- [x] `make security`

## GitHub Checks
- Required checks for `main`:
  - `CI / test`
  - `CodeQL / analyze`

## Changelog
- [ ] Add to `CHANGELOG.md` under `## Unreleased` if this change should be called out before the next explicit release.

## Open Risks
- Auto-merge still depends on repository settings permitting Actions approval and pull-request auto-merge.
