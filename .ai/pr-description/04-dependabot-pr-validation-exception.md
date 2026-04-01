## Summary
- Allow Dependabot maintenance PRs to bypass spec validation only when they change dependency manifests or GitHub workflow files.
- Preserve the existing spec-first enforcement for human-authored PRs and for any PR that touches application code.
- Add tests to pin the allowlist so the exception stays intentionally narrow.

## Spec
- Spec: `docs/specs/04-dependabot-pr-validation-exception.md`
- Test plan: `docs/test-plans/04-dependabot-pr-validation-exception.md`
- PR draft path: `.ai/pr-description/04-dependabot-pr-validation-exception.md`

## Acceptance Criteria
- [x] AC1: `.github/scripts/validate_pr.py` detects Dependabot-authored PRs and skips spec validation only when every changed file is an allowed dependency or GitHub workflow file.
- [x] AC2: Dependabot PRs that include application or other disallowed file changes continue to require normal spec validation.
- [x] AC3: Tests cover both the allow and reject cases for the Dependabot-specific file filter.

## Security Review
- [x] Security considerations were reviewed and updated in the linked spec
- [x] No meaningful security impact
- [ ] Auth/authz behavior changed
- [ ] Secrets or credential handling changed
- [x] Input validation, data exposure, file access, network access, or dependencies changed
- Reviewer focus:
  - Confirm the new bypass remains limited to `dependabot[bot]` and dependency/workflow-only diffs.

## Validation
- [ ] `make lint`
- [ ] `make test`
- [ ] `make security`

## GitHub Checks
- Required checks for `main`:
  - `CI / test`
  - `CodeQL / analyze`

## Changelog
- [ ] Add to `CHANGELOG.md` under `## Unreleased` if this change should be called out before the next explicit release.

## Open Risks
- The allowlist may need future updates if the repository adopts additional dependency manifest files.
