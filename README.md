# System Factory

System Factory keeps repo-based AI systems as deterministic YAML lifecycles. Each system moves stage by stage through clear definitions of done, local CLI commands, and CI guardrails.

## Run the demo (Working Paper Review Engine)
1) Install dependencies  
   `python -m pip install -r requirements.txt`
2) Validate the canonical system  
   `python scripts/system_factory.py validate --file systems/working-paper-review-engine.system.yaml`
3) Render the current stage issue (core-engine)  
   `python scripts/system_factory.py render-issue --file systems/working-paper-review-engine.system.yaml --stage core-engine`  
   A deterministic example lives at `examples/issues/working-paper-review-engine_core-engine.md`.
4) Mark the stage done  
   Edit `systems/working-paper-review-engine.system.yaml` to set the `core-engine` stage `status` to `done` (leave `current_stage` as `core-engine` until you advance).
5) Advance to the next stage  
   `python scripts/system_factory.py advance --files systems/working-paper-review-engine.system.yaml`  
   The CLI updates the system file and prints the next-stage issue content when it changes.

## CLI reference
- `create` – render a system file from `templates/system-template.yaml`.
- `validate` – validate one or all system files against `schema/system.schema.yaml`.
- `render-issue` – render the current or named stage issue body (use `--output` to write a file).
- `next-stage` – print the next stage id if the current one is `done`.
- `advance` – update `current_stage`, flip the next stage to `in_progress`, and emit issue payloads.

## Repository map
- `systems/` – canonical working slice (`working-paper-review-engine.system.yaml`).
- `examples/` – additional sample systems plus rendered issue fixtures.
- `schema/` – lifecycle schema and stage order.
- `templates/` – starter system template with the canonical stages.
- `scripts/` – CLI (`system_factory.py`) and helpers.
- `tests/` – unit tests for validation, advancement, and rendering.
- `playbooks/` – stage-specific guidance (`bootstrap-system`, `add-contracts`, `add-core-engine`, `review-hardening`, `release-system`).
- `.github/workflows/` – validation and advance-on-merge automation.

## Workflows
- `validate-system-files` runs on pushes and PRs touching lifecycle files or tooling.
- `advance-on-merge` (optional) advances systems touched in a merged PR and opens the next-stage issue.

## Tests
After installing dependencies, run:
```bash
python -m unittest discover -s tests -p "test_*.py"
```
