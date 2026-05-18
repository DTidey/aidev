# AGENTS.md

## Purpose
This repository uses a spec-first, multi-agent workflow. The spec in `docs/specs/<nn>-<slug>.md` is the source of truth.

## Workflow Order
1. Spec Writer: create or update a spec from `.ai/templates/spec_template.md`.
2. Orchestrator: break spec into tasks and a small commit plan.
3. Implementer: ship minimal code changes strictly against acceptance criteria.
4. Tester: add/update tests mapped to acceptance criteria; add at least 3 adversarial cases beyond the spec edge cases.
5. Reviewer: validate spec alignment, correctness, maintainability, and security.
6. Orchestrator: approve merge only when CI is green and behavior matches spec.

## Non-Negotiable Rules
- No implementation before spec.
- No behavior beyond spec without first updating the spec.
- Every new spec/test-plan/PR-draft change packet must use the same two-digit prefix, such as `03-my-change.md`.
- Assign the next available prefix and never renumber old packets after they land.
- Release versions use `MAJOR.MINOR.PATCH` formatting in `CHANGELOG.md`.
- Do not create a new release unless the user explicitly asks for one.
- Acceptance criteria must be labeled `AC1`, `AC2`, `AC3`, ...
- Acceptance criteria must be testable and mapped to tests.
- Understand first: restate the problem, goal, affected area, and expected outcome before writing code or a spec. Do not assume silently.
- Surface uncertainty with options: if requirements are unclear, ask; present two or three reasonable approaches and recommend the simplest sustainable one.
- Ambiguities must be surfaced explicitly, not guessed silently.
- Fix root causes: never hide errors, silence failures, add fake success paths, or patch symptoms.
- Code-changing specs must document security considerations or explicitly state no meaningful security impact.
- Never hardcode secrets. Confirm with the user before running any destructive deletion command.
- Never use emojis.
- Use current documentation for external libraries and APIs; do not guess syntax or behavior.
- Record the reasoning behind non-obvious decisions in `log/changelog-YYYY-MM-DD.md`.

## Coding Standards
- One file = one purpose; one function = one job.
- Functions ≤ 50 lines, nesting ≤ 4 levels. Split by feature/domain when a file mixes concerns or grows unwieldy.
- Read the relevant code before proposing or making changes.
- Search for existing utilities and patterns before writing new code.
- Write the minimum code that correctly solves the problem; avoid speculative features and unnecessary abstractions.

## Style & Communication
- Lead with the decision or answer; state the reason briefly after.
- The *what* belongs in code; the *why* belongs in responses, commit messages, or comments.
- Comments: write only when the reasoning is not obvious from the code; one line is usually enough.
- Delegate independent work to fresh-context subagents; batch parallel reads in one turn.

## Required Commands
- `make lint`
- `make test`
- `make security`

## PR Requirements
- If code changes are present, include/update a spec in `docs/specs/*.md`.
- PR body must link the spec path (`docs/specs/<nn>-<slug>.md`).
- The linked spec must be the spec updated in the PR.
- PR body must check every acceptance criterion defined in the linked spec.
- For code changes, the spec and PR materials must document the security review disposition.
- If code changes are present, include/update a PR draft in `.ai/pr-description/<nn>-<slug>.md`.
- The PR draft must link the spec path (`docs/specs/<nn>-<slug>.md`).
- The PR draft must check every acceptance criterion defined in the linked spec.
- The PR draft should summarize the behavior change, validation run, and any open risks.
- If code changes are present, include/update `docs/test-plans/<nn>-<slug>.md`.
- Keep PRs small and reviewable.
- Exception: Dependabot PRs that only touch dependency files skip spec validation.

## GitHub Enforcement
- Protect `main` with branch protection or a repository ruleset.
- Require pull requests before merge.
- Require these exact status checks before merge:
  - `CI / test`
  - `CodeQL / analyze`
- Dismiss stale approvals when new commits are pushed.
- Block force pushes and branch deletion on `main`.
- Keep `.github/CODEOWNERS` current so review ownership is explicit.
- Keep Dependabot enabled for `pip` and GitHub Actions updates.

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
- Security considerations reviewed for code-changing work.
- `make security` passes for code-changing work.
- `make lint` and `make test` pass.
- CI is green.
- Shipped behavior matches the current spec.

## Release Notes
- `CHANGELOG.md` tracks intentional release history separately from numbered spec packets.
- Keep unreleased work under `## Unreleased` until an explicit release request is made.
