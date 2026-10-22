# Certifi and Virtualenv Security Bump

**Spec file:** `docs/specs/11-certifi-virtualenv-security-bump.md`  
**Spec slug:** certifi-virtualenv-security-bump  
**Status:** Done  
**Owner:** DTidey  
**Date:** 2026-10-22  

## Problem statement
- `make security` fails on `main`. pip-audit reports new advisories against two dev-lock
  dependencies: certifi 2026.2.25 (PYSEC-2026-4320) and virtualenv 21.14.5 (CVE-2026-113725,
  CVE-2026-113722).
- CI's Security step fails as a result, which blocks Dependabot PRs #52 (ruff) and #53
  (pre-commit). Their own bumps are unrelated to the failure.

## Scope
In scope:
- Raising the two vulnerable pins, plus distlib and packaging, which virtualenv 21.14.9 requires.

Out of scope / non-goals:
- Other dependency upgrades, including the pending Dependabot bumps.
- The `Auto-manage Dependabot PRs` failure ("Auto merge is not allowed for this repository"),
  which is a GitHub repository setting, not a code change.

## Assumptions
- The pip-audit advisory database as of 2026-10-22.
- These are dev-only tooling dependencies, so the test suite and lint cover the risk.

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
- AC2: Only these pins change in `requirements-dev.txt`: certifi 2026.2.25 -> 2026.10.19,
  virtualenv 21.14.5 -> 21.14.9, distlib 0.4.0 -> 0.4.4 and packaging 26.0 -> 26.3 (both required
  by virtualenv 21.14.9). `requirements.txt` and the `.in` files are unchanged.
- AC3: `make lint` and `make test` pass with the new versions installed via `make sync`.

## Security considerations
- Auth/authz impact: None.
- Input handling or injection risk: None.
- Secrets or credential handling: None.
- Data exposure or privacy impact: None.
- File system access impact: None.
- Network or external service impact: None.
- Dependency or supply-chain impact: Removes three known advisories. No new dependencies;
  distlib and packaging are existing transitive dependencies raised to satisfy virtualenv.
- Security notes for reviewers/testers: Re-run pip-audit without ignores on both lock files.

## Edge cases
- An intermediate fix version still vulnerable: virtualenv 21.14.7 fixes CVE-2026-113725 but not
  CVE-2026-113722, so the pin goes to 21.14.9.
- A package needing a dependency bumped too: virtualenv 21.14.9 requires distlib >= 0.4.3 and
  packaging >= 26.3.

## Test guidance
- AC1 -> `make security`;
  `tests/test_security_workflow_docs.py::test_makefile_and_ci_wire_security_automation`
- AC2 -> `git diff main -- requirements*.txt requirements*.in`
- AC3 -> `make lint`, `make test`

## Decision log
- 2026-10-22: Pinned virtualenv to 21.14.9, not 21.14.7 (the fix version first reported).
  pip-audit on 21.14.7 reports CVE-2026-113722.
- 2026-10-22: Used targeted `--upgrade-package` re-pins instead of a full `pip-compile --upgrade`,
  so unrelated pins stay put and Dependabot's pending PRs stay small.
