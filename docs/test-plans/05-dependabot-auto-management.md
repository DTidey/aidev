# Test Plan: dependabot-auto-management

Path: `docs/test-plans/05-dependabot-auto-management.md`

## What changed
- Added a Dependabot-specific workflow that auto-approves and enables auto-merge for safe dependency and workflow update PRs.
- Added content tests to pin the workflow’s scope and safety guards.

## Acceptance criteria coverage
- AC1: Verify the workflow runs on `pull_request_target` for `main` and targets `dependabot[bot]` PRs from `dependabot/` branches.
- AC2: Verify the workflow includes the dependency-manifest allowlist and `.github/workflows/` file filter.
- AC3: Verify the workflow runs approval and `--auto --squash` merge commands.
- AC4: Run `make lint`, `make test`, and `make security`.

## Edge cases
- From spec:
  - Workflow-dependency PRs under `.github/workflows/` should still qualify.
  - PRs that mix allowed files with source-code changes must not qualify.
  - Empty file lists must not qualify.
- Additional adversarial cases:
  - A future change auto-manages all bot PRs instead of only Dependabot PRs.
  - A future change widens the branch guard beyond `dependabot/`.
  - A future change approves PRs but forgets to enable auto-merge.

## Notes
- Flaky risks: None expected from content tests; GitHub-side mergeability still depends on live repository settings.
- Determinism considerations: Pin the workflow content locally and rely on GitHub Actions for runtime behavior.
