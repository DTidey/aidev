# Virtualenv Security Bump

**Spec file:** `docs/specs/13-virtualenv-security-bump.md`  
**Spec slug:** virtualenv-security-bump  
**Status:** Done  
**Owner:** DTidey  
**Date:** 2026-11-27  

## Problem statement
- `make security` fails on `main`. pip-audit reports a new advisory against a dev-lock
  dependency: virtualenv 21.14.10 (PYSEC-2026-4402, fixed in 21.14.13).
- CI's Security step fails as a result, which blocks Dependabot PRs #61 (ruff 0.17.6) and #62
  (pip-tools 7.7.0). Their own bumps are unrelated to the failure.

## Scope
In scope:
- Raising the vulnerable virtualenv pin to its minimum fixed version.

Out of scope / non-goals:
- Other dependency upgrades, including the pending Dependabot bumps.

## Assumptions
- The pip-audit advisory database as of 2026-11-27.
- This is a dev-only tooling dependency, so the test suite, lint and pre-commit cover the risk.

## Proposed behavior / API
### Public interface
- `requirements-dev.txt`: raised pin.
- CLI entry points: none.

### Inputs / outputs
- Inputs: the lock files.
- Outputs: a clean `make security`.
- Error handling: unchanged.

### Examples
```bash
make sync && make security   # No known vulnerabilities found
```

## Acceptance criteria
- AC1: `make security` passes with no `--ignore-vuln` exceptions.
- AC2: Only this pin changes in `requirements-dev.txt`: virtualenv 21.14.10 -> 21.14.13.
  `requirements.txt` and the `.in` files are unchanged.
- AC3: `make lint` and `make test` pass with the new version installed from the lock files.

## Security considerations
- Auth/authz impact: None.
- Input handling or injection risk: None.
- Secrets or credential handling: None.
- Data exposure or privacy impact: None.
- File system access impact: None.
- Network or external service impact: None.
- Dependency or supply-chain impact: Removes one known advisory (PYSEC-2026-4402). No new
  dependencies and no transitive pin changes; virtualenv is an existing transitive dependency
  (via pre-commit).
- Security notes for reviewers/testers: Re-run pip-audit without ignores on both lock files.

## Edge cases
- Transitive requirements of the new version: virtualenv 21.14.13 requires `distlib>=0.4.3,<1`,
  `filelock>=3.24.2,<5`, `packaging>=26.3`, `platformdirs>=4.4,<5` and `python-discovery>=1.6.1`.
  The existing pins already satisfy all of them, so pip-compile changed no other line.
- Interaction with the pending Dependabot bumps: #61 and #62 touch different lines of
  `requirements-dev.txt`, so the lock must merge cleanly and stay audit-clean with them applied.

## Test guidance
- AC1 -> `make security`;
  `tests/test_security_workflow_docs.py::test_makefile_and_ci_wire_security_automation`
- AC2 -> `git diff main -- requirements*.txt requirements*.in`
- AC3 -> `make lint`, `make test`

## Decision log
- 2026-11-27: Pinned the minimum fixed version (21.14.13) via
  `pip-compile --upgrade-package virtualenv==21.14.13`, not the latest. It clears pip-audit and
  keeps the change surgical.
