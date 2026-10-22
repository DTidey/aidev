# 2026-10-22: Certifi and virtualenv security bump (packet 11)

- **Why Dependabot PRs failed.** Two separate causes. CI's Security step failed because new
  advisories against certifi and virtualenv on `main` were published after 2026-10-14, which is
  also why the earlier pip-tools PR (#50) passed. The auto-manage job failed because the
  repository's "Allow auto-merge" setting is off. It last succeeded on 2026-10-07, so the setting
  was probably turned off during the 2026-10-10 branch-protection work. It is a GitHub setting,
  so this packet does not change it.
- **virtualenv 21.14.9, not 21.14.7.** CI reported 21.14.7 as the fix, but pip-audit on 21.14.7
  surfaced a second advisory (CVE-2026-113722) that only 21.14.9 fixes.
- **Targeted re-pins.** `--upgrade-package` keeps unrelated pins unchanged, so the pending
  Dependabot PRs still merge cleanly on top.
