"""Tests for the spec-first-repo bootstrap directory completeness and content."""

from pathlib import Path

BOOTSTRAP = Path(".ai/bootstrap/spec-first-repo")
GETTING_STARTED = Path(".ai/bootstrap/GETTING_STARTED.md")


EXPECTED_FILES = [
    "AGENTS.md",
    "CLAUDE.md",
    "10Rules.md",
    "CHANGELOG.md",
    "README.md",
    "validator-expectations.md",
    ".ai/templates/spec_template.md",
    ".ai/templates/test_plan_template.md",
    ".ai/templates/pr_draft_template.md",
    ".ai/templates/pr_description_template.md",
    ".ai/templates/review_checklist.md",
    ".ai/roles/00_spec_writer.md",
    ".ai/roles/01_orchestrator.md",
    ".ai/roles/02_implementer.md",
    ".ai/roles/03_tester.md",
    ".ai/roles/04_reviewer.md",
    ".ai/pr-description/.gitkeep",
    "docs/specs/README.md",
    "docs/test-plans/README.md",
    "log/.gitkeep",
    ".github/CODEOWNERS",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/dependabot.yml",
    ".github/scripts/validate_pr.py",
    ".github/workflows/ci.yml",
]


def test_bootstrap_files_present() -> None:
    for rel in EXPECTED_FILES:
        assert (BOOTSTRAP / rel).exists(), f"Missing bootstrap file: {rel}"


def test_getting_started_exists() -> None:
    assert GETTING_STARTED.exists()
    text = GETTING_STARTED.read_text(encoding="utf-8")
    for heading in ("Step 1", "Step 2", "Step 3", "Step 5", "Step 9"):
        assert heading in text, f"GETTING_STARTED.md missing section: {heading}"


def test_bootstrap_agents_has_placeholders() -> None:
    text = (BOOTSTRAP / "AGENTS.md").read_text(encoding="utf-8")
    assert "<lint command>" in text
    assert "<test command>" in text
    assert "<security command>" in text
    assert "make lint" not in text
    assert "make test" not in text


def test_bootstrap_role_files_present() -> None:
    roles_dir = BOOTSTRAP / ".ai/roles"
    for i in range(5):
        files = list(roles_dir.glob(f"0{i}_*.md"))
        assert files, f"Missing role file for index {i}"
        assert files[0].stat().st_size > 0, f"Role file is empty: {files[0].name}"


def test_bootstrap_templates_have_security_sections() -> None:
    spec = (BOOTSTRAP / ".ai/templates/spec_template.md").read_text(encoding="utf-8")
    assert "Security considerations" in spec

    for tmpl in ("pr_draft_template.md", "pr_description_template.md"):
        text = (BOOTSTRAP / ".ai/templates" / tmpl).read_text(encoding="utf-8")
        assert "ecurity review" in text or "ecurity Review" in text, (
            f"{tmpl} missing security review section"
        )

    checklist = (BOOTSTRAP / ".ai/templates/review_checklist.md").read_text(encoding="utf-8")
    assert "path traversal" in checklist


def test_bootstrap_validate_pr_functions_present() -> None:
    text = (BOOTSTRAP / ".github/scripts/validate_pr.py").read_text(encoding="utf-8")
    for fn in ("def main", "def changed_files", "def spec_ac_ids", "def checked_ac_ids"):
        assert fn in text, f"validate_pr.py missing function: {fn}"
    assert "if __name__" in text


def test_bootstrap_spec_template_no_python_fence() -> None:
    text = (BOOTSTRAP / ".ai/templates/spec_template.md").read_text(encoding="utf-8")
    assert "```python" not in text, "spec_template should use language-agnostic code fence"
