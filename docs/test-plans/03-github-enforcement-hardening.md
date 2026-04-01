# Test Plan: GitHub Enforcement Hardening

## Scope
- Add GitHub-native automation for code scanning and dependency updates.
- Align public PR templates and docs with the current security workflow.
- Make branch protection expectations explicit for `main`.

## Acceptance criteria mapping
- AC1: Verify `.github/workflows/codeql.yml` exists and targets `python` and `actions`; verify `.github/dependabot.yml` exists and covers `pip` and GitHub Actions.
- AC2: Verify `.github/CODEOWNERS` exists and `.github/PULL_REQUEST_TEMPLATE.md` includes security review prompts plus `make security`.
- AC3: Verify `README.md` and `AGENTS.md` document the recommended branch protection settings and exact required checks for `main`.
- AC4: Verify static assertions cover CodeQL, Dependabot, `CODEOWNERS`, public PR template alignment, and required check names.

## Test approach
- Use static assertions in `tests/test_security_workflow_docs.py` to validate config presence and expected content.
- Run `make lint`, `make test`, and `make security`.

## Risks to watch
- Workflow job names and documented required check names may drift apart.
- Dependabot intervals or ecosystems may be accidentally narrowed later.
- Public and internal PR templates could diverge again if only one is updated.
