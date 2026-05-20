# Getting Started with the Spec-First Workflow

This guide explains how to bootstrap a new repository using the spec-first, multi-agent workflow
defined in `spec-first-repo/`.

## What you get

A structured, spec-driven development workflow where:

- Every code change begins with a written spec (the source of truth)
- Five roles (Spec Writer, Orchestrator, Implementer, Tester, Reviewer) each have clear,
  bounded responsibilities
- Numbered "packets" link a spec, test plan, and PR draft to every change
- CI automatically validates that PRs follow the process

## Step 1: Copy the bootstrap directory

Copy the entire `spec-first-repo/` directory into the root of your new repository. The files are
designed to land at the paths they currently occupy:

```bash
cp -r .ai/bootstrap/spec-first-repo/. /path/to/your-new-repo/
```

This creates the following structure in your new repo:

```
AGENTS.md                        ← workflow rules (edit to add your commands)
CLAUDE.md                        ← Claude Code guidance (edit to describe your project)
10Rules.md                       ← coding principles for all agents
CHANGELOG.md                     ← release history (starts empty under ## Unreleased)
.ai/
  templates/                     ← spec, test-plan, PR draft, review templates
  roles/                         ← role definitions for each workflow stage
  pr-description/                ← PR draft artifacts land here (one per change packet)
docs/
  specs/                         ← specs land here (one per change packet)
  test-plans/                    ← test plans land here (one per change packet)
log/                             ← decision logs land here (changelog-YYYY-MM-DD.md)
.github/
  CODEOWNERS                     ← review ownership
  PULL_REQUEST_TEMPLATE.md       ← PR template enforcing the workflow
  dependabot.yml                 ← automated dependency updates
  scripts/validate_pr.py         ← CI script that enforces the workflow
  workflows/ci.yml               ← CI pipeline template
```

## Step 2: Customize AGENTS.md

`AGENTS.md` is the primary workflow contract read by AI agents and humans alike. Replace all
`<placeholder>` values:

| Placeholder | Replace with |
|---|---|
| `<lint command>` | Your project's lint command (e.g. `npm run lint`, `make lint`, `cargo clippy`) |
| `<test command>` | Your project's test command (e.g. `npm test`, `pytest`, `cargo test`) |
| `<security command>` | Your security scan command, or remove the line if not applicable |
| `<CI test job name>` | The exact GitHub Actions job name for tests (e.g. `CI / test`) |
| `<CodeQL job name>` | Your SAST/CodeQL job name, or remove if not applicable |

## Step 3: Customize CLAUDE.md

`CLAUDE.md` is read by Claude Code at the start of every session. It must describe your project
accurately.

- Under `## Commands`: fill in your actual setup, lint, test, and security commands
- Under `## Architecture`: describe your project's purpose and structure
- Under `## Tooling`: add language version, formatter, linter, and dependency management details

## Step 4: Customize the role files

Open each file in `.ai/roles/` and replace `<lint command>` and `<test command>` with your
project's actual commands. These files are the instructions that AI agents (or humans) follow at
each workflow stage.

## Step 5: Configure GitHub

### Branch protection

On GitHub, go to **Settings → Branches → Add rule** for `main`:

- Require a pull request before merging
- Require status checks to pass before merging (add the exact job names you set in Step 2)
- Dismiss stale pull request approvals when new commits are pushed
- Do not allow force pushes
- Do not allow branch deletion

### CODEOWNERS

Edit `.github/CODEOWNERS` and replace `@your-github-username` with your GitHub username or team.

### Dependabot

Review `.github/dependabot.yml`. Update the `package-ecosystem` entries to match your project:

- Python → `pip`
- Node.js → `npm`
- Rust → `cargo`
- Go → `gomod`
- Java → `gradle` or `maven`

Remove ecosystems that do not apply. The `github-actions` entry should stay unless you have
a reason to remove it.

## Step 6: Set up CI

