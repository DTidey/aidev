# Validator Expectations

Use this as a checklist when adding CI or local validation for the spec-first workflow.

## Minimum Checks
- Reject code-changing PRs that do not update a linked spec in `docs/specs/<nn>-<slug>.md`.
- Ensure the linked spec is one of the changed spec files in the PR.
- Ensure the PR body checks every acceptance criterion defined in the linked spec.
- Require a matching test plan at `docs/test-plans/<nn>-<slug>.md` for code changes.
- Require a matching PR draft at `.ai/pr-description/<nn>-<slug>.md` for code changes.
- Ensure the PR draft links the same spec path as the PR body.
- Ensure acceptance criteria checked in the PR draft are a complete match for the linked spec's AC IDs.
- Enforce the two-digit packet naming convention when the repo uses numbered packets.

## Recommended Checks
- Ignore supporting docs such as `README.md` and folder `README.md` files when determining changed specs.
- Validate multi-digit AC IDs such as `AC10`.
- Fail clearly when unknown AC IDs are checked.
- Fail clearly when expected artifacts are missing or misnamed.
- Distinguish docs-only changes from code-changing PRs.

## Suggested Commands
- `<lint command>`
- `<test command>`

## Implementation Notes
- Keep validator logic in a small script or testable module.
- Add unit tests for spec link parsing, AC extraction, artifact path derivation, and packet-name validation.
- Prefer machine-checkable conventions over reviewer memory.
