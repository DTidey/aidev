"""Tests for CLAUDE.md — packet 07-add-claude-documentation."""

from __future__ import annotations

from pathlib import Path

CLAUDE_MD = Path("CLAUDE.md")


def _content() -> str:
    return CLAUDE_MD.read_text(encoding="utf-8")


# AC1: file exists at repo root with required prefix heading
def test_claude_md_exists_and_has_prefix() -> None:
    assert CLAUDE_MD.is_file(), "CLAUDE.md must exist at the repository root"
    first_line = _content().splitlines()[0]
    assert first_line == "# CLAUDE.md", f"First line must be '# CLAUDE.md', got: {first_line!r}"


# AC2: all make targets and single-test pattern are documented
def test_claude_md_has_all_make_targets() -> None:
    content = _content()
    for target in (
        "make venv",
        "make compile",
        "make sync",
        "make lint",
        "make test",
        "make security",
        "make precommit",
    ):
        assert target in content, f"CLAUDE.md must document '{target}'"
    assert "pytest" in content, "CLAUDE.md must document the single-test invocation using pytest"


# AC3: numbered packet system is described with artifact paths and current highest prefix
def test_claude_md_describes_packet_system() -> None:
    content = _content()
    assert "docs/specs/" in content, "CLAUDE.md must reference the specs artifact path"
    assert "docs/test-plans/" in content, "CLAUDE.md must reference the test-plans artifact path"
    assert ".ai/pr-description/" in content, "CLAUDE.md must reference the pr-description path"
    assert "06" in content, "CLAUDE.md must note the current highest prefix (06)"


# AC4: all five role names are mentioned
def test_claude_md_describes_five_roles() -> None:
    content = _content()
    for role in ("Spec Writer", "Orchestrator", "Implementer", "Tester", "Reviewer"):
        assert role in content, f"CLAUDE.md must describe the '{role}' role"


# AC5: CI enforcement and handoff format are documented
def test_claude_md_documents_ci_and_handoff() -> None:
    content = _content()
    assert "validate_pr.py" in content, "CLAUDE.md must reference validate_pr.py"
    assert "Blocked on:" in content, "CLAUDE.md must include the 'Blocked on:' handoff keyword"
    assert "Affected AC:" in content, "CLAUDE.md must include the 'Affected AC:' handoff keyword"


# Adversarial: file is non-empty
def test_claude_md_is_not_empty() -> None:
    assert len(_content().strip()) > 0, "CLAUDE.md must not be empty"


# Adversarial: does not contradict AGENTS.md on the non-negotiable rule
def test_claude_md_consistent_with_agents_md_no_impl_before_spec() -> None:
    agents = Path("AGENTS.md").read_text(encoding="utf-8")
    claude = _content()
    # Both must reference the spec-first constraint in some form
    assert "spec" in agents.lower()
    assert "spec" in claude.lower()


# Adversarial: required CI checks are named correctly
def test_claude_md_names_required_ci_checks() -> None:
    content = _content()
    assert "CI / test" in content, "CLAUDE.md must name the 'CI / test' required status check"
    assert "CodeQL / analyze" in content, "CLAUDE.md must name the 'CodeQL / analyze' check"
