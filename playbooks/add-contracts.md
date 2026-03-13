# Playbook: Add Contracts

Goal: define inputs, outputs, and acceptance rules clearly.

## Steps
- Confirm `current_stage` is `contracts` and review the preceding stages.
- Document input and output formats (schemas, examples, edge cases).
- Capture acceptance criteria for correctness, determinism, and failure handling.
- Update `definition_of_done` for downstream stages if contracts change scope.
- Validate: `python scripts/system_factory.py validate --file <path>`.

## Definition of done
- Inputs and outputs have concrete, reviewed formats.
- Acceptance criteria enumerate success, failure, and ambiguity handling.
- Open questions are updated or converted to follow-ups.
- Stage status set to `done` in the system file and referenced in the PR summary.
