---
name: spec-first-workflow
description: Use when a repo follows a spec-first development process with source-of-truth specs, acceptance criteria, small role-based handoffs, and often aligned change packets such as docs/specs, docs/test-plans, and PR drafts sharing the same two-digit prefix; Codex should defer to repo-local workflow files such as AGENTS.md, README, docs/specs, .ai/templates, or validator scripts when present.
---

# Spec-First Workflow

Use this skill when the user wants work done inside a repository that appears to use a spec-first workflow, especially one with:

- a source-of-truth spec for each change
- acceptance criteria labels such as `AC1`, `AC2`, `AC3`
- role-based stages like spec writer, implementer, tester, reviewer, or orchestrator
- companion artifacts that stay aligned by slug or packet number
- CI or scripts that validate spec links, AC checklists, or packet naming

## Goals

- Keep implementation aligned to a written spec.
- Prefer small, reviewable changes.
- Make ambiguity explicit instead of silently inventing behavior.
- Keep spec, implementation, tests, and PR artifacts in sync.

## Precedence

Apply instructions in this order:

1. Explicit user request
2. Repo-local instructions and templates such as `AGENTS.md`, `README.md`, `docs/specs/README.md`, `.ai/templates/*`, or CI validators
3. This skill's defaults

If the repo already defines a workflow, follow it. This skill exists to make Codex reliable and consistent, not to override the repository.

## Quick Start

Before editing code:

1. Look for repo-local workflow signals such as `AGENTS.md`, `CLAUDE.md`, `README.md`, `docs/specs/`, `docs/test-plans/`, `.ai/templates/`, `.ai/roles/`, or validator scripts/tests.
2. Decide whether the repo uses numbered change packets like `<nn>-<slug>.md`, especially shared prefixes across spec, test plan, and PR draft artifacts.
3. If code changes are requested, identify the governing spec. If none exists, create or update the spec first unless the user explicitly asks only for planning/discussion.
4. Confirm which companion artifacts are required for code changes, commonly spec, test plan, and PR draft, and whether they must share the same packet prefix.

For repo-detection details and default behaviors, read [references/repo-signals.md](references/repo-signals.md).

## Default Workflow

Use this sequence unless the repo defines another one:

1. Spec Writer
   Create or update the spec from the repo template if present.
2. Orchestrator
   Break the spec into a short task list and small commit plan.
3. Implementer
   Ship the smallest code change that satisfies the acceptance criteria.
4. Tester
   Add or update tests and the test plan, mapping tests to acceptance criteria.
5. Reviewer
   Check spec alignment, correctness, maintainability, and regression risk.
6. Orchestrator
   Verify lint/tests/CI expectations and confirm the shipped behavior matches the spec.

## Spec Rules

When creating or updating a spec:

- Prefer the repo's template if one exists.
- Keep the scope explicit.
- Include non-goals when useful.
- Label acceptance criteria `AC1`, `AC2`, `AC3`, and so on if the repo expects AC labels.
- Make each acceptance criterion testable.
- Surface uncertainty explicitly.

If blocked by ambiguity, use this handoff format unless the repo defines another:

- `Blocked on: <question>`
- `Affected AC: <AC id(s) or "missing">`
- `Proposed default: <optional>`

## Implementation Rules

- Do not implement behavior that is not in the spec unless the spec is updated first.
- Prefer minimal code changes over broad refactors.
- Map each user-visible behavior change back to one or more acceptance criteria.
- Keep changes small and reviewable.
- Preserve existing repo conventions, naming, and validation flows.

## Test And PR Artifacts

If the repo expects companion artifacts for code changes:

- Keep the spec, test plan, and PR draft on the same packet or slug when applicable.
- Ensure acceptance criteria checked in PR materials exactly match the spec's AC IDs.
- Summarize validation run and open risks if the repo expects that.

Common patterns include:

- `docs/specs/<nn>-<slug>.md`
- `docs/test-plans/<nn>-<slug>.md`
- `.ai/pr-description/<nn>-<slug>.md`

Treat these as defaults only when repo-local files support them.

If the repo requires numbered packets:

- use the next available prefix
- keep all related artifacts on the same prefix
- never silently renumber existing packets

## Validation

Run the repo's required validation commands when available. Common examples:

- `make lint`
- `make test`

If CI or local validators enforce spec links, artifact presence, packet naming, or AC checklists, satisfy those constraints before considering the work done.

## Reviewer Mode

If the user asks for a review, prioritize findings:

- Report correctness bugs, spec mismatches, missing tests, regressions, and maintainability risks first.
- Include concrete file references and affected acceptance criteria when possible.
- Keep summaries brief after findings.

Use this blocker format unless the repo defines another:

- `File: <path:line>`
- `AC: <AC id or "N/A">`
- `Why this blocks merge: <one sentence>`

## Defaults When The Repo Is Silent

If no repo-local workflow exists, the safe default is:

- create a spec before code changes
- label testable acceptance criteria
- implement minimally against the spec
- add tests for new behavior
- run lint and tests
- keep supporting artifacts aligned if they exist
