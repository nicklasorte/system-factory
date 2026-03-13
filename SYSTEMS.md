# System Lifecycle Model

Each system is defined in a YAML file ending with `.system.yaml`. The file is the single source of truth for state, contracts, and stage progress.

## Required fields
- `name`, `type`, `objective`: Human-readable identifiers.
- `current_stage`: One of the canonical stages below.
- `status`: `planned`, `in_progress`, `blocked`, or `complete`.
- `stages`: Ordered list matching the canonical stage order.
- `inputs`, `outputs`, `dependencies`, `acceptance_criteria`, `open_questions`: Lists describing the system context.

See `schema/system.schema.yaml` for a machine-readable definition and `templates/system-template.yaml` for a starter file.

## Canonical stages
1. intake
2. scaffold
3. contracts
4. core-logic
5. exports
6. tests
7. hardening
8. docs
9. release

`current_stage` must appear in the stage list. A stage is “complete” when its `status` is `done` and its `definition_of_done` items are satisfied in the PR that closed it. CI advances to the next stage once a merged PR marks the current stage `done`.

## Stage fields
Required per stage: `id`, `name`, `description`, `status`, `definition_of_done`.
Optional helpers: `required_files`, `checks`, `non_goals`, `outputs`, `next_hint`.

## Progression rules
- Only one active stage at a time; work the `current_stage`.
- To advance, set the `current_stage` stage `status` to `done` in the PR.
- After merge, `advance-on-merge` updates `current_stage`, flips the next stage to `in_progress`, and opens the next issue (or a completion issue when `release` is done).

## File locations
- Systems under active development live in `systems/`.
- Worked examples live in `examples/`.
- The template lives in `templates/system-template.yaml`.
