import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import yaml

from scripts.lib.repo_scaffolder import load_repo_roles, scaffold_repo


class RepoScaffoldingTests(unittest.TestCase):
    def test_roles_include_engine(self):
        roles = load_repo_roles(Path("templates/repo-roles.yaml"))
        self.assertIn("engine_repo", roles)
        self.assertEqual(roles["engine_repo"].standards_dependency, "spectrum-systems")
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
            self.assertEqual(data["repo"]["standards_dependency"], "spectrum-systems")
            self.assertIn("working_paper_markdown", "\n".join(data["contracts"]["consumed_artifact_types"]))
            self.assertIn("spectrum-systems", (repo_root / "CONTRACTS.md").read_text())
            self.assertIn("consume_and_produce", (repo_root / "ARCHITECTURE.md").read_text())
            self.assertIn(repo_root / "validation" / "contract_validation.py", created)


if __name__ == "__main__":
    unittest.main()
