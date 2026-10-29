# Test Plan: filelock-virtualenv-security-bump

Path: `docs/test-plans/12-filelock-virtualenv-security-bump.md`

## What changed
- Two vulnerable dev-lock pins raised to their minimum fixed versions: filelock 4.2.1 and
  virtualenv 21.14.10.

## Acceptance criteria coverage
- AC1: `make security` outputs "No known vulnerabilities found" with no ignores.
  `tests/test_security_workflow_docs.py::test_makefile_and_ci_wire_security_automation` still
  asserts the Makefile has no `--ignore-vuln`.
- AC2: `git diff main -- requirements.txt requirements-dev.txt requirements.in
  requirements-dev.in` shows only the two listed pins.
- AC3: `make lint` (89 files) and `make test` (47 passed).

## Edge cases
- From spec:
  - filelock 3 -> 4 major bump: virtualenv 21.14.10 (`>=3.24.2,<5`), cachecontrol (`>=3.8.0`) and
    python-discovery (`>=3.16.1`) all accept 4.2.1, confirmed from package metadata
  - filelock 4.0.9 still vulnerable to eight advisories, so the pin goes to 4.2.1
- Additional adversarial cases:
  - `pip check` on the synced venv: no broken requirements
  - filelock 4 in use: `virtualenv` creates a working new environment, a `FileLock`
    acquire/release round trip succeeds, and `pre-commit clean && pre-commit run --all-files`
    rebuilds its hook environments and passes
  - The lock merged with Dependabot PR #55 (ruff 0.17.2): the merge is clean, pip-audit finds no
    vulnerabilities, and ruff 0.17.2 `check` and `format --check` pass on the repo

## Notes
- Flaky risks: new advisories can appear at any time.
- Determinism considerations: none.

## Commands
```bash
make sync
make security
make lint
make test
make precommit
```
