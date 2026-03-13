import unittest
from pathlib import Path

from scripts.lib.issue_renderer import render_completion_issue, render_stage_issue


class IssueRendererTests(unittest.TestCase):
    def _system(self):
        return {
            "name": "Demo System",
            "type": "demo",
            "objective": "Test rendering.",
            "current_stage": "intake",
            "status": "in_progress",
            "inputs": [{"name": "in", "description": "demo"}],
            "outputs": [{"name": "out", "description": "demo"}],
            "dependencies": ["dep"],
            "acceptance_criteria": ["ship"],
            "open_questions": ["What next?"],
            "stages": [
                {
                    "id": "intake",
                    "name": "Intake",
                    "description": "Capture context",
                    "status": "done",
                    "required_files": ["schema/system.schema.yaml"],
                    "checks": ["validate"],
                    "definition_of_done": ["context captured"],
                    "next_hint": "Do scaffold",
                },
                {
                    "id": "scaffold",
                    "name": "Scaffold",
                    "description": "Scaffold repo",
                    "status": "planned",
                    "definition_of_done": ["files created"],
                },
                {
                    "id": "contracts",
                    "name": "Contracts",
                    "description": "Contracts",
                    "status": "planned",
                    "definition_of_done": ["contracts done"],
                },
                {
                    "id": "core-logic",
                    "name": "Core",
                    "description": "Core logic",
                    "status": "planned",
                    "definition_of_done": ["core done"],
                },
                {
                    "id": "exports",
                    "name": "Exports",
                    "description": "Exports",
                    "status": "planned",
                    "definition_of_done": ["exports done"],
                },
                {
                    "id": "tests",
                    "name": "Tests",
                    "description": "Tests",
                    "status": "planned",
                    "definition_of_done": ["tests done"],
                },
                {
                    "id": "hardening",
                    "name": "Hardening",
                    "description": "Hardening",
                    "status": "planned",
                    "definition_of_done": ["hardening done"],
                },
                {
                    "id": "docs",
                    "name": "Docs",
                    "description": "Docs",
                    "status": "planned",
                    "definition_of_done": ["docs done"],
                },
                {
                    "id": "release",
                    "name": "Release",
                    "description": "Release",
                    "status": "planned",
                    "definition_of_done": ["release done"],
                },
            ],
        }

    def test_render_stage_issue_includes_goal_and_files(self):
        system = self._system()
        title, body = render_stage_issue(system, stage_id="scaffold", system_file=Path("systems/demo.system.yaml"))
        self.assertIn("Scaffold", title)
        self.assertIn("Required Files", body)
        self.assertIn("systems/demo.system.yaml", body)

    def test_completion_issue(self):
        system = self._system()
        title, body = render_completion_issue(system)
        self.assertIn("Release", title)
        self.assertIn("Summary", body)


if __name__ == "__main__":
    unittest.main()
