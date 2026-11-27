## Summary

- Fixes `make security`, which fails on `main` because of a new advisory (PYSEC-2026-4402)
  against virtualenv 21.14.10. That failure blocks CI on Dependabot PRs #61 (ruff 0.17.6) and
  #62 (pip-tools 7.7.0). Raises virtualenv to 21.14.13, the minimum fixed version.
- No other pin changes; the existing transitive pins already satisfy virtualenv 21.14.13.

## Spec

- Spec: `docs/specs/13-virtualenv-security-bump.md`
- Test plan: `docs/test-plans/13-virtualenv-security-bump.md`
- PR draft path: `.ai/pr-description/13-virtualenv-security-bump.md`

## Acceptance Criteria

- [x] AC1: `make security` passes with no `--ignore-vuln` exceptions.
- [x] AC2: Only the virtualenv dev-lock pin changes; `requirements.txt` and `.in` files unchanged.
- [x] AC3: `make lint` and `make test` pass with the new version installed.

## Security Review

- [x] Security considerations reviewed in `docs/specs/13-virtualenv-security-bump.md`
- [x] Removes one known advisory; no new dependencies

## Validation

Run in a fresh Python 3.12 venv installed from both lock files:

- `pip check`: no broken requirements
- Security (bandit + pip-audit, no ignores): No known vulnerabilities found
- Lint (`ruff check`, `ruff format --check`): pass, 97 files
- Tests: 47 passed
- `virtualenv` smoke test: new environment created and runs
- Lock merged with #61 and #62: clean three-way merge, pip-audit clean, ruff 0.17.6 check and
  format pass, `pip check` clean with pip-tools 7.7.0

Open risks: after merge, #61 and #62 need a rebase (`@dependabot rebase`).
