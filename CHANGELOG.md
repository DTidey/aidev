# Changelog

This file records intentionally published project milestones.

Release policy:
- Development packet numbers like `09-release-changelog-policy` are not release numbers.
- Release versions use `MAJOR.MINOR.PATCH` formatting such as `0.1.0`.
- A new release section is created only when explicitly requested.
- Changes can accumulate under `Unreleased` until a release is intentionally cut.

## Unreleased

### Security
- Raised msgpack, pygments, urllib3 and virtualenv to fixed versions and removed the temporary `CVE-2026-4539` pip-audit ignore; `make sync` now upgrades pip-tools alongside pip (packet `10-dependency-security-bumps`).

### Changed
- `10Rules.md` merged into `AGENTS.md` (root and bootstrap) and deleted; `AGENTS.md` is now the single source of agent rules, and the root and bootstrap `CLAUDE.md` import it (packet `09-merge-10rules-into-agents`).

### Added
- `CLAUDE.md`: repository-root guidance file auto-loaded by Claude Code, documenting commands, numbered packet system, five-role workflow, and CI enforcement rules (packet `07-add-claude-documentation`).

