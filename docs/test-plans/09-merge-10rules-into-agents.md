# Test Plan: merge-10rules-into-agents

Path: `docs/test-plans/09-merge-10rules-into-agents.md`

## What changed
- `10Rules.md` merged into the root and bootstrap `AGENTS.md`, then deleted. References updated.
- The root and bootstrap `CLAUDE.md` import `@AGENTS.md`.

## Acceptance criteria coverage
- AC1: `tests/test_bootstrap.py::test_agents_contains_merged_10rules_principles` checks both
  files for 10 merged-rule phrases. Manually, a key-phrase check of all 57 instructions from
  `git show main:10Rules.md` against the root `AGENTS.md` gives 57/57.
- AC2: `tests/test_bootstrap.py::test_root_and_bootstrap_agents_rules_in_sync`;
  `test_bootstrap_agents_has_placeholders`. Manually, unwrapping and diffing root against
  bootstrap gives the same 21 placeholder-only differences on `main` and on this branch.
- AC3: `tests/test_bootstrap.py::test_10rules_removed_everywhere`,
  `test_docs_do_not_reference_10rules`, `test_bootstrap_files_present`.
- AC4: `tests/test_bootstrap.py::test_claude_md_imports_agents`.
- AC5: `tests/test_bootstrap.py::test_agents_uses_ascii_operators`.

## Edge cases
- From spec:
  - Placeholder rules excluded from the sync check by an explicit list
  - Untouched bootstrap lines stay byte-identical (diff review)
- Additional adversarial cases:
  - Drift detection: deleting one rule from the bootstrap copy makes the sync and merged-rule
    tests fail (verified, then restored)
  - Wrapped continuation lines are joined before comparison, so wrapping differences don't cause
    false failures
  - An `@AGENTS.md` mention in prose doesn't count: the import test requires it as a whole line
  - Typographic `≤`/`→` reintroduced by copy-paste: `test_agents_uses_ascii_operators`

## Notes
- Flaky risks: none. Tests read repository files only.
- Determinism considerations: none.

## Commands
```bash
make lint
make test
make security
```
