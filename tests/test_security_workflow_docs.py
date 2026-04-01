from pathlib import Path


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def test_spec_template_includes_security_considerations_prompts() -> None:
    content = read(".ai/templates/spec_template.md")
    assert "## Security considerations" in content
    assert "- Auth/authz impact:" in content
    assert "- Input handling or injection risk:" in content
    assert "- Secrets or credential handling:" in content
    assert "- Data exposure or privacy impact:" in content
    assert "- File system access impact:" in content
    assert "- Network or external service impact:" in content
    assert "- Dependency or supply-chain impact:" in content


def test_pr_templates_include_security_review_and_no_impact_path() -> None:
    for path in [
        ".github/PULL_REQUEST_TEMPLATE.md",
        ".ai/templates/pr_draft_template.md",
        ".ai/templates/pr_description_template.md",
    ]:
        content = read(path)
        assert "Security" in content
        assert "Security considerations were reviewed and updated in the linked spec" in content
        assert "No meaningful security impact" in content
        assert "Reviewer focus:" in content


def test_role_guidance_calls_for_security_review_and_blockers() -> None:
    tester = read(".ai/roles/03_tester.md")
    reviewer = read(".ai/roles/04_reviewer.md")

    assert "Security considerations" in tester
    assert "security impact is unclear or inadequately testable" in tester
    assert "Security considerations" in reviewer
    assert "security impact is unclear, undocumented, or inadequately tested" in reviewer


def test_repo_docs_describe_security_review_as_required_workflow_behavior() -> None:
    agents = read("AGENTS.md")
    readme = read("README.md")

    assert "Code-changing specs must document security considerations" in agents
    assert "Security considerations reviewed for code-changing work" in agents
    assert "## Security Review" in readme
    assert "## GitHub Enforcement" in agents
    assert "## GitHub Enforcement" in readme
    assert "CI / test" in agents
    assert "CodeQL / analyze" in agents
    assert "CI / test" in readme
    assert "CodeQL / analyze" in readme
    assert "make security" in agents
    assert "make security" in readme


def test_makefile_and_ci_wire_security_automation() -> None:
    makefile = read("Makefile")
    ci = read(".github/workflows/ci.yml")
    reqs = read("requirements-dev.in")

    assert "PYTHON ?= python3" in makefile
    assert "$(PYTHON) -m venv .venv" in makefile
    assert "security:" in makefile
    assert "bandit -q -r .github/scripts" in makefile
    assert "XDG_CACHE_HOME=/tmp/.cache pip-audit --no-deps --disable-pip" in makefile
    assert "--ignore-vuln CVE-2026-4539" in makefile
    assert "name: Create virtualenv" in ci
    assert "make venv" in ci
    assert "make compile" in ci
    assert "make sync" in ci
    assert "make lint" in ci
    assert "name: Security" in ci
    assert "make security" in ci
    assert "make test" in ci
    assert "bandit" in reqs
    assert "pip-audit" in reqs


def test_github_guardrails_files_exist_and_match_documented_checks() -> None:
    codeql = read(".github/workflows/codeql.yml")
    auto_approve = read(".github/workflows/auto-approve-own-prs.yml")
    auto_dependabot = read(".github/workflows/auto-manage-dependabot-prs.yml")
    dependabot = read(".github/dependabot.yml")
    codeowners = read(".github/CODEOWNERS")
    pr_template = read(".github/PULL_REQUEST_TEMPLATE.md")
    pr_draft_template = read(".ai/templates/pr_draft_template.md")
    pr_description_template = read(".ai/templates/pr_description_template.md")

    assert "name: CodeQL" in codeql
    assert "language: [python, actions]" in codeql
    assert "github/codeql-action/init@v4" in codeql
    assert "github/codeql-action/autobuild@v4" in codeql
    assert "github/codeql-action/analyze@v4" in codeql
    assert "pull_request_target:" in auto_approve
    assert "branches: [main]" in auto_approve
    assert "pull-requests: write" in auto_approve
    assert "github.event.pull_request.user.login == github.repository_owner" in auto_approve
    assert "startsWith(github.event.pull_request.head.ref, 'codex/')" in auto_approve
    assert 'gh pr review "${{ github.event.pull_request.html_url }}" --approve' in auto_approve
    assert "name: Auto-manage Dependabot PRs" in auto_dependabot
    assert "pull_request_target:" in auto_dependabot
    assert "types: [opened, reopened, synchronize, ready_for_review]" in auto_dependabot
    assert "branches: [main]" in auto_dependabot
    assert "contents: write" in auto_dependabot
    assert "pull-requests: write" in auto_dependabot
    assert "github.event.pull_request.user.login == 'dependabot[bot]'" in auto_dependabot
    assert "startsWith(github.event.pull_request.head.ref, 'dependabot/')" in auto_dependabot
    assert "uses: actions/github-script@v7" in auto_dependabot
    assert '"requirements.txt"' in auto_dependabot
    assert '".github/workflows/"' in auto_dependabot
    assert 'gh pr review "${{ github.event.pull_request.html_url }}" --approve' in auto_dependabot
    assert (
        'gh pr merge "${{ github.event.pull_request.html_url }}" --auto --squash' in auto_dependabot
    )
    assert 'package-ecosystem: "pip"' in dependabot
    assert 'package-ecosystem: "github-actions"' in dependabot
    assert "@DTidey" in codeowners
    assert "make security" in pr_template
    assert "CI / test" in pr_draft_template
    assert "CodeQL / analyze" in pr_draft_template
    assert "CI / test" in pr_description_template
    assert "CodeQL / analyze" in pr_description_template
