## Summary

- Fixes `make security`, which fails on `main` because of new advisories. That failure blocks CI
  on Dependabot PR #55 (ruff 0.17.2). Raises filelock to 4.2.1 and virtualenv to 21.14.10, the
  minimum fixed versions.
- filelock is a major bump (3 -> 4); every dependent (virtualenv, cachecontrol, python-discovery)
  declares compatibility with 4.x.

## Spec

- Spec: `docs/specs/12-filelock-virtualenv-security-bump.md`
- Test plan: `docs/test-plans/12-filelock-virtualenv-security-bump.md`
- PR draft path: `.ai/pr-description/12-filelock-virtualenv-security-bump.md`

## Acceptance Criteria

- [x] AC1: `make security` passes with no `--ignore-vuln` exceptions.
- [x] AC2: Only the two listed dev-lock pins change; `requirements.txt` and `.in` files unchanged.
- [x] AC3: `make lint` and `make test` pass with the new versions installed.

## Security Review

- [x] Security considerations reviewed in `docs/specs/12-filelock-virtualenv-security-bump.md`
- [x] Removes ten known advisories; no new dependencies

## Validation

- `make sync`: pass; `pip check`: no broken requirements
- `make security`: No known vulnerabilities found (no ignores)
- `make lint`: pass
- `make test`: 47 passed
- `make precommit` after `pre-commit clean`: pass (hook environments rebuilt with filelock 4)
- Lock merged with #55: clean merge, pip-audit clean, ruff 0.17.2 check and format pass

Open risks: after merge, #55 needs a rebase (`@dependabot rebase`).
