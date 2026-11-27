# 2026-11-27: Virtualenv security bump (packet 13)

- **Why Dependabot PRs #61 and #62 failed.** Not the ruff or pip-tools bumps: a new advisory
  (PYSEC-2026-4402) against virtualenv 21.14.10 was published after packet 12 landed, so
  `make security` fails on `main`.
- **Minimum fixed version, not latest.** Pinned 21.14.13 explicitly with
  `pip-compile --upgrade-package virtualenv==21.14.13`. It clears pip-audit and keeps the change
  surgical; pip-compile changed no transitive pins because the existing ones already satisfy it.
- **Verified outside the shared `.venv`.** The worktree's `.venv` is a symlink to the main
  checkout, so all checks ran in a throwaway venv under `/tmp/aidev-p13-venv` instead.
