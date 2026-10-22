## Summary

- Fixes `make security`, which fails on `main` because of new advisories. That failure blocks CI
  on Dependabot PRs #52 (ruff) and #53 (pre-commit). Raises certifi to 2026.10.19 and virtualenv
  to 21.14.9, plus distlib and packaging, which virtualenv 21.14.9 requires.
- virtualenv goes to 21.14.9, not 21.14.7: 21.14.7 still has CVE-2026-113722.

## Spec

- Spec: `docs/specs/11-certifi-virtualenv-security-bump.md`
- Test plan: `docs/test-plans/11-certifi-virtualenv-security-bump.md`
- PR draft path: `.ai/pr-description/11-certifi-virtualenv-security-bump.md`

## Acceptance Criteria

- [x] AC1: `make security` passes with no `--ignore-vuln` exceptions.
- [x] AC2: Only the four listed dev-lock pins change; `requirements.txt` and `.in` files unchanged.
- [x] AC3: `make lint` and `make test` pass with the new versions installed.

## Security Review

- [x] Security considerations reviewed in `docs/specs/11-certifi-virtualenv-security-bump.md`
- [x] Removes three known advisories; no new dependencies

## Validation

- `make sync`: pass; `pip check`: no broken requirements
- `make security`: No known vulnerabilities found (no ignores)
- `make lint`: pass
- `make test`: 47 passed
- Lock merged with #52 and #53: clean merge, pip-audit clean, ruff 0.17.1 check and format pass

Open risks: the Dependabot auto-manage job will keep failing until "Allow auto-merge" is enabled
in the repository settings. After merge, #52 and #53 need a rebase (`@dependabot rebase`).
