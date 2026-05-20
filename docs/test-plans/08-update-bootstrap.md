# Test Plan: update-bootstrap

Path: `docs/test-plans/08-update-bootstrap.md`

## What changed
- Added 14 new files and updated 7 existing files in `.ai/bootstrap/spec-first-repo/`.
- Added `GETTING_STARTED.md` at `.ai/bootstrap/`.
- All changes are documentation, templates, and copy-ready tooling; no application logic changed.

## Acceptance criteria coverage
- AC1: `test_bootstrap_files_present` — checks every expected file path exists.
- AC2: `test_bootstrap_agents_has_placeholders` — asserts command placeholders appear in
  AGENTS.md and not the literal `make lint` / `make test` strings.
- AC3: `test_bootstrap_role_files_present` — checks all five role files exist and are non-empty.
- AC4: `test_bootstrap_templates_have_security_sections` — checks that spec_template.md contains
  "Security considerations", and that pr_draft/pr_description templates contain "Security Review"
  or "Security review".
- AC5: `test_getting_started_exists` — checks the file exists and covers expected headings.
- AC6: `test_bootstrap_validate_pr_functions_present` — checks that key function names from the
  main repo's script are present in the bootstrap copy.

## Edge cases
- From spec:
  - `ci.yml` contains placeholder echo commands — checked that the file exists and is valid YAML.
  - `validate_pr.py` extends `DEPENDABOT_ALLOWED_ROOT_FILES` with Node/Rust/Go entries.
- Additional adversarial cases:
  - Bootstrap AGENTS.md must not contain literal `make lint` (would be a regression to old state).
  - Bootstrap spec_template.md must not be missing the Security considerations section
    (confirms the template sync happened correctly).
  - Bootstrap `validate_pr.py` must contain the `main()` entry point (ensures it was not
    accidentally truncated).

## Notes
- Flaky risks: None — all tests are pure file-read assertions with no I/O side effects.
- Determinism: Fully deterministic.
