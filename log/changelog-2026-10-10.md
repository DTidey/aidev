# 2026-10-10: Merge 10Rules into AGENTS (packet 09)

- **Why upstream:** DTidey/meridian-capital, built from this framework, found that about a third
  of `10Rules.md` wasn't in `AGENTS.md`, and that Claude Code never loaded `AGENTS.md`. Every
  repo built from the bootstrap kit inherits both gaps, so the fix belongs here.
- **Merge and delete rather than point.** A pointer line still leaves tools that don't follow
  links without a third of the rules.
- **Bootstrap patched rule by rule.** Its wrapping is hand-made (96-99 columns), so regenerating
  it would rewrite unrelated lines. A script applied only the eight changed rules, and a check
  confirmed root/bootstrap differences are the same 21 placeholder lines before and after.
- **Sync test added.** The bootstrap copy had already drifted in form. The test fails if any
  non-placeholder rule in the root is missing from the bootstrap.

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
