# Specs

Each feature or behavior change should have a spec in this folder.

Convention:
- Spec: `docs/specs/<nn>-<slug>.md`
- Test plan: `docs/test-plans/<nn>-<slug>.md`
- PR draft: `.ai/pr-description/<nn>-<slug>.md`

Every spec should include:
- Problem statement
- Scope and non-goals
- Acceptance criteria labeled `AC1`, `AC2`, ...
- Edge cases and error handling
- Test guidance mapping `AC` IDs to tests

Workflow:
1. Create or update the spec.
2. Break the spec into a short task list and commit plan.
3. Implement strictly to the spec.
4. Add tests and the matching test plan.
5. Review against the spec and acceptance criteria.
6. Merge only when CI is green and behavior matches the spec.

Authoring notes:
- Keep acceptance criteria concrete and testable.
- If a change affects behavior not covered by the spec, update the spec first.
- Use the next available two-digit packet prefix for new work.
