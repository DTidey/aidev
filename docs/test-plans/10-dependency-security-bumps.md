# Test Plan: dependency-security-bumps

Path: `docs/test-plans/10-dependency-security-bumps.md`

## What changed
- Four vulnerable dev-lock pins raised (plus python-discovery).
- The CVE-2026-4539 pip-audit ignore removed, and `make sync` upgrades pip-tools.

## Acceptance criteria coverage
- AC1: `make security` outputs "No known vulnerabilities found" with no ignores.
- AC2: `git diff main -- requirements.txt requirements-dev.txt requirements.in
  requirements-dev.in` shows only the listed pins.
- AC3: Makefile review. `make sync` ran successfully on the existing venv and installed the new
  pins.
- AC4: `tests/test_security_workflow_docs.py::test_makefile_and_ci_wire_security_automation`.
  `grep -rn CVE-2026-4539` finds only historical packet 02 docs.
- AC5: `make lint` (ruff 0.16.10, 80 files) and `make test` (41 passed).

## Edge cases
- From spec:
  - virtualenv 21 requires python-discovery: resolved by pip-compile
- Additional adversarial cases:
  - Reintroducing any `--ignore-vuln` makes the security-workflow test fail (verified, then
    restored)
  - pip-audit run without the ignore before the bumps: confirms the ignored pygments advisory
    really was the CVE-2026-4539 alias
  - `make sync` on a venv with a stale ruff (0.15.12) and pip-tools: completes and aligns versions

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
