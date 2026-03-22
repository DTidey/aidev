# Repo Signals

Use this file only when you need help deciding how much of the workflow should come from the repo versus the skill.

## Strong Signals

Treat the repo as authoritative if you find any of these:

- `AGENTS.md` or similar workflow instructions
- templates such as `.ai/templates/spec_template.md`
- role files such as `.ai/roles/*.md`
- docs that define spec, test-plan, or PR-draft paths
- tests or scripts that validate spec links, acceptance criteria, or artifact naming

When these exist, mirror them instead of inventing a parallel process.

## Useful Questions

Answer these quickly before coding:

1. What file is the source of truth for behavior?
2. Is there already a spec for this change?
3. Does the repo require numbered packets or matching artifact names?
4. Which companion artifacts are required for code changes?
5. Which commands or scripts determine readiness?

## Good Default Assumptions

Use these only when the repo does not answer the question:

- A spec should exist before implementation.
- Acceptance criteria should be labeled and testable.
- Tests should map back to acceptance criteria.
- Code changes should be minimal and should not exceed the spec.
- Lint and tests should pass before handoff.

## When To Escalate

Pause and ask the user when:

- the requested behavior conflicts with the current spec
- multiple specs might govern the same change
- the repo has incompatible workflow signals
- there is no safe default for ambiguous behavior
