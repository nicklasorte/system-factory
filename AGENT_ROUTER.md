# Agent Router

Use this router to decide how to engage agents on a task.

## Principles
- Always read the relevant `*.system.yaml` first; it is the source of truth.
- Only work on the `current_stage`. Do not refactor unrelated areas.
- Keep outputs deterministic and diff-friendly.
- Leave clear handoff notes and update status artifacts before exiting.
- Prefer small, reviewable PRs.

## Which agent to use
- **Codex (this repo)**: Primary for structured coding, schema work, and CI updates.
- **Copilot**: Inline completions inside an active PR when you already know what to build.
- **Claude**: For broader synthesis or when drafting docs/playbooks that need tone and structure.

## Workflow
1. Load the system file and confirm `current_stage` and `definition_of_done`.
2. Open or pick up the stage issue created by automation.
3. Make changes scoped to that stage; update the system file status when done.
4. Run available validation/tests.
5. Submit a small PR with handoff notes describing what changed and what is next.

## Choosing the next step
Automation advances stages when the merged PR sets the current stage `status: done`. If you are blocked, open a `blocked-decision` issue with the context and options.
