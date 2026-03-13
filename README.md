# System Factory

System Factory turns this repository into the source of truth for agent-driven system delivery. Every system is expressed as a machine-readable YAML file, advanced stage by stage through GitHub issues and pull requests, and validated in CI.

## How it works
- Describe a new system with a lifecycle file (`*.system.yaml`) that follows `schema/system.schema.yaml`.
- Agents work on the current stage only, open a PR, and mark the stage `done`.
- When the PR merges, automation advances the lifecycle, commits the updated state, and opens the next stage issue until release.

## Quick start
1) Seed a system (manual workflow):
   - Trigger **Seed System** in GitHub Actions with the name, type, and objective.
   - The workflow creates `systems/<slug>.system.yaml`, validates it, opens the intake issue, and raises a PR with the new file.
2) Validate any system file locally:
   ```bash
   python -m pip install -r requirements.txt
   python scripts/system_factory.py validate --all
   ```
3) Render the next-stage issue for a system:
   ```bash
   python scripts/system_factory.py render-issue --file examples/working-paper-review-engine.system.yaml
   ```
4) Compute the next stage (after marking the current one `done`):
   ```bash
   python scripts/system_factory.py next-stage --file systems/<slug>.system.yaml
   ```

## Repository map
- `schema/` – canonical lifecycle schema.
- `templates/` – starter system template.
- `examples/` – sample systems showing progression.
- `scripts/` – CLI for creating, validating, advancing, and rendering issues.
- `playbooks/` – stage-specific guidance.
- `.github/` – instructions, issue templates, and workflows.

## End-to-end example
1) Seed the “Working Paper Review Engine”.
2) Intake issue guides capturing objectives and dependencies.
3) PR updates the system file; `validate-system-files` checks YAML.
4) Merge triggers `advance-on-merge`, which advances to `scaffold`, updates the system file, and opens the scaffold issue.
5) Repeat until the `release` stage is completed; a completion issue is opened.

## Tests
Run lightweight tests after installing dependencies:
```bash
python -m unittest
```
