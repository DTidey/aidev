# Specs

Each feature/change should have a spec in this folder.

Code-changing specs should also have a matching test plan in `docs/test-plans/<slug>.md`.

Every spec should include:
- Scope and non-goals
- Acceptance criteria labeled `AC1`, `AC2`, ...
- Edge cases and error handling
- Test guidance mapping AC -> tests

Workflow:
1) Create spec (Spec Writer)
2) Implement to spec (Implementer)
3) Add tests (Tester)
4) Review against spec (Reviewer)
5) Merge only when CI is green (Orchestrator)
