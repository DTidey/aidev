## Summary
- Rewrote and extended the bootstrap at `.ai/bootstrap/spec-first-repo/` to be comprehensive and
  current with the evolved workflow.
- Added 14 new files: five role definitions, a CLAUDE.md template, 10Rules.md, CHANGELOG.md
  starter, full GitHub infrastructure (validate_pr.py, ci.yml, PULL_REQUEST_TEMPLATE.md,
  CODEOWNERS, dependabot.yml), directory placeholders, and docs/test-plans/README.md.
- Updated 7 existing files: AGENTS.md (synced with root), all four templates (security sections
  added), README.md, and validator-expectations.md.
- Added `GETTING_STARTED.md` at `.ai/bootstrap/` with a nine-step setup guide.

## Spec
- Spec: `docs/specs/08-update-bootstrap.md`
- Test plan: `docs/test-plans/08-update-bootstrap.md`
- PR draft path: `.ai/pr-description/08-update-bootstrap.md`

## Acceptance Criteria
- [x] AC1: The bootstrap directory contains all files listed in the Proposed behavior section.
- [x] AC2: AGENTS.md in the bootstrap uses `<placeholder>` values for project-specific commands.
- [x] AC3: All five role files are present in `.ai/roles/` with correct content.
- [x] AC4: All four templates include the Security considerations / Security review sections.
- [x] AC5: GETTING_STARTED.md exists at `.ai/bootstrap/` and covers all setup steps.
- [x] AC6: validate_pr.py in the bootstrap is functionally equivalent to the main repo's script.

## Security Review
- [x] Security considerations were reviewed and updated in the linked spec
- [x] No meaningful security impact
- Reviewer focus: None required — changes are documentation and templates only.

## Validation
- [x] `make lint`
- [x] `make test`
- [x] `make security`

## GitHub Checks
- Required checks for `main`:
  - `CI / test`
  - `CodeQL / analyze`

## Changelog
- [ ] Add to `CHANGELOG.md` under `## Unreleased` if this change should be called out before the
  next explicit release.

## Open Risks
- The bootstrap `validate_pr.py` is a copy of the main repo's script and may diverge over time.
  This is documented in validator-expectations.md.
