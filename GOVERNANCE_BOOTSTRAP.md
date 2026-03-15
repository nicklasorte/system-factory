# SSOS Governance Bootstrap

System Factory now bootstraps SSOS governance for every scaffolded repository so new repos inherit the control-plane standards from `nicklasorte/spectrum-systems` by default.

## Options (factory contract)
- `include_governance_bootstrap` – include SSOS governance assets (default: true).
- `include_project_automation` – render `.github/workflows/ssos-project-automation.yml` with `{{GITHUB_PROJECT_NUMBER}}`.
- `include_issue_templates` – render SSOS issue templates under `.github/ISSUE_TEMPLATE/`.
- `include_label_script` – render `scripts/setup-labels.sh` to align labels across repos.
- `governing_repo` – governing source for schemas and rules (default: `nicklasorte/spectrum-systems`).
- `github_project_number` – optional project number used by automation.
- `system_layer` – one of `Factory | Governance | Orchestrator | Engine | Knowledge | Advisor`.
- `preset` – classification preset that sets sensible defaults for the above flags.

CLI flags mirror these options: `--include-governance-bootstrap` / `--skip-governance-bootstrap`, `--include-project-automation`, `--include-issue-templates`, `--include-label-script`, `--governing-repo`, `--github-project-number`, `--system-layer`, `--preset`.

## Baseline governance scaffold (always on)
- New repos always include README/CLAUDE/CODEX/SYSTEMS tied to the governing repo, `docs/repository-template.md` describing the governed layout, seeded `docs/`, `tests/`, and `scripts/` directories, and `.github/workflows/tests.yml` that installs dev dependencies and runs `pytest`.
- `tests/test_structure.py` ships with each scaffold to keep the governance layout aligned with `nicklasorte/spectrum-systems` even if control-plane assets are toggled.
- Place design-review artifacts under `docs/design-reviews/` and map them to canonical artifact contracts in `spectrum-systems`; declare any new artifact types in `config/contracts.yaml`.

## Presets
- `engine` → `role=engine_repo`, governance bootstrap on, project automation on, label script on, layer `Engine`.
- `orchestrator` → `role=orchestration_repo`, governance bootstrap on, project automation on, label script on, layer `Orchestrator`.
- `advisor` → `role=analysis_repo`, governance bootstrap on, project automation on, label script on, layer `Advisor`.
- `governance` → `role=standards_repo`, governance bootstrap on, project automation on, label script off, layer `Governance`.
- `knowledge` → `role=library_repo`, governance bootstrap on, project automation on, label script on, layer `Knowledge`.

## Canonical vs repo-local
- Canonical: schemas, contracts, and GitHub operating standards in `nicklasorte/spectrum-systems` (governing repo).
- Repo-local: rendered docs (README, AGENTS, CLAUDE, CODEX), issue templates, automation workflow, label script, metadata docs. Local repos must not redefine canonical contracts—propose changes upstream first.

## Customize or disable
- Skip control-plane assets with `--skip-governance-bootstrap` or disable specific pieces with `--skip-project-automation`, `--skip-issue-templates`, or `--skip-label-script`.
- Update `--governing-repo` or `--github-project-number` when pointing at different control planes.
- Keep governance linkage text in README/AGENTS/CLAUDE/CODEX aligned with the governing repo whenever options change.

## Examples
```bash
# Engine repo with full SSOS bootstrap
python scripts/system_factory.py scaffold-repo --name "Working Paper Review Engine" --role engine_repo --preset engine --github-project-number 99

# Orchestrator without label script
python scripts/system_factory.py scaffold-repo --name "Coordination Hub" --role orchestration_repo --preset orchestrator --skip-label-script

# Advisor repo pointing at a different governance source
python scripts/system_factory.py scaffold-repo --name "Advisory Notes" --role analysis_repo --preset advisor --governing-repo other-org/spectrum-systems
```
