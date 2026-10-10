## Summary

- Merges every `10Rules.md` instruction missing from `AGENTS.md` into the matching section of
  the root and bootstrap `AGENTS.md`, then deletes both `10Rules.md` copies. `AGENTS.md` is now
  the single source of agent rules.
- Adds `@AGENTS.md` to the root and bootstrap `CLAUDE.md`. Claude Code only auto-loads
  `CLAUDE.md`, so without the import Claude sessions never saw the rules.
- Patches the bootstrap template rule by rule, keeping its placeholders and hand wrapping, and
  adds a sync test so the root and bootstrap copies can't drift.
- Upstreams DTidey/meridian-capital packet 14; the root `AGENTS.md` is identical to meridian's.

## Spec

- Spec: `docs/specs/09-merge-10rules-into-agents.md`
- Test plan: `docs/test-plans/09-merge-10rules-into-agents.md`
- PR draft path: `.ai/pr-description/09-merge-10rules-into-agents.md`

## Acceptance Criteria

- [x] AC1: Root and bootstrap `AGENTS.md` contain every instruction from `10Rules.md`.
- [x] AC2: Bootstrap rules match the root apart from documented placeholders; unchanged lines
  are byte-identical.
- [x] AC3: `10Rules.md` deleted in both places; docs and the file-list test updated.
- [x] AC4: Root and bootstrap `CLAUDE.md` import `@AGENTS.md`.
- [x] AC5: Neither `AGENTS.md` contains typographic operators.

## Security Review

- [x] Security considerations reviewed in `docs/specs/09-merge-10rules-into-agents.md`
- [x] Documentation and template only; secrets and destructive-deletion rules retained

## Validation

- `ruff check` and `ruff format --check` (ruff 0.16.10, as pinned): pass
- `make test`: 47 passed
- `make security`: pass (after rebasing onto packet 10, which fixed the vulnerable pins)
- Drift check: removing a rule from the bootstrap copy makes the new tests fail

Open risks: none.
