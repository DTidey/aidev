# Test Plan: automated-security-checks

Path: `docs/test-plans/02-automated-security-checks.md`

## What changed
- Added a proposal for automated security checks as a first-class repository command and CI step.
- Standardized phase 2 around a single `make security` entry point backed by Python-focused tooling.

## Acceptance criteria coverage
- AC1: Verify `Makefile` defines `make security` and runs both a static security analyzer and a dependency vulnerability audit.
- AC2: Verify CI runs `make security` as part of the standard validation job.
- AC3: Verify repository docs and workflow guidance include `make security` as a standard command for code-changing work.
- AC4: Verify tests or static assertions cover the command definition, CI integration, and documentation expectations.

## Edge cases
- From spec:
  - Static analysis should behave sensibly even though this repo contains limited Python application code.
  - Dependency auditing should work when runtime requirements are empty.
  - CI and local commands must stay aligned.
  - The command should remain tunable if a tool is noisy.
- Additional adversarial cases:
  - CI runs raw security tools directly while local developers are told to use a different command.
  - `make security` exists but only runs one class of check.
  - Documentation mentions security automation without naming the actual command contributors should run.

## Notes
- Flaky risks: Dependency audit output can vary with vulnerability database state, so structural tests should focus on configuration while command validation runs in CI/local usage.
- Determinism considerations: Prefer file-content assertions for workflow wiring and run the actual command in repo validation once dependencies are installed.
- Known exception: `pip-audit` temporarily ignores `CVE-2026-4539` for `pygments` until an upstream fix is available.
