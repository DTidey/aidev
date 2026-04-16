# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# One-time setup
make venv       # create .venv
make compile    # pin requirements via pip-tools
make sync       # install all dependencies into .venv

# Daily workflow
make lint       # ruff check + ruff format --check
make test       # pytest (tests/ directory)
make security   # bandit on .github/scripts + pip-audit on requirements files
make precommit  # run all pre-commit hooks against every file
```

Run a single test:
```bash
. .venv/bin/activate && pytest tests/test_foo.py::test_bar -q
```

## Architecture

This repository is a **spec-first, multi-agent workflow framework**. It contains no application code — its purpose is to define and enforce a structured process for AI agents collaborating on code changes.

### Numbered packet system

Every change is tracked as a numbered "packet" with a shared two-digit prefix, e.g. `07`:

| Artifact | Path |
|---|---|
| Spec | `docs/specs/07-my-change.md` |
| Test plan | `docs/test-plans/07-my-change.md` |
| PR draft | `.ai/pr-description/07-my-change.md` |

The prefix is assigned sequentially and never renumbered. All three artifacts for a packet must share the exact `<nn>-<slug>` filename stem. Use the next available prefix (check existing files in `docs/specs/` — currently the highest is `06`).

### Five-role workflow

Roles are defined in `.ai/roles/` and must be executed in order:

1. **Spec Writer** (`00_spec_writer.md`) — writes `docs/specs/<nn>-<slug>.md` from `.ai/templates/spec_template.md`. No implementation code.
2. **Orchestrator** (`01_orchestrator.md`) — breaks the spec into a task checklist and commit plan. Approves merge only when CI is green and spec matches shipped behavior.
3. **Implementer** (`02_implementer.md`) — writes minimal code strictly against acceptance criteria. Stops and reports `Blocked on:` if the spec is ambiguous.
4. **Tester** (`03_tester.md`) — writes `docs/test-plans/<nn>-<slug>.md` and pytest tests mapped to ACs; adds at least 3 adversarial cases beyond the spec edge cases.
5. **Reviewer** (`04_reviewer.md`) — categorises findings as Blockers / Important / Suggestions; blockers must cite `File: <path:line>`, `AC: <id>`, and a one-sentence reason.

### Acceptance criteria conventions

- Labelled `AC1`, `AC2`, `AC3`, … in the spec.
- Every AC must be testable and mapped to a named test in the test plan.
- PR body and PR draft must check every AC with `- [x] AC1 …` syntax — this is validated automatically.

### CI enforcement

`.github/scripts/validate_pr.py` runs on every PR and enforces:
- PR body is non-empty and links a spec file matching `docs/specs/\d{2}-[a-z0-9][a-z0-9-]*.md`.
- The linked spec was actually modified in the PR (for code-changing PRs).
- Every AC in the linked spec is checked in the PR body.
- Matching test plan and PR draft files exist, were updated, and check the same ACs.
- Exception: Dependabot PRs that only touch dependency files skip spec validation.

Required GitHub status checks before merging to `main`: `CI / test` and `CodeQL / analyze`.

### Blocking and handoff format

When blocked at any role, use exactly:
```
Blocked on: <question>
Affected AC: <AC id(s) or "missing">
Proposed default: <optional>
```

Reviewer blockers additionally require:
```
File: <path:line>
AC: <AC id or "N/A">
Why this blocks merge: <one sentence>
```

### Security

- Every spec that changes code must include a `Security considerations` section (template fields: auth/authz, input handling, secrets, data exposure, file access, network access, dependency impact).
- `make security` runs Bandit against `.github/scripts/` and pip-audit against both requirements files.
- `CVE-2026-4539` (pygments) is intentionally ignored in pip-audit until an upstream fix is available — revisit when upstream guidance changes.

### Tooling

- **Python 3.11**, line length 100, ruff rule sets: `E F I B UP`.
- Pre-commit hooks auto-fix with `ruff check --fix` and `ruff format` on every commit.
- Dependencies managed via `pip-tools`: edit `requirements.in` / `requirements-dev.in`, then `make compile && make sync`.
- Versions in `CHANGELOG.md` use `MAJOR.MINOR.PATCH`; accumulate under `## Unreleased` until a release is explicitly requested.
