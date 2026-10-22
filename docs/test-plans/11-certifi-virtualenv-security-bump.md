# Test Plan: certifi-virtualenv-security-bump

Path: `docs/test-plans/11-certifi-virtualenv-security-bump.md`

## What changed
- Two vulnerable dev-lock pins raised (certifi, virtualenv), plus distlib and packaging, which
  virtualenv 21.14.9 requires.

## Acceptance criteria coverage
- AC1: `make security` outputs "No known vulnerabilities found" with no ignores.
  `tests/test_security_workflow_docs.py::test_makefile_and_ci_wire_security_automation` still
  asserts the Makefile has no `--ignore-vuln`.
- AC2: `git diff main -- requirements.txt requirements-dev.txt requirements.in
  requirements-dev.in` shows only the four listed pins.
- AC3: `make lint` (85 files) and `make test` (47 passed).

## Edge cases
- From spec:
  - virtualenv 21.14.7 still vulnerable: pip-audit reported CVE-2026-113722, so the pin goes to
    21.14.9
  - virtualenv 21.14.9 requires distlib >= 0.4.3 and packaging >= 26.3: resolved by pip-compile
    and confirmed from the installed package metadata
- Additional adversarial cases:
  - `pip check` on the synced venv: no broken requirements
  - The lock merged with Dependabot PRs #52 (ruff 0.17.1) and #53 (pre-commit 4.7.0): both merge
    cleanly and pip-audit finds no vulnerabilities
  - ruff 0.17.1 on the repo: `ruff check` and `ruff format --check` pass, so #52 will not fail
    lint after this lands

## Notes
- Flaky risks: new advisories can appear at any time.
- Determinism considerations: none.

## Commands
```bash
make sync
make security
make lint
make test
```
