# Playbook: Add Core Logic

Goal: implement the main execution path that satisfies the contracts.

## Steps
- Confirm `current_stage` is `core-logic`; review contracts and acceptance criteria.
- Implement the happy path with deterministic outputs.
- Add minimal logging or artifacts for reproducibility.
- Keep changes scoped to the core flow; defer optimizations.
- Run validation and any available tests.

## Definition of done
- Core path runs end-to-end against contracted inputs/outputs.
- Deterministic behavior with stable artifacts.
- Risks and edge cases noted for later stages.
- Stage status set to `done` with a brief handoff in the PR.
