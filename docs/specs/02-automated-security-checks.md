# Automated Security Checks

**Spec file:** `docs/specs/02-automated-security-checks.md`
**Spec slug:** automated-security-checks
**Status:** Done
**Owner:** Codex
**Date:** 2026-03-31

## Problem statement
- The workflow now requires documented security review, but it still relies entirely on human diligence for automated detection of common issues.
- Repositories adopting this framework need a simple default for automated security checks that fits the existing `make`-driven workflow and CI.
- Without a standard command, teams will either skip automation entirely or invent inconsistent security steps per repository.

## Scope
In scope:
- Add a required `make security` command to the repository.
- Install and document a lightweight Python security toolchain suitable for this repo.
- Run automated security checks in CI alongside lint and tests.
- Update workflow docs, templates, and test coverage so the new command is part of the framework rather than an ad hoc local convention.

Out of scope / non-goals:
- Achieving comprehensive application security coverage.
- Adding secret-scanning baselines or repository history scanning in this phase.
- Blocking on language-specific tools for non-Python repos that may adopt the workflow later.
- Replacing human review of security-sensitive behavior.

## Assumptions
- This repository should provide a concrete example implementation for Python-based adopters.
- The smallest useful default is one static analyzer plus one dependency vulnerability audit.
- False positives should be manageable enough that contributors can run the checks locally without heavy triage overhead.
- Security automation should be exposed through a single make target to keep CI and local usage aligned.

## Proposed behavior / API
### Public interface
- Files/modules affected:
  - `Makefile`
  - `requirements-dev.in`
  - `requirements-dev.txt`
  - `.github/workflows/ci.yml`
  - `AGENTS.md`
  - `README.md`
  - `.ai/templates/pr_draft_template.md`
  - `.ai/templates/pr_description_template.md`
  - `tests/test_security_workflow_docs.py`

### Inputs / outputs
- Inputs:
  - Repository Python source files
  - `requirements.txt`
  - `requirements-dev.txt`
- Outputs:
  - `make security` runs the configured automated security checks and exits non-zero on findings
  - CI runs the same security command before tests complete
  - Documentation tells contributors when and why to run the command
- Error handling:
  - Security tool failures should fail the command and CI job clearly
  - Repositories without Python application code may still pass the checks if no issues are found in the existing tree

### Examples
```bash
make security
```

```text
bandit scans the repository for common Python security issues
pip-audit checks runtime and development dependencies for known vulnerabilities
```

## Acceptance criteria
- AC1: The repository exposes a `make security` command that runs at least one static security analysis tool and one dependency vulnerability audit suitable for this Python project.
- AC2: The CI workflow runs the automated security checks as part of the standard validation path.
- AC3: Repository documentation and workflow guidance treat `make security` as a standard command for code-changing work.
- AC4: Tests or static assertions verify the security command, CI integration, and documented workflow expectations so the automation remains part of the framework.

## Security considerations
- Auth/authz impact: None directly; this change affects developer workflow, not runtime access control.
- Input handling or injection risk: Low; commands are fixed in repository-controlled tooling.
- Secrets or credential handling: Avoid tools that require external credentials for normal operation.
- Data exposure or privacy impact: Low; checks run locally in the repository tree and against dependency metadata.
- File system access impact: Read-only scanning of repo contents and dependency manifests.
- Network or external service impact: Dependency audit tooling may rely on vulnerability data sources during installation or execution depending on environment.
- Dependency or supply-chain impact: Introduces new development-only security tooling that should be pinned in compiled requirements.
- Security notes for reviewers/testers: Watch for brittle CI coupling, excessive false positives, or commands that silently skip checks.

## Edge cases
- The repository has very little Python application code today, so static analysis should still behave sensibly on a mostly workflow-oriented repo.
- Dependency auditing should succeed even when runtime requirements are currently empty.
- CI and local commands must stay aligned; avoid duplicating raw tool invocations only in workflow YAML.
- If a tool proves too noisy for a starter framework, the command should remain easy to tune later.

## Test guidance
- AC1 -> Tests or static assertions verify `Makefile` defines `security` and references both configured tools
- AC2 -> Tests or static assertions verify `.github/workflows/ci.yml` runs `make security`
- AC3 -> Documentation review verifies `AGENTS.md` and `README.md` include `make security` in expected commands
- AC4 -> Tests verify workflow docs reference the new command and security automation expectations

## Decision log
- 2026-03-31: Chose a single `make security` target with Bandit and pip-audit as the initial Python example because it is simple, common, and aligned with the existing make-based workflow.
- 2026-03-31: Added a temporary `pip-audit` ignore for `CVE-2026-4539` on `pygments` because the audit reported no available fixed version; revisit when upstream remediation is available.
