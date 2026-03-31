## Summary
- Add a spec for automated security checks in the repository workflow.
- Standardize on a `make security` command backed by Python static analysis and dependency auditing.
- Wire the command into CI and document it as part of normal code-change validation.

## Spec
- Spec: `docs/specs/02-automated-security-checks.md`
- Test plan: `docs/test-plans/02-automated-security-checks.md`
- PR draft path: `.ai/pr-description/02-automated-security-checks.md`

## Acceptance Criteria
- [x] AC1: The repository exposes a `make security` command that runs at least one static security analysis tool and one dependency vulnerability audit suitable for this Python project.
- [x] AC2: The CI workflow runs the automated security checks as part of the standard validation path.
- [x] AC3: Repository documentation and workflow guidance treat `make security` as a standard command for code-changing work.
- [x] AC4: Tests or static assertions verify the security command, CI integration, and documented workflow expectations so the automation remains part of the framework.

## Security Review
- [x] Security considerations were reviewed and updated in the linked spec
- [x] No meaningful security impact
- [ ] Auth/authz behavior changed
- [ ] Secrets or credential handling changed
- [x] Input validation, data exposure, file access, network access, or dependencies changed
- Reviewer focus:
  - Verify the chosen tools fit the repo’s Python footprint and do not silently skip the intended checks.

## Validation
- [x] `make lint`
- [x] `make test`
- [x] `make security`

## Changelog
- [ ] Add to `CHANGELOG.md` under `## Unreleased` if this change should be called out before the next explicit release.

## Open Risks
- Vulnerability audit results can change over time as advisory data changes, so CI behavior may evolve without source changes.
- `pip-audit` currently ignores `CVE-2026-4539` for `pygments` because no fixed version was reported during implementation; that exception should be revisited.
