# Specs

Each feature/change should have a spec in this folder.

Convention:
- Spec: `docs/specs/<nn>-<slug>.md`
- Test plan: `docs/test-plans/<nn>-<slug>.md`
- PR draft: `.ai/pr-description/<nn>-<slug>.md`

Every spec should include:
- Scope and non-goals
- Acceptance criteria labeled `AC1`, `AC2`, ...
- Edge cases and error handling
- Test guidance mapping AC -> tests

Workflow:
1. Create or update the spec (Spec Writer)
2. Break the spec into tasks and a small commit plan (Orchestrator)
3. Implement strictly to the spec (Implementer)
4. Add tests and the matching test plan (Tester)
5. Review against the spec and acceptance criteria (Reviewer)
6. Merge only when CI is green and behavior matches the spec (Orchestrator)
