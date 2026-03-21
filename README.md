# aidev

Multi-agent coding workflow with explicit specs, role handoffs, and CI gates.

## Workflow
1. Spec Writer creates/updates `docs/specs/<nn>-<slug>.md` from `.ai/templates/spec_template.md`.
2. Orchestrator creates a task checklist and small commit plan from that spec and keeps the packet aligned.
3. Implementer delivers minimal code changes strictly against acceptance criteria.
4. Tester updates `docs/test-plans/<nn>-<slug>.md` and adds tests mapped to acceptance criteria.
5. Reviewer validates correctness/spec alignment and reports findings by severity.
6. Orchestrator merges only when CI is green and spec matches shipped behavior.

## Role Handoff Format
- Ambiguity/blockers should be explicit:
  - `Blocked on: <question>`
  - `Affected AC: <AC id(s) or "missing">`
  - `Proposed default: <optional>`
- Reviewer blockers should include:
  - `File: <path:line>`
  - `AC: <AC id or N/A>`
  - `Why this blocks merge: <one sentence>`

## Local Commands
```bash
make venv
make compile
make sync
make lint
make test
```

## CI Guardrails
- PRs with code changes must update the exact linked spec in `docs/specs/*.md`.
- PR body must link the spec (`docs/specs/<nn>-<slug>.md`).
- PR body must check every acceptance criterion from the linked spec.
- PRs with code changes must update the matching PR draft at `.ai/pr-description/<nn>-<slug>.md`.
- PRs with code changes must update the matching test plan at `docs/test-plans/<nn>-<slug>.md`.
- Lint and tests must pass.
