# Filelock and Virtualenv Security Bump

**Spec file:** `docs/specs/12-filelock-virtualenv-security-bump.md`  
**Spec slug:** filelock-virtualenv-security-bump  
**Status:** Done  
**Owner:** DTidey  
**Date:** 2026-10-29  

## Problem statement
- `make security` fails on `main`. pip-audit reports new advisories against two dev-lock
  dependencies: filelock 3.24.3 (nine advisories, including CVE-2026-112940 and CVE-2026-112936)
  and virtualenv 21.14.9 (CVE-2026-113713).
- CI's Security step fails as a result, which blocks Dependabot PR #55 (ruff 0.17.2). Its own
  bump is unrelated to the failure.

## Scope
In scope:
- Raising the two vulnerable pins to their minimum fixed versions.

Out of scope / non-goals:
- Other dependency upgrades, including the pending Dependabot bump.

## Assumptions
- The pip-audit advisory database as of 2026-10-29.
- These are dev-only tooling dependencies, so the test suite, lint and pre-commit cover the risk.

## Proposed behavior / API
### Public interface
- `requirements-dev.txt`: raised pins.
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
- AC2: Only these pins change in `requirements-dev.txt`: filelock 3.24.3 -> 4.2.1 and virtualenv
  21.14.9 -> 21.14.10. `requirements.txt` and the `.in` files are unchanged.
- AC3: `make lint` and `make test` pass with the new versions installed via `make sync`.

## Security considerations
- Auth/authz impact: None.
- Input handling or injection risk: None.
- Secrets or credential handling: None.
- Data exposure or privacy impact: None.
- File system access impact: None.
- Network or external service impact: None.
- Dependency or supply-chain impact: Removes ten known advisories. No new dependencies; filelock
  is an existing transitive dependency (via virtualenv, cachecontrol and python-discovery).
- Security notes for reviewers/testers: Re-run pip-audit without ignores on both lock files.

## Edge cases
- A major-version bump of a transitive dependency: filelock 3 -> 4. Every dependent must accept
  4.x: virtualenv 21.14.10 requires `filelock>=3.24.2,<5`, cachecontrol `>=3.8.0`, python-discovery
  `>=3.16.1`.
- An intermediate fix version still vulnerable: filelock 4.0.9 fixes only CVE-2026-112936; the
  other eight advisories need 4.2.1.

## Test guidance
- AC1 -> `make security`;
  `tests/test_security_workflow_docs.py::test_makefile_and_ci_wire_security_automation`
- AC2 -> `git diff main -- requirements*.txt requirements*.in`
- AC3 -> `make lint`, `make test`

## Decision log
- 2026-10-29: Pinned the minimum fixed versions (filelock 4.2.1, virtualenv 21.14.10), not the
  latest (4.2.4, 21.15.1) that an unconstrained `--upgrade-package` selects. Both clear pip-audit;
  the minimum keeps the change surgical.
- 2026-10-29: Accepted the filelock 3 -> 4 major bump. No 3.x release fixes the advisories, and
  all three dependents declare compatibility with 4.x.
