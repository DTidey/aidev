"""Tests for the spec-first-repo bootstrap directory completeness and content."""

from pathlib import Path

BOOTSTRAP = Path(".ai/bootstrap/spec-first-repo")
GETTING_STARTED = Path(".ai/bootstrap/GETTING_STARTED.md")


EXPECTED_FILES = [
    "AGENTS.md",
    "CLAUDE.md",
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


ROOT_AGENTS = Path("AGENTS.md")
MERGED_RULE_PHRASES = (
    "If the request is risky, say so.",
    "For domain-specific code, do not guess.",
    "Keep changes surgical",
    "reproduce with a failing test first",
    "Verify before claiming done",
    "Protect the system",
    "Cohesion beats line count.",
    "each step includes its own check",
    "explain a jargon term the first time it appears",
    "Between unrelated tasks, clear context.",
)
# Rules that are deliberately repo-specific in the root file and placeholders in the bootstrap.
_PLACEHOLDER_RULES = (
    "make lint",
    "make test",
    "make security",
    "CI / test",
    "CodeQL / analyze",
    "Require these exact status checks",
    "Keep Dependabot enabled for `pip`",
)


def _rule_bullets(text: str) -> list[str]:
    """Return list items with wrapped continuation lines joined into one line each."""
    items: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if line.startswith(("- ", "1. ", "2. ", "3. ", "4. ", "5. ", "6. ")):
            items.append(stripped)
        elif items and line.startswith("  ") and not stripped.startswith("- "):
            items[-1] += " " + stripped
    return items


def test_10rules_removed_everywhere() -> None:
    assert not Path("10Rules.md").exists()
    assert not (BOOTSTRAP / "10Rules.md").exists()


def test_agents_contains_merged_10rules_principles() -> None:
    for path in (ROOT_AGENTS, BOOTSTRAP / "AGENTS.md"):
        flat = " ".join(path.read_text(encoding="utf-8").split())
        for phrase in MERGED_RULE_PHRASES:
            assert phrase in flat, f"{path} missing merged rule: {phrase}"


def test_root_and_bootstrap_agents_rules_in_sync() -> None:
    root = _rule_bullets(ROOT_AGENTS.read_text(encoding="utf-8"))
    boot = set(_rule_bullets((BOOTSTRAP / "AGENTS.md").read_text(encoding="utf-8")))
    shared = [r for r in root if not any(p in r for p in _PLACEHOLDER_RULES)]
    missing = [r for r in shared if r not in boot]
    assert not missing, f"bootstrap AGENTS.md out of sync with root: {missing[:3]}"


def test_claude_md_imports_agents() -> None:
    for path in (Path("CLAUDE.md"), BOOTSTRAP / "CLAUDE.md"):
        lines = path.read_text(encoding="utf-8").splitlines()
        assert "@AGENTS.md" in lines, f"{path} does not import AGENTS.md"


def test_docs_do_not_reference_10rules() -> None:
    for path in (GETTING_STARTED, BOOTSTRAP / "README.md", BOOTSTRAP / "CLAUDE.md"):
        assert "10Rules" not in path.read_text(encoding="utf-8"), f"{path} still mentions 10Rules"


def test_agents_uses_ascii_operators() -> None:
    for path in (ROOT_AGENTS, BOOTSTRAP / "AGENTS.md"):
        text = path.read_text(encoding="utf-8")
        assert "≤" not in text and "→" not in text, f"{path} uses typographic operators"
