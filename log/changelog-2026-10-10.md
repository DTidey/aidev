# 2026-10-10: Dependency security bumps (packet 10)

- **The CVE-2026-4539 ignore was removed, not renewed.** Packet 02 added it because pygments had
  no fix; 2.20.0 now has one. Keeping it would hide an advisory that can be fixed.
- **The test asserts no ignores at all.** The old test asserted the ignore existed, which would
  have failed this fix and pushed toward keeping it. Exceptions should now be deliberate.
- **`make sync` upgrades pip-tools with pip.** aidev's pip-tools (7.6.1) works with pip 26.2
  today, but the same gap broke meridian-capital's sync when pip moved ahead of a pinned
  pip-tools.
- **The Markdown exclusion for ruff was left out.** Ruff 0.16.10 passes on aidev's docs, so
  adding it would be speculative; meridian-capital needed it because its specs have Python
  examples.
