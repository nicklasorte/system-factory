from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def test_baseline_governance_files_exist():
    for name in ["README.md", "CLAUDE.md", "CODEX.md", "SYSTEMS.md"]:
        assert (ROOT / name).exists()


def test_baseline_directories_exist():
    for rel in ["docs", "tests", "scripts", ".github/workflows"]:
        assert (ROOT / rel).exists()


def test_readme_links_to_standards_repo():
    readme_text = (ROOT / "README.md").read_text()
    assert "spectrum-systems" in readme_text


def test_repository_template_documents_structure():
    template_doc = (ROOT / "docs" / "repository-template.md").read_text()
    assert "README.md" in template_doc
    assert "spectrum-systems" in template_doc
    assert ".github/workflows" in template_doc
