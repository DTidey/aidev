# AGENTS.md

## Purpose
This repository uses a spec-first workflow. The spec in `docs/specs/<nn>-<slug>.md` is the source of truth for behavior changes.

## Workflow Order
1. Spec Writer: create or update a spec from `.ai/templates/spec_template.md`.
2. Orchestrator: break the spec into tasks and a small commit plan.
3. Implementer: ship minimal code changes strictly against acceptance criteria.
4. Tester: add or update tests mapped to acceptance criteria and maintain `docs/test-plans/<nn>-<slug>.md`.
5. Reviewer: validate spec alignment, correctness, and maintainability.
6. Orchestrator: approve merge only when CI is green and behavior matches the spec.

## Non-Negotiable Rules
- No implementation before spec.
- No behavior beyond spec without first updating the spec.
- Every new spec, test-plan, and PR-draft packet uses the same two-digit prefix, such as `03-my-change.md`.
- Assign the next available prefix and never renumber old packets after they land.
- Acceptance criteria must be labeled `AC1`, `AC2`, `AC3`, ...
- Acceptance criteria must be testable and mapped to tests.
- Ambiguities must be surfaced explicitly, not guessed silently.
- Do not create a release unless explicitly requested.

## Required Commands
- `<lint command>`
- `<test command>`

## PR Requirements
- If code changes are present, include or update a spec in `docs/specs/*.md`.
- PR body must link the spec path `docs/specs/<nn>-<slug>.md`.
- The linked spec must be the spec updated in the PR.
- PR body must check every acceptance criterion defined in the linked spec.
- If code changes are present, include or update a PR draft in `.ai/pr-description/<nn>-<slug>.md`.
- The PR draft must link the same spec path.
- The PR draft must check every acceptance criterion defined in the linked spec.
- If code changes are present, include or update `docs/test-plans/<nn>-<slug>.md`.
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
- Tests added or updated for new behavior.
- Required validation commands pass.
- CI is green.
- Shipped behavior matches the current spec.

## Release Notes
- Keep unreleased work under `## Unreleased` in `CHANGELOG.md` if the repo uses release notes.
