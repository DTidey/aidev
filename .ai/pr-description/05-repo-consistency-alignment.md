## Summary
- Align the validator with the repository's written rule that dependency and tooling changes are code changes for human-authored PRs.
- Backfill historical packet artifacts so older packets match the current security-review and companion-file requirements.
- Add tests that pin both behaviors so the repo stays internally consistent.

## Spec
- Spec: `docs/specs/05-repo-consistency-alignment.md`
- Test plan: `docs/test-plans/05-repo-consistency-alignment.md`
- PR draft path: `.ai/pr-description/05-repo-consistency-alignment.md`

## Acceptance Criteria
- [x] AC1: `.github/scripts/validate_pr.py` treats dependency and tooling files such as `pyproject.toml`, `requirements*.in`, `requirements*.txt`, `Makefile`, and `.pre-commit-config.yaml` as code-changing inputs for human-authored PRs, while keeping documentation-only files exempt.
- [x] AC2: Packet `00` includes a matching PR draft and its spec includes the security review information required by the current repository rules.
- [x] AC3: Historical PR drafts that previously predated the current security-review workflow are updated so they include the current required security-review and validation context where applicable.
- [x] AC4: Tests verify the stricter docs-only classification and the presence of the required historical packet artifacts and sections.

## Security Review
- [x] Security considerations were reviewed and updated in the linked spec
- [x] No meaningful security impact
- [ ] Auth/authz behavior changed
- [ ] Secrets or credential handling changed
- [x] Input validation, data exposure, file access, network access, or dependencies changed
- Reviewer focus:
  - Confirm docs-only detection stays narrow and that historical artifact updates improve accuracy without changing workflow behavior.

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
- Historical packet backfills improve consistency, but repository settings in the GitHub UI still need to stay aligned separately.
