# Update bootstrap to be comprehensive and current

**Spec file:** `docs/specs/08-update-bootstrap.md`
**Spec slug:** update-bootstrap
**Status:** Done
**Owner:** DTidey
**Date:** 2026-05-20

## Problem statement
- The bootstrap at `.ai/bootstrap/spec-first-repo/` was created before the workflow matured and
  is now significantly out of date.
- It is missing role definitions, GitHub infrastructure files, a CLAUDE.md template, 10Rules.md,
  and security review additions that have since been added to the main repo.
- A new project copying the bootstrap would get an incomplete and inconsistent starting point.

## Scope
In scope:
- Update existing bootstrap files to match the current repo's workflow artifacts.
- Add all missing files so the bootstrap directory is self-contained and copy-ready.
- Add a GETTING_STARTED.md guide at `.ai/bootstrap/` explaining how to use the bootstrap.

Out of scope / non-goals:
- Changes to the main repo's workflow files (AGENTS.md, CLAUDE.md, role definitions, templates).
- Changing the bootstrap directory path or naming convention.

## Assumptions
- The bootstrap directory is intended to be copied verbatim into a new repository.
- Project-specific commands (lint, test, security) should be `<placeholder>` values in bootstrap
  files, replaced by the adopting repo.
- The `validate_pr.py` script in the bootstrap is a copy of the main repo's script, extended
  with additional common dependency file exemptions.

## Proposed behavior / API
The bootstrap directory after this change contains:

### Root-level files
- `AGENTS.md` — synced with current root AGENTS.md; command placeholders substituted.
- `CLAUDE.md` — new template with project command and architecture placeholders.
- `10Rules.md` — copy of current root `10Rules.md`.
- `CHANGELOG.md` — minimal starter.
- `README.md` — updated to describe the full structure.
- `validator-expectations.md` — updated to document what the script enforces and how to adapt it.

### `.ai/` additions
- `.ai/roles/` — all five role files (Spec Writer, Orchestrator, Implementer, Tester, Reviewer).
  Roles 02 and 03 use `<lint command>` / `<test command>` placeholders.
- `.ai/templates/spec_template.md` — adds Security considerations section.
- `.ai/templates/pr_draft_template.md` — adds Security Review section and GitHub Checks;
  commands changed to placeholders.
- `.ai/templates/pr_description_template.md` — same additions as pr_draft_template.
- `.ai/templates/review_checklist.md` — expanded Security section matching current main repo.
- `.ai/pr-description/.gitkeep` — directory placeholder.

### `docs/` additions
- `docs/test-plans/README.md` — convention guide for the test-plans folder.

### `log/` addition
- `log/.gitkeep` — directory placeholder.

### `.github/` additions
- `.github/CODEOWNERS` — placeholder username.
- `.github/PULL_REQUEST_TEMPLATE.md` — command placeholders substituted.
- `.github/dependabot.yml` — covers pip and github-actions; commented for other ecosystems.
- `.github/scripts/validate_pr.py` — copy of the main repo script plus additional
  `DEPENDABOT_ALLOWED_ROOT_FILES` entries for Node, Rust, and Go.
- `.github/workflows/ci.yml` — generic CI template with language-agnostic placeholders.

### New guide
- `GETTING_STARTED.md` (at `.ai/bootstrap/`) — nine-step setup guide with a full file reference
  table and a "what not to change" section.

## Acceptance criteria
- AC1: The bootstrap directory contains all files listed in the Proposed behavior section.
- AC2: `AGENTS.md` in the bootstrap matches the current root `AGENTS.md` structure, with
  `<lint command>`, `<test command>`, and `<security command>` replacing specific commands.
- AC3: All five role files are present in `.ai/roles/` with correct content.
- AC4: All four templates (spec, pr_draft, pr_description, review_checklist) include the Security
  considerations / Security review sections present in the main repo's templates.
- AC5: `GETTING_STARTED.md` exists at `.ai/bootstrap/` and covers all setup steps.
- AC6: `validate_pr.py` in the bootstrap is functionally equivalent to the main repo's script.

## Security considerations
- Auth/authz impact: None.
- Input handling or injection risk: None (documentation and template files only).
- Secrets or credential handling: None.
- Data exposure or privacy impact: None.
- File system access impact: None.
- Network or external service impact: None.
- Dependency or supply-chain impact: None.
- Security notes: No meaningful security impact.

## Edge cases
- The bootstrap `validate_pr.py` is a copy of the main repo's script; they may diverge over time.
  The validator-expectations.md notes this explicitly.
- The `ci.yml` template uses placeholder echo commands; a new repo must replace them before CI
  is functional.

## Test guidance
- AC1 -> `test_bootstrap_files_present`
- AC2 -> `test_bootstrap_agents_has_placeholders`
- AC3 -> `test_bootstrap_role_files_present`
- AC4 -> `test_bootstrap_templates_have_security_sections`
- AC5 -> `test_getting_started_exists`
- AC6 -> `test_bootstrap_validate_pr_functions_present`

## Decision log
- 2026-05-20: Used `<placeholder>` syntax for all project-specific commands to be consistent
  with the existing AGENTS.md bootstrap convention.
- 2026-05-20: Added extra `DEPENDABOT_ALLOWED_ROOT_FILES` entries (Node, Rust, Go) to the
  bootstrap validate_pr.py since the bootstrap serves non-Python projects too.
