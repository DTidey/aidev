# Spec-First Repo Bootstrap

This folder is a copy-ready starter kit for adopting the spec-first workflow in a new repository.

## Intended Target Layout

Copy these files into a target repo at the same paths:

- `AGENTS.md`
- `docs/specs/README.md`
- `.ai/templates/spec_template.md`
- `.ai/templates/test_plan_template.md`
- `.ai/templates/pr_draft_template.md`
- `.ai/templates/pr_description_template.md`
- `.ai/templates/review_checklist.md`

Use these optional guidance files while setting up automation:

- `.ai/bootstrap/spec-first-repo/validator-expectations.md`

## After Copying

1. Replace placeholder commands in `AGENTS.md`.
2. Decide whether the repo uses numbered packets such as `<nn>-<slug>.md`.
3. Add CI or local validation for spec links, acceptance criteria, and companion artifacts.
4. If needed, add repo-specific workflow details that override the default process.

## Notes

- This starter assumes a spec-first workflow where specs are the source of truth.
- Keep repo-local rules authoritative if they differ from the global skill defaults.
- Prefer small, reviewable PRs with matching spec, test-plan, and PR-draft artifacts.
