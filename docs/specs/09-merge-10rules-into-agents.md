# Merge 10Rules into AGENTS

**Spec file:** `docs/specs/09-merge-10rules-into-agents.md`  
**Spec slug:** merge-10rules-into-agents  
**Status:** Done  
**Owner:** DTidey  
**Date:** 2026-10-10  

## Problem statement
- Agent rules were split across `AGENTS.md` and `10Rules.md`, and `AGENTS.md` never referred to
  `10Rules.md`. About a third of `10Rules.md` was missing from `AGENTS.md`, including surgical
  changes, failing-test-first, domain-specific caution and verify-before-done. Tools that read
  only `AGENTS.md` never saw those rules.
- Claude Code auto-loads `CLAUDE.md` but not `AGENTS.md`. Neither aidev's `CLAUDE.md` nor the
  bootstrap `CLAUDE.md` imported it, so Claude sessions in aidev-based repos ran without the rules.
- Found in a downstream repo, DTidey/meridian-capital, which fixed it in its packet 14. This
  packet brings the fix upstream, so new repos built from the bootstrap kit get it too.

## Scope
In scope:
- Root `AGENTS.md`: every missing `10Rules.md` instruction merged into the matching section.
  The file is identical to meridian-capital's.
- Bootstrap `AGENTS.md`: the same rule changes, keeping its placeholders and wrapping.
- Deleting both `10Rules.md` copies and updating live references: bootstrap `README.md`,
  `GETTING_STARTED.md` and `tests/test_bootstrap.py`.
- `@AGENTS.md` imports in the root and bootstrap `CLAUDE.md`.
- Standardising the root `AGENTS.md` on ASCII `<=` and `->`, as the bootstrap already does.

Out of scope / non-goals:
- New rules, or changing the meaning of existing ones.
- Historical packet 08 docs that mention `10Rules.md`.
- The `make sync` pip-tools fix and other Makefile changes; that's a separate packet.

## Assumptions
- `AGENTS.md` is the tool-agnostic convention, so it should be the single source of rules.
- Claude Code resolves `@path` imports in `CLAUDE.md`.
- The user confirmed deleting `10Rules.md` (2026-10-10).

## Proposed behavior / API
### Public interface
- No code interfaces change.
- Bootstrap kit file list: `10Rules.md` removed.
- CLI entry points: none.

### Inputs / outputs
- Inputs: not applicable.
- Outputs: documentation and bootstrap template files.
- Error handling: not applicable.

### Examples
```markdown
## Project rules
@AGENTS.md
```

## Acceptance criteria
- AC1: Root and bootstrap `AGENTS.md` contain every instruction from the deleted `10Rules.md`.
- AC2: Apart from the documented placeholder rules, every rule in the root `AGENTS.md` appears
  in the bootstrap `AGENTS.md` (with wrapping undone). Bootstrap placeholders are kept, and
  unchanged bootstrap lines are byte-identical.
- AC3: `10Rules.md` is deleted at the root and in the bootstrap kit. `GETTING_STARTED.md`, the
  bootstrap `README.md` and the bootstrap `CLAUDE.md` don't mention it, and the bootstrap
  file-list test no longer expects it.
- AC4: The root and bootstrap `CLAUDE.md` both import `@AGENTS.md`.
- AC5: Neither `AGENTS.md` contains typographic operators (`≤`, `→`).

## Security considerations
- Auth/authz impact: None.
- Input handling or injection risk: None.
- Secrets or credential handling: None. The "never hardcode secrets" and destructive-deletion
  confirmation rules are retained in both files.
- Data exposure or privacy impact: None.
- File system access impact: None.
- Network or external service impact: None.
- Dependency or supply-chain impact: None.
- Security notes for reviewers/testers: Documentation and template only. Tests only read files.

## Edge cases
- A 10Rules instruction already partly present: extend the existing bullet, don't duplicate it.
- Hand-wrapped bootstrap text that no wrap width reproduces exactly: patch only the changed rules
  and keep other lines byte-identical.
- Placeholder rules that differ between root and bootstrap on purpose: excluded from the sync
  check by an explicit list.

## Test guidance
- AC1 -> `tests/test_bootstrap.py::test_agents_contains_merged_10rules_principles`
- AC2 -> `tests/test_bootstrap.py::test_root_and_bootstrap_agents_rules_in_sync`,
  `test_bootstrap_agents_has_placeholders`
- AC3 -> `tests/test_bootstrap.py::test_10rules_removed_everywhere`,
  `test_docs_do_not_reference_10rules`, `test_bootstrap_files_present`
- AC4 -> `tests/test_bootstrap.py::test_claude_md_imports_agents`
- AC5 -> `tests/test_bootstrap.py::test_agents_uses_ascii_operators`

## Decision log
- 2026-10-10: Merged into `AGENTS.md` and deleted `10Rules.md`, rather than adding a pointer.
  Tools that don't follow links get every rule, and nothing is left to drift.
- 2026-10-10: Patched the bootstrap rule by rule instead of regenerating it. Its wrapping is
  hand-made (96-99 columns), so regenerating would rewrite unrelated lines.
- 2026-10-10: Added a root/bootstrap sync test, so the two copies can't silently drift again.
