## Summary

- Fixes `make security`, which has failed on `main` and blocks CI (including PR #47). Raises
  msgpack, pygments, urllib3 and virtualenv to fixed versions, plus python-discovery, which
  virtualenv 21 requires.
- Removes the temporary `--ignore-vuln CVE-2026-4539` (pygments) from packet 02. Its condition,
  an upstream fix, is now met. The test now asserts the Makefile has no ignores at all, and the
  stale notes in `CLAUDE.md` and `README.md` are removed.
- `make sync` now upgrades pip-tools alongside pip, so a pip release can't strand an
  incompatible pip-tools. This upstreams DTidey/meridian-capital packet 11.

## Spec

- Spec: `docs/specs/10-dependency-security-bumps.md`
- Test plan: `docs/test-plans/10-dependency-security-bumps.md`
- PR draft path: `.ai/pr-description/10-dependency-security-bumps.md`

## Acceptance Criteria

- [x] AC1: `make security` passes with no `--ignore-vuln` exceptions.
- [x] AC2: Only the listed dev-lock pins change; `requirements.txt` and `.in` files unchanged.
- [x] AC3: `make sync` upgrades pip-tools together with pip.
- [x] AC4: Stale ignore docs removed; a test asserts there are no ignores.
- [x] AC5: `make lint` and `make test` pass with the new versions installed.

## Security Review

- [x] Security considerations reviewed in `docs/specs/10-dependency-security-bumps.md`
- [x] Removes five known advisories, including one previously ignored

## Validation

- `make sync`: pass
- `make security`: No known vulnerabilities found (no ignores)
- `make lint`: pass (ruff 0.16.10)
- `make test`: 41 passed
- Reintroducing an ignore fails the security-workflow test

Open risks: none. After merge, PR #47 needs a rebase, with a small conflict in `log/` and
`CHANGELOG.md`.
