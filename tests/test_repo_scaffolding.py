import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import yaml

from scripts.lib.repo_scaffolder import load_repo_roles, scaffold_repo
from scripts.lib.system_model import slugify


class RepoScaffoldingTests(unittest.TestCase):
    def test_roles_include_engine(self):
        roles = load_repo_roles(Path("templates/repo-roles.yaml"))
        self.assertIn("engine_repo", roles)
        self.assertEqual(roles["engine_repo"].standards_dependency, "nicklasorte/spectrum-systems")
        self.assertEqual(roles["engine_repo"].contract_mode, "consume_and_produce")

    def test_scaffold_engine_creates_contract_assets(self):
        with TemporaryDirectory() as tmpdir:
            output_root = Path(tmpdir)
            created = scaffold_repo(
                name="Review Engine",
                role="engine_repo",
                output=output_root,
                contract_mode="consume_and_produce",
                primary_artifact_types=["working_paper_markdown", "review_packet"],
                standards_version="main",
            )
            repo_root = output_root / "review-engine"
            self.assertTrue((repo_root / "CONTRACTS.md").exists())
            self.assertTrue((repo_root / "config" / "provenance.yaml").exists())
            contracts_file = repo_root / "config" / "contracts.yaml"
            self.assertTrue(contracts_file.exists())
            data = yaml.safe_load(contracts_file.read_text())
            self.assertEqual(data["repo"]["contract_mode"], "consume_and_produce")
            self.assertEqual(data["repo"]["standards_dependency"], "nicklasorte/spectrum-systems")
            self.assertIn("working_paper_markdown", "\n".join(data["contracts"]["consumed_artifact_types"]))
            self.assertIn("nicklasorte/spectrum-systems", (repo_root / "CONTRACTS.md").read_text())
            self.assertIn("consume_and_produce", (repo_root / "ARCHITECTURE.md").read_text())
            self.assertIn(repo_root / "validation" / "contract_validation.py", created)
            self._assert_baseline_structure(repo_root)

    def _assert_governance_bootstrap(self, repo_root: Path):
        self.assertTrue((repo_root / ".github" / "ISSUE_TEMPLATE" / "artifact.yml").exists())
        self.assertTrue((repo_root / ".github" / "workflows" / "ssos-project-automation.yml").exists())
        self.assertTrue((repo_root / "scripts" / "setup-labels.sh").exists())
        self.assertTrue((repo_root / "docs" / "github-operations.md").exists())
        readme_text = (repo_root / "README.md").read_text()
        self.assertIn("Governance bootstrap: enabled", readme_text)
        self.assertIn("SSOS / czar org", readme_text)
        self.assertIn("nicklasorte/spectrum-systems", readme_text)
        workflow_text = (repo_root / ".github" / "workflows" / "ssos-project-automation.yml").read_text()
        self.assertIn("SSOS Project Automation", workflow_text)
        issue_template = (repo_root / ".github" / "ISSUE_TEMPLATE" / "artifact.yml").read_text()
        self.assertIn("nicklasorte/spectrum-systems", issue_template)

    def _assert_baseline_structure(self, repo_root: Path):
        for name in ["README.md", "CLAUDE.md", "CODEX.md", "SYSTEMS.md"]:
            self.assertTrue((repo_root / name).exists(), f"Missing baseline file: {name}")
        for rel in ["docs", "tests", "scripts", ".github/workflows"]:
            self.assertTrue((repo_root / rel).exists(), f"Missing baseline directory: {rel}")
        self.assertTrue((repo_root / ".github" / "workflows" / "tests.yml").exists())
        self.assertTrue((repo_root / "tests" / "test_structure.py").exists())
        template_doc = (repo_root / "docs" / "repository-template.md").read_text()
        self.assertIn("README.md", template_doc)
        self.assertIn("spectrum-systems", template_doc)
        self.assertIn(".github/workflows", template_doc)

    def test_engine_preset_includes_governance_bootstrap(self):
        with TemporaryDirectory() as tmpdir:
            created = scaffold_repo(
                name="Engine Gov Repo",
                role="engine_repo",
                output=Path(tmpdir),
                preset="engine",
                github_project_number="123",
            )
            repo_root = Path(tmpdir) / slugify("Engine Gov Repo")
            self._assert_governance_bootstrap(repo_root)
            self._assert_baseline_structure(repo_root)
            self.assertIn(repo_root / ".github" / "ISSUE_TEMPLATE" / "comment_matrix.yml", created)

    def test_orchestrator_preset_includes_governance_bootstrap(self):
        with TemporaryDirectory() as tmpdir:
            scaffold_repo(
                name="Coordination Hub",
                role="orchestration_repo",
                output=Path(tmpdir),
                preset="orchestrator",
            )
            repo_root = Path(tmpdir) / slugify("Coordination Hub")
            self._assert_governance_bootstrap(repo_root)
            self._assert_baseline_structure(repo_root)
            readme_text = (repo_root / "README.md").read_text()
            self.assertIn("System layer: Orchestrator", readme_text)

    def test_advisor_preset_includes_governance_bootstrap(self):
        with TemporaryDirectory() as tmpdir:
            scaffold_repo(
                name="Advisory Notes",
                role="analysis_repo",
                output=Path(tmpdir),
                preset="advisor",
            )
            repo_root = Path(tmpdir) / slugify("Advisory Notes")
            self._assert_governance_bootstrap(repo_root)
            self._assert_baseline_structure(repo_root)
            readme_text = (repo_root / "README.md").read_text()
            self.assertIn("System layer: Advisor", readme_text)


if __name__ == "__main__":
    unittest.main()
