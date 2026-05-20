# Validator Expectations

Use this as a reference when customizing `.github/scripts/validate_pr.py` for your project.

The included script enforces the spec-first workflow automatically on every PR. It requires only
the Python standard library and runs in CI via `.github/workflows/ci.yml`.

## What the validator enforces

### Always checked
- PR body is non-empty (author filled in the template).

### Checked for code-changing PRs
- A spec under `docs/specs/<nn>-<slug>.md` was modified in the PR.
- Spec files use a two-digit prefix (`\d{2}-[a-z0-9][a-z0-9-]*.md`).
- The PR body links the spec path (`docs/specs/<nn>-<slug>.md`).
- The linked spec file actually exists.
- The linked spec was modified in this PR (not just referenced).
- Every AC defined in the linked spec is checked (`- [x] ACn`) in the PR body.
- No unknown AC IDs are checked in the PR body.
- A matching test plan exists at `docs/test-plans/<nn>-<slug>.md` and was updated.
- A matching PR draft exists at `.ai/pr-description/<nn>-<slug>.md` and was updated.
- The PR draft links the same spec path as the PR body.
- The PR draft checks the same set of ACs as the spec defines.

### Exempted automatically
- Dependabot PRs that touch only known dependency files (pip, npm, Cargo, Go, GitHub Actions
  workflows) skip spec validation entirely.

## What counts as a "non-code" path

Docs-only PRs (no spec required) consist entirely of:
- `README.md` and `CHANGELOG.md` in the repo root
- `.md`, `.rst`, or `.txt` files under `docs/`, `.ai/`, or `.github/`

All other changed files trigger the spec requirement.

## Adapting the validator for your project

### Adding dependency file exemptions
Edit `DEPENDABOT_ALLOWED_ROOT_FILES` in `validate_pr.py` to add your project's lock files or
manifest files. The script already covers common Python, Node, Rust, and Go filenames.

### Adding non-code paths
Edit `NON_CODE_ROOT_FILES` or `is_non_code_path()` if your project has additional always-safe
doc paths.

### Changing the spec path convention
The `SPEC_LINK_PATTERN` regex enforces `docs/specs/\d{2}-[a-z0-9][a-z0-9-]*.md`. If you change
this convention, update the regex and the companion path derivation functions
(`test_plan_path_for_spec`, `pr_draft_path_for_spec`).

## Unit testing the validator

Add tests for:
- Spec link parsing (valid and invalid patterns)
- AC extraction from spec and PR body
- Artifact path derivation from spec path
- Packet name validation (two-digit prefix)
- Docs-only detection
- Dependabot exemption
- Missing/extra AC detection

The existing `tests/test_validate_pr.py` in the aidev bootstrap repo provides a reference
implementation of these tests.
