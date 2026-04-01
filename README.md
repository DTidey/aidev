# aidev

Multi-agent coding workflow with explicit specs, role handoffs, and CI gates.

## Workflow
1. Spec Writer creates/updates `docs/specs/<nn>-<slug>.md` from `.ai/templates/spec_template.md`.
2. Orchestrator creates a task checklist and small commit plan from that spec and keeps the packet aligned.
3. Implementer delivers minimal code changes strictly against acceptance criteria.
4. Tester updates `docs/test-plans/<nn>-<slug>.md`, adds tests mapped to acceptance criteria, and covers security-relevant behavior called out in the spec.
5. Reviewer validates correctness, spec alignment, and documented security impact, then reports findings by severity.
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
make security
```

## CI Guardrails
- PRs with code changes must update the exact linked spec in `docs/specs/*.md`.
- PR body must link the spec (`docs/specs/<nn>-<slug>.md`).
- PR body must check every acceptance criterion from the linked spec.
- PRs with code changes must update the matching PR draft at `.ai/pr-description/<nn>-<slug>.md`.
- PRs with code changes must update the matching test plan at `docs/test-plans/<nn>-<slug>.md`.
- Code-changing specs and PR materials should record the security review disposition, even when the answer is "no meaningful security impact".
- Automated validation should run through `make security` for repositories that adopt the default Python security tooling.
- Lint and tests must pass.

## GitHub Enforcement
- Protect `main` in GitHub branch protection or a repository ruleset.
- Require a pull request before merging into `main`.
- Require status checks before merging and select these exact checks:
  - `CI / test`
  - `CodeQL / analyze`
- Dismiss stale approvals when new commits are pushed.
- Block force pushes and branch deletion on `main`.
- Keep `CODEOWNERS` enabled so review ownership stays explicit.
- Let Dependabot manage weekly updates for `pip` and GitHub Actions dependencies.

## Security Review
- Code-changing specs should include a `Security considerations` section so authors can call out auth/authz, input handling, secrets, data exposure, file access, network access, and dependency impact.
- PR materials should summarize the security review disposition so reviewers know whether there is no meaningful security impact or a sensitive area that needs extra scrutiny.
- This repository currently uses `make security` as the default automation entry point, backed by Bandit and pip-audit.
- The default `pip-audit` invocation currently ignores `CVE-2026-4539` for `pygments` because no fixed version was available when this workflow was added; revisit that exception when upstream guidance changes.
- Deeper AppSec automation can still be layered on later for secret scanning, broader SAST, or language-specific checks.
