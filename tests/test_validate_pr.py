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
        "docs/specs/new-feature.md",
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
- Link to docs/specs/first-spec.md
- Backup link docs/specs/second-spec.md
"""
    assert mod.extract_spec_link(body) == "docs/specs/first-spec.md"


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
        "docs/specs/feature-a.md",
        "docs/specs/feature-b.md",
    ]
    assert mod.changed_specs(files) == {
        "docs/specs/feature-a.md",
        "docs/specs/feature-b.md",
    }


def test_linked_spec_must_be_in_changed_specs() -> None:
    files = {
        "docs/specs/other-spec.md",
        "docs/specs/second-spec.md",
    }
    assert "docs/specs/linked-spec.md" not in files


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
        mod.test_plan_path_for_spec("docs/specs/linked-spec.md") == "docs/test-plans/linked-spec.md"
    )
