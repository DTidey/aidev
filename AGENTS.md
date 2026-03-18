# AGENTS.md

## Purpose
This repository uses a spec-first, multi-agent workflow. The spec in `docs/specs/<slug>.md` is the source of truth.

## Workflow Order
1. Spec Writer: create or update a spec from `.ai/templates/spec_template.md`.
2. Orchestrator: break spec into tasks and a small commit plan.
3. Implementer: ship minimal code changes strictly against acceptance criteria.
4. Tester: add/update tests mapped to acceptance criteria.
5. Reviewer: validate spec alignment, correctness, and maintainability.
6. Orchestrator: approve merge only when CI is green and behavior matches spec.

## Non-Negotiable Rules
- No implementation before spec.
- No behavior beyond spec without first updating the spec.
- Acceptance criteria must be labeled `AC1`, `AC2`, `AC3`, ...
- Acceptance criteria must be testable and mapped to tests.
- Ambiguities must be surfaced explicitly, not guessed silently.

## Required Commands
- `make lint`
- `make test`

## PR Requirements
- If code changes are present, include/update a spec in `docs/specs/*.md`.
- PR body must link the spec path (`docs/specs/<slug>.md`).
- The linked spec must be the spec updated in the PR.
- PR body must check every acceptance criterion defined in the linked spec.
- If code changes are present, include/update `docs/test-plans/<slug>.md`.
- Keep PRs small and reviewable.

## Role Handoff Format
When blocked or unclear, use:
- `Blocked on: <question>`
- `Affected AC: <AC id(s) or "missing">`
- `Proposed default: <optional>`

Reviewer blockers must include:
- `File: <path:line>`
- `AC: <AC id or "N/A">`
- `Why this blocks merge: <one sentence>`

## Definition of Done
- All acceptance criteria satisfied.
- Tests added/updated for new behavior.
- `make lint` and `make test` pass.
- CI is green.
- Shipped behavior matches the current spec.
