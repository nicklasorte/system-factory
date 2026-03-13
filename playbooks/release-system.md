# Playbook: Release System

Goal: finalize the system, verify artifacts, and capture follow-ups.

## Steps
- Confirm `current_stage` is `release` and all prior stages are `done`.
- Run validation and tests; ensure outputs are reproducible.
- Draft release notes and completion summary.
- Close or move remaining open questions to follow-up issues.
- Update system status to `complete` when the final stage is done.

## Definition of done
- Validation passes; artifacts and docs match the released behavior.
- Completion issue opened automatically after merge.
- Handoff notes include next opportunities or maintenance items.
