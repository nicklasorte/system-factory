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
- `list-roles` – list contract-aware repo roles supported by system-factory.
- `scaffold-repo` – scaffold a contract-aware repository for a given role (engine_repo, orchestration_repo, standards_repo, library_repo, analysis_repo).

## Repository map
- `systems/` – canonical working slice (`working-paper-review-engine.system.yaml`).
- `examples/` – additional sample systems plus rendered issue fixtures.
- `examples/repo/` – contract-aware scaffold examples (e.g., working-paper-review-engine).
- `schema/` – lifecycle schema and stage order.
- `templates/system-template.yaml` – starter system template with the canonical stages.
- `templates/repo-roles.yaml` – registry of repo roles and contract defaults.
- `templates/repo/base/` – contract-aware repo scaffold (docs, contract declarations, provenance, validation stubs).
- `templates/constitution-linked-engine/` – scaffold for operational engines pre-wired to the `spectrum-systems` constitution with compatibility and versioning policies.
- `scripts/` – CLI (`system_factory.py`) and helpers.
- `tests/` – unit tests for validation, advancement, rendering, and repo scaffolding.
- `playbooks/` – stage-specific guidance (`bootstrap-system`, `add-contracts`, `add-core-engine`, `review-hardening`, `release-system`).
- `.github/workflows/` – validation and advance-on-merge automation.

## Czar-aligned, contract-aware scaffolding
System Factory now generates repositories that are contract-aware by default and aligned with the `spectrum-systems` “czar” repository. New scaffolds:
- Declare repo roles (`standards_repo`, `engine_repo`, `orchestration_repo`, `library_repo`, `analysis_repo`) in `templates/repo-roles.yaml`.
- Carry machine-readable contract declarations (`config/contracts.yaml`) that point at canonical contracts in `spectrum-systems`.
- Include provenance placeholders (`config/provenance.yaml`) and validation stubs (`validation/contract_validation.py`) to enforce contracts for both inputs and outputs.
- Ship documentation templates (`CONTRACTS.md`, `ARCHITECTURE.md`, `GOVERNANCE.md`, `OPERATIONS.md`, `SYSTEMS.md`, `CODEX.md`, `CLAUDE.md`) that explain the czar alignment and forbid redefining canonical contracts.

Example: to scaffold an engine repo:
```bash
python scripts/system_factory.py scaffold-repo --name "Working Paper Review Engine" --role engine_repo --output scaffolds
```
This produces `scaffolds/working-paper-review-engine` with contract declarations, provenance placeholders, validation stubs, and czar-aware docs that point at `spectrum-systems`.

## SSOS governance bootstrap
- Repo scaffolds can include SSOS control-plane assets by default: issue templates, project automation, label bootstrap, and governance-linkage docs (README/AGENTS/CLAUDE/CODEX).
- New options: `--include-governance-bootstrap | --skip-governance-bootstrap`, `--include-project-automation`, `--include-issue-templates`, `--include-label-script`, `--governing-repo` (default `nicklasorte/spectrum-systems`), `--github-project-number`, `--system-layer`, and `--preset`.
- Presets live in `templates/repo-presets.yaml` (`engine`, `orchestrator`, `advisor`, `governance`, `knowledge`) and set sensible defaults for the flags above.
- See `GOVERNANCE_BOOTSTRAP.md` for defaults, disable/override guidance, and which files remain canonical in `nicklasorte/spectrum-systems`.
- Example output with governance bootstrap enabled: `examples/repo/working-paper-review-engine` (includes .github automation, labels script, metadata docs).

## Constitution-linked engines
Use `templates/constitution-linked-engine/` when creating an operational engine repository. It includes the constitution pin (`config/constitution.yaml`), integration guidance, compatibility policy, versioning/drift policy, and a `src/` stub for adapters that enforce the `spectrum-systems` contracts.

## Workflows
- `validate-system-files` runs on pushes and PRs touching lifecycle files or tooling.
- `advance-on-merge` (optional) advances systems touched in a merged PR and opens the next-stage issue.

## Tests
After installing dependencies, run:
```bash
python -m unittest discover -s tests -p "test_*.py"
```
