from __future__ import annotations

import importlib.util
from pathlib import Path


def _load_validate_pr_module():
    script_path = Path(".github/scripts/validate_pr.py")
    spec = importlib.util.spec_from_file_location("validate_pr", script_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_is_docs_only_allows_markdown_and_known_root_files() -> None:
    mod = _load_validate_pr_module()
    files = [
        "docs/specs/09-new-feature.md",
        ".ai/roles/00_spec_writer.md",
        ".github/PULL_REQUEST_TEMPLATE.md",
        "README.md",
    ]
    assert mod.is_docs_only(files) is True


def test_is_docs_only_rejects_code_like_changes_under_dot_github() -> None:
    mod = _load_validate_pr_module()
    files = [
        ".github/scripts/validate_pr.py",
        ".github/workflows/ci.yml",
    ]
    assert mod.is_docs_only(files) is False


def test_is_docs_only_rejects_non_markdown_under_docs_and_ai() -> None:
    mod = _load_validate_pr_module()
    files = [
        "docs/generator.py",
        ".ai/templates/spec_template.yaml",
    ]
    assert mod.is_docs_only(files) is False


def test_extract_spec_link_returns_first_match() -> None:
    mod = _load_validate_pr_module()
    body = """
## Spec
- Link to docs/specs/01-first-spec.md
- Backup link docs/specs/02-second-spec.md
"""
    assert mod.extract_spec_link(body) == "docs/specs/01-first-spec.md"


def test_checked_ac_ids_parses_only_checked_items() -> None:
    mod = _load_validate_pr_module()
    body = """
## Acceptance criteria
- [x] AC1 implemented
- [X] AC2 implemented
- [ ] AC3 pending
"""
    assert mod.checked_ac_ids(body) == {"AC1", "AC2"}


def test_spec_ac_ids_extracts_defined_acceptance_criteria(tmp_path: Path) -> None:
    mod = _load_validate_pr_module()
    spec_file = tmp_path / "spec.md"
    spec_file.write_text(
        "\n".join(
            [
                "# Feature",
                "",
                "## Acceptance criteria",
                "- AC1: first requirement",
                "- AC2: second requirement",
                "- AC10: tenth requirement",
            ]
        ),
        encoding="utf-8",
    )
    assert mod.spec_ac_ids(str(spec_file)) == {"AC1", "AC2", "AC10"}


def test_checked_acs_can_be_compared_against_spec_ids(tmp_path: Path) -> None:
    mod = _load_validate_pr_module()
    spec_file = tmp_path / "spec.md"
    spec_file.write_text(
        "\n".join(
            [
                "## Acceptance criteria",
                "- AC1: first requirement",
                "- AC2: second requirement",
            ]
        ),
        encoding="utf-8",
    )
    body = """
- [x] AC1 done
- [x] AC3 done
"""
    unknown = sorted(mod.checked_ac_ids(body) - mod.spec_ac_ids(str(spec_file)))
    assert unknown == ["AC3"]


def test_changed_specs_ignores_specs_readme() -> None:
    mod = _load_validate_pr_module()
    files = [
        "docs/specs/README.md",
        "docs/specs/01-feature-a.md",
        "docs/specs/02-feature-b.md",
    ]
    assert mod.changed_specs(files) == {
        "docs/specs/01-feature-a.md",
        "docs/specs/02-feature-b.md",
    }


def test_is_dependabot_dependency_only_allows_dependency_files() -> None:
    mod = _load_validate_pr_module()
    files = [
        "pyproject.toml",
        "requirements.in",
        "requirements.txt",
        "requirements-dev.in",
        "requirements-dev.txt",
        ".github/workflows/ci.yml",
    ]
    assert mod.is_dependabot_dependency_only(files) is True


def test_is_dependabot_dependency_only_rejects_regular_source_changes() -> None:
    mod = _load_validate_pr_module()
    files = [
        "pyproject.toml",
        "backend/app/main.py",
    ]
    assert mod.is_dependabot_dependency_only(files) is False


def test_linked_spec_must_be_in_changed_specs() -> None:
    files = {
        "docs/specs/01-other-spec.md",
        "docs/specs/02-second-spec.md",
    }
    assert "docs/specs/03-linked-spec.md" not in files


def test_missing_acs_can_be_compared_against_spec_ids(tmp_path: Path) -> None:
    mod = _load_validate_pr_module()
    spec_file = tmp_path / "spec.md"
    spec_file.write_text(
        "\n".join(
            [
                "## Acceptance criteria",
                "- AC1: first requirement",
                "- AC2: second requirement",
                "- AC10: tenth requirement",
            ]
        ),
        encoding="utf-8",
    )
    body = """
- [x] AC1 done
"""
    missing = sorted(mod.spec_ac_ids(str(spec_file)) - mod.checked_ac_ids(body))
    assert missing == ["AC10", "AC2"]


def test_test_plan_path_matches_spec_slug() -> None:
    mod = _load_validate_pr_module()
    assert (
        mod.test_plan_path_for_spec("docs/specs/03-linked-spec.md")
        == "docs/test-plans/03-linked-spec.md"
    )


def test_pr_draft_path_matches_spec_slug() -> None:
    mod = _load_validate_pr_module()
    assert (
        mod.pr_draft_path_for_spec("docs/specs/03-linked-spec.md")
        == ".ai/pr-description/03-linked-spec.md"
    )


def test_artifact_has_spec_link_detects_matching_spec(tmp_path: Path) -> None:
    mod = _load_validate_pr_module()
    draft_file = tmp_path / "03-linked-spec.md"
    draft_file.write_text(
        "\n".join(
            [
                "## Spec",
                "- Spec: docs/specs/03-linked-spec.md",
            ]
        ),
        encoding="utf-8",
    )
    assert mod.artifact_has_spec_link(str(draft_file), "docs/specs/03-linked-spec.md") is True


def test_artifact_checked_ac_ids_reads_from_file(tmp_path: Path) -> None:
    mod = _load_validate_pr_module()
    draft_file = tmp_path / "03-linked-spec.md"
    draft_file.write_text(
        "\n".join(
            [
                "## Acceptance Criteria",
                "- [x] AC1 done",
                "- [X] AC2 done",
                "- [ ] AC3 pending",
            ]
        ),
        encoding="utf-8",
    )
    assert mod.artifact_checked_ac_ids(str(draft_file)) == {"AC1", "AC2"}


def test_has_numbered_packet_name_requires_two_digit_prefix() -> None:
    mod = _load_validate_pr_module()
    assert mod.has_numbered_packet_name("docs/specs/03-linked-spec.md") is True
    assert mod.has_numbered_packet_name("docs/specs/linked-spec.md") is False