Edit `.github/workflows/ci.yml`. The file contains placeholder comments marking where to add
your project's language setup, install, lint, and test steps.

The validate-PR step runs `python .github/scripts/validate_pr.py` and must stay. It requires
only the Python standard library, so a plain `actions/setup-python` step is sufficient even for
non-Python projects.

`validate_pr.py` enforces:

- PR body is non-empty
- Code-changing PRs link a spec under `docs/specs/`
- The linked spec was modified in the PR
- Every AC defined in the spec is checked in the PR body
- Matching test plan and PR draft exist, were updated, and check the same ACs
- Dependabot dependency-only PRs are exempted automatically

If you want CodeQL analysis, create a separate workflow file following the GitHub documentation.

## Step 7: Set up PULL_REQUEST_TEMPLATE.md

The included `.github/PULL_REQUEST_TEMPLATE.md` contains placeholder commands. Replace the lint,
test, and security command placeholders in the Testing section with your actual commands.

## Step 8: Initialize your CHANGELOG

Edit `CHANGELOG.md` and add your project name. The workflow accumulates unreleased work under
`## Unreleased` until you explicitly cut a release.

## Step 9: Start your first workflow

Every code change follows the five-role workflow defined in `AGENTS.md`:

1. **Spec Writer**: create `docs/specs/01-your-change.md` from `.ai/templates/spec_template.md`
2. **Orchestrator**: review the spec and break it into a task checklist
3. **Implementer**: write code strictly against the acceptance criteria
4. **Tester**: write tests and `docs/test-plans/01-your-change.md`
5. **Reviewer**: review against the spec; raise blockers where needed
6. **Orchestrator**: approve merge when CI is green and all ACs are satisfied

Use packet number `01` for your first change. Each subsequent change increments the prefix
(`02`, `03`, ...).

Before opening the PR, create `.ai/pr-description/01-your-change.md` from
`.ai/templates/pr_draft_template.md`. The PR validator checks that this file exists and checks
the same ACs as the PR body.

## File reference

| File / Directory | Purpose |
|---|---|
| `AGENTS.md` | Workflow rules and non-negotiable constraints for AI agents |
| `CLAUDE.md` | Per-session project context for Claude Code |
| `10Rules.md` | Ten coding principles enforced across all roles |
| `.ai/templates/spec_template.md` | Template for writing specs |
| `.ai/templates/test_plan_template.md` | Template for writing test plans |
| `.ai/templates/pr_draft_template.md` | Template for PR draft artifacts |
| `.ai/templates/review_checklist.md` | Checklist used during code review |
| `.ai/roles/00_spec_writer.md` | Instructions for the Spec Writer role |
| `.ai/roles/01_orchestrator.md` | Instructions for the Orchestrator role |
| `.ai/roles/02_implementer.md` | Instructions for the Implementer role |
| `.ai/roles/03_tester.md` | Instructions for the Tester role |
| `.ai/roles/04_reviewer.md` | Instructions for the Reviewer role |
| `docs/specs/` | Source-of-truth specs, one per change packet |
| `docs/test-plans/` | Test plans aligned to each spec packet |
| `.ai/pr-description/` | PR draft artifacts aligned to each spec packet |
| `log/` | Decision logs named `changelog-YYYY-MM-DD.md` |
| `.github/scripts/validate_pr.py` | CI enforcement script (do not rename or move) |
| `.github/workflows/ci.yml` | CI pipeline (customize for your language/toolchain) |

## What not to change

- **Do not rename or move `.github/scripts/validate_pr.py`**. The CI workflow references it by
  path, and the script's logic assumes the repo structure defined above.
- **Do not change the packet naming convention** (`<nn>-<slug>.md`). The validator enforces
  the two-digit prefix and derives companion artifact paths from it.
- **Do not remove the PR template**. The validate_pr.py script reads the PR body against
  the template's AC-checking convention (`- [x] AC1 ...`).
