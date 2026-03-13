import unittest
from pathlib import Path

from scripts.lib.system_model import (
    ValidationError,
    advance_system,
    ensure_valid_system,
    next_stage_id,
)


def build_system(current_status="done"):
    return {
        "name": "Test System",
        "type": "demo",
        "objective": "Test the factory.",
        "current_stage": "intake",
        "status": "in_progress",
        "inputs": [{"name": "input", "description": "demo"}],
        "outputs": [{"name": "output", "description": "demo"}],
        "dependencies": ["dep"],
        "acceptance_criteria": ["ship"],
        "open_questions": ["open?"],
        "stages": [
          {
            "id": "intake",
            "name": "Intake",
            "description": "test",
            "status": current_status,
            "definition_of_done": ["a"]
          },
          {
            "id": "scaffold",
            "name": "Scaffold",
            "description": "test",
            "status": "planned",
            "definition_of_done": ["b"]
          },
          {
            "id": "contracts",
            "name": "Contracts",
            "description": "test",
            "status": "planned",
            "definition_of_done": ["c"]
          },
          {
            "id": "core-logic",
            "name": "Core",
            "description": "test",
            "status": "planned",
            "definition_of_done": ["d"]
          },
          {
            "id": "exports",
            "name": "Exports",
            "description": "test",
            "status": "planned",
            "definition_of_done": ["e"]
          },
          {
            "id": "tests",
            "name": "Tests",
            "description": "test",
            "status": "planned",
            "definition_of_done": ["f"]
          },
          {
            "id": "hardening",
            "name": "Hardening",
            "description": "test",
            "status": "planned",
            "definition_of_done": ["g"]
          },
          {
            "id": "docs",
            "name": "Docs",
            "description": "test",
            "status": "planned",
            "definition_of_done": ["h"]
          },
          {
            "id": "release",
            "name": "Release",
            "description": "test",
            "status": "planned",
            "definition_of_done": ["i"]
          },
        ],
    }


class SystemModelTests(unittest.TestCase):
    def test_next_stage_requires_done(self):
        system = build_system(current_status="in_progress")
        ensure_valid_system(system)
        self.assertIsNone(next_stage_id(system))

    def test_next_stage_when_done(self):
        system = build_system(current_status="done")
        ensure_valid_system(system)
        self.assertEqual(next_stage_id(system), "scaffold")

    def test_unknown_stage_rejected(self):
        system = build_system()
        system["current_stage"] = "unknown"
        with self.assertRaises(ValidationError):
            ensure_valid_system(system)

    def test_advance_marks_next_stage_in_progress(self):
        system = build_system(current_status="done")
        result = advance_system(system)
        self.assertTrue(result.changed)
        self.assertEqual(system["current_stage"], "scaffold")
        next_stage = next(
            s for s in system["stages"] if s["id"] == "scaffold"
        )
        self.assertEqual(next_stage["status"], "in_progress")

    def test_advance_final_stage_marks_complete(self):
        system = build_system(current_status="done")
        system["current_stage"] = "release"
        for stage in system["stages"]:
            stage["status"] = "done"
        result = advance_system(system)
        self.assertTrue(result.completed)
        self.assertEqual(system["status"], "complete")


if __name__ == "__main__":
    unittest.main()
