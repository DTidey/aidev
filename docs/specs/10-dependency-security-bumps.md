# Dependency Security Bumps

**Spec file:** `docs/specs/10-dependency-security-bumps.md`  
**Spec slug:** dependency-security-bumps  
**Status:** Done  
**Owner:** DTidey  
**Date:** 2026-10-10  

## Problem statement
- `make security` fails on `main`. pip-audit reports advisories against four dev-lock
  dependencies: msgpack 1.1.2, pygments 2.19.2, urllib3 2.7.0 and virtualenv 20.38.0.
- CI's Security step fails as a result, which stops the Test step and blocks PR #47.
- The Makefile still ignores CVE-2026-4539 (pygments). It was added in packet 02 as a temporary
  exception "until an upstream fix is available"; pygments 2.20.0 now fixes it.
- `make sync` upgrades pip but not pip-tools. A pip release that breaks the pinned pip-tools
  breaks `make sync`, which happened downstream in DTidey/meridian-capital (its packet 11).

## Scope
In scope:
- Raising the four vulnerable pins, plus python-discovery, which virtualenv 21 requires.
- Removing the CVE-2026-4539 ignore and its docs, and asserting that no ignore exists.
- `make sync` upgrading pip-tools alongside pip.

Out of scope / non-goals:
- Other dependency upgrades.
- Excluding Markdown from ruff: ruff 0.16.10 passes on aidev's current docs.
- Branch protection settings, which are configured in GitHub.

## Assumptions
- The pip-audit advisory database as of 2026-10-10.
- These are dev-only tooling dependencies, so the test suite and lint cover the risk.

## Proposed behavior / API
### Public interface
- `Makefile`: the `sync` target also upgrades pip-tools; the `security` target has no
  `--ignore-vuln`.
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
- AC2: Only these pins change in `requirements-dev.txt`: msgpack 1.1.2 -> 1.2.3, pygments
  2.19.2 -> 2.21.0, urllib3 2.7.0 -> 2.8.0, virtualenv 20.38.0 -> 21.14.5, plus python-discovery
  1.6.2 (new, required by virtualenv 21). `requirements.txt` and the `.in` files are unchanged.
- AC3: `make sync` upgrades pip-tools together with pip, setuptools and wheel.
- AC4: `CLAUDE.md` and `README.md` no longer describe the removed ignore. A test asserts the
  Makefile contains no `--ignore-vuln`.
- AC5: `make lint` and `make test` pass with the new versions installed via `make sync`.

## Security considerations
- Auth/authz impact: None.
- Input handling or injection risk: None.
- Secrets or credential handling: None.
- Data exposure or privacy impact: None.
- File system access impact: None.
- Network or external service impact: None.
- Dependency or supply-chain impact: Removes five known advisories, including one that was being
  ignored. No new direct dependencies; python-discovery is a new transitive dependency of
  virtualenv 21.
- Security notes for reviewers/testers: Re-run pip-audit without ignores on both lock files.

## Edge cases
- A package needing a dependency bumped too: virtualenv 21 requires python-discovery.
- A future advisory without a fix: adding an ignore now needs a deliberate test change.

## Test guidance
- AC1 -> `make security`
- AC2 -> `git diff main -- requirements*.txt requirements*.in`
- AC3 -> `Makefile` review; `make sync` on the previously synced venv
- AC4 -> `tests/test_security_workflow_docs.py::test_makefile_and_ci_wire_security_automation`;
  `grep -rn CVE-2026-4539` limited to historical packet 02 docs
- AC5 -> `make lint`, `make test`

## Decision log
- 2026-10-10: Removed the CVE-2026-4539 ignore instead of keeping it. Packet 02 made it
  conditional on an upstream fix, which now exists.
- 2026-10-10: The test now asserts there is no `--ignore-vuln` at all, rather than one specific
  ignore. Exceptions should be deliberate and visible, not leftovers.
- 2026-10-10: The Markdown exclusion for ruff (added downstream in meridian packet 15) was left
  out; it isn't needed yet, and adding it now would be speculative.
