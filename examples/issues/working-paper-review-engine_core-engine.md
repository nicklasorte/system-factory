## Goal
Implement review aggregation, scoring, and lifecycle automation.

## Required Files
- systems/working-paper-review-engine.system.yaml
- scripts/system_factory.py
- scripts/lib/system_model.py
- scripts/lib/issue_renderer.py
- tests/test_system_model.py
- tests/test_issue_renderer.py
- examples/issues/working-paper-review-engine_core-engine.md

## Non-Goals
- (none)

## Checks
- Validation errors surface missing or duplicate stages clearly
- Issue rendering is deterministic for this system file
- Advancement blocked unless current stage is done

## Definition of Done
- CLI validate/render/advance succeed on this system file
- Deterministic issue fixture updated
- Next stage remains planned until this stage is done

## Context
- Objective: Automate draft paper reviews with crisp accept/block decisions and evidence.
- Current Stage: core-engine
- System Status: in_progress
- Inputs: paper_markdown, review_guidelines
- Outputs: review_packet, risk_log
- Dependencies: Access to source drafts, Stable prompt guidelines

## Open Questions
- How should conflicting reviewer feedback be resolved?
- Which signals drive block versus accept?

## Next Stage Hint
Add regression coverage and operator notes.
