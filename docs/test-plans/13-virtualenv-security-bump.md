# Test Plan: virtualenv-security-bump

Path: `docs/test-plans/13-virtualenv-security-bump.md`

## What changed
- One vulnerable dev-lock pin raised to its minimum fixed version: virtualenv 21.14.13.

## Acceptance criteria coverage
- AC1: `make security` outputs "No known vulnerabilities found" with no ignores.
  `tests/test_security_workflow_docs.py::test_makefile_and_ci_wire_security_automation` still
  asserts the Makefile has no `--ignore-vuln`.
- AC2: `git diff main -- requirements.txt requirements-dev.txt requirements.in
  requirements-dev.in` shows only the virtualenv pin.
- AC3: `make lint` (97 files) and `make test` (47 passed).

## Edge cases
- From spec:
  - virtualenv 21.14.13's requirements (distlib, filelock, packaging, platformdirs,
    python-discovery) are met by the existing pins, confirmed from package metadata; pip-compile
    changed no other line
  - The lock merged with Dependabot PRs #61 (ruff 0.17.6) and #62 (pip-tools 7.7.0) stays clean
- Additional adversarial cases:
  - `pip check` on a fresh venv installed from both lock files: no broken requirements
  - virtualenv 21.14.13 in use: `virtualenv` creates a new environment whose interpreter runs
  - Three-way merge (`git merge-file`) of this lock with the #61 and #62 pins: no conflicts;
    pip-audit on the merged lock finds no vulnerabilities, and ruff 0.17.6 `check` and
    `format --check` pass on the repo with pip-tools 7.7.0 installed alongside (`pip check` clean)

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
