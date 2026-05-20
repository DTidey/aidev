# Spec-First Repo Bootstrap

This directory is a copy-ready starter kit for adopting the spec-first, multi-agent workflow in a
new repository.

See `../GETTING_STARTED.md` for step-by-step setup instructions.

## Files included

### Root-level files (copy to repo root)

| File | Purpose |
|---|---|
| `AGENTS.md` | Workflow rules and non-negotiable constraints; customize command placeholders |
| `CLAUDE.md` | Per-session project context for Claude Code; fill in commands and architecture |
| `10Rules.md` | Ten coding principles for all agents; copy unchanged |
| `CHANGELOG.md` | Release history starter; add your project name |

### AI workflow files

| Path | Purpose |
|---|---|
| `.ai/templates/spec_template.md` | Template for specs |
| `.ai/templates/test_plan_template.md` | Template for test plans |
| `.ai/templates/pr_draft_template.md` | Template for PR draft artifacts |
| `.ai/templates/pr_description_template.md` | Template for PR descriptions |
| `.ai/templates/review_checklist.md` | Checklist used during code review |
| `.ai/roles/00_spec_writer.md` | Spec Writer role instructions |
| `.ai/roles/01_orchestrator.md` | Orchestrator role instructions |
| `.ai/roles/02_implementer.md` | Implementer role instructions |
| `.ai/roles/03_tester.md` | Tester role instructions |
| `.ai/roles/04_reviewer.md` | Reviewer role instructions |
| `.ai/pr-description/.gitkeep` | Placeholder; PR draft artifacts land here |

### Docs

| Path | Purpose |
|---|---|
| `docs/specs/README.md` | Convention guide for the specs folder |
| `docs/test-plans/README.md` | Convention guide for the test-plans folder |
| `log/.gitkeep` | Placeholder; decision logs land here |

### GitHub configuration

| Path | Purpose |
|---|---|
| `.github/CODEOWNERS` | Review ownership; replace the placeholder username |
| `.github/PULL_REQUEST_TEMPLATE.md` | PR template; replace command placeholders |
| `.github/dependabot.yml` | Automated dependency updates; adjust ecosystems |
| `.github/scripts/validate_pr.py` | CI script that enforces the workflow; do not move |
| `.github/workflows/ci.yml` | CI pipeline template; add project-specific build steps |

## After copying

1. Replace every `<placeholder>` in `AGENTS.md`, `CLAUDE.md`, `.ai/roles/02_implementer.md`,
   `.ai/roles/03_tester.md`, `.github/PULL_REQUEST_TEMPLATE.md`, and `.github/workflows/ci.yml`.
2. Edit `.github/CODEOWNERS` to name your team.
3. Edit `.github/dependabot.yml` to match your package ecosystems.
4. Enable branch protection on `main` requiring the status check names you chose.
5. Create your first spec at `docs/specs/01-<slug>.md` using `.ai/templates/spec_template.md`.
