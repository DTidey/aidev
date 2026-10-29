# 2026-10-29: Filelock and virtualenv security bump (packet 12)

- **Why Dependabot PR #55 failed.** Not the ruff bump: new advisories against filelock 3.24.3 and
  virtualenv 21.14.9 were published after packet 11 landed, so `make security` fails on `main`.
  More filelock advisories appeared between #55's CI run (4) and the local check (9).
- **Minimum fixed versions, not latest.** An unconstrained `--upgrade-package` picked filelock
  4.2.4 and virtualenv 21.15.1. The minimums (4.2.1, 21.14.10) clear pip-audit, so they were pinned
  explicitly to keep the change surgical.
- **filelock major bump accepted.** No 3.x release fixes the advisories. virtualenv, cachecontrol
  and python-discovery all allow 4.x, and virtualenv, pre-commit and a FileLock round trip were
  exercised against 4.2.1.
