# System Factory Architecture

System Factory now scaffolds contract-aware repositories that align with the `spectrum-systems` “czar” standards. The factory itself does not define canonical contracts; it wires generated repos to consume them.

Key concepts:
- Repo roles: `standards_repo`, `engine_repo`, `orchestration_repo`, `library_repo`, `analysis_repo` (see `templates/repo-roles.yaml`).
- Standards dependency: generated repos point at `spectrum-systems` for canonical schemas, provenance definitions, and governance.
- Contract declarations: every scaffold ships `config/contracts.yaml` with `consumed_artifact_types`, `produced_artifact_types`, `supported_contract_versions`, `standards_source_repo`, and enforcement settings.
- Provenance: `config/provenance.yaml` captures source inputs, run_id, standards version, outputs, and timestamps; align with `provenance_record` in `spectrum-systems`.
- Validation: `validation/contract_validation.py` provides stubs for loading canonical contracts and validating input/output artifacts.
- Docs: scaffolds include `CONTRACTS.md`, `ARCHITECTURE.md`, `GOVERNANCE.md`, `OPERATIONS.md`, `SYSTEMS.md`, `CODEX.md`, `CLAUDE.md`, and `docs/repository-template.md` that describe czar alignment, governed layout (docs/tests/scripts/.github), and forbid local contract redefinition.
- CI and validation: `.github/workflows/tests.yml` installs dev dependencies and runs `pytest`, with seeded `tests/test_structure.py` to guard the governance template; workflows remain deterministic even when governance bootstrap flags are toggled.

Responsibility boundaries:
- `spectrum-systems` remains the single source of truth for canonical contracts and governance.
- `system-factory` only scaffolds compatibility and wiring; it never forks canonical schemas.
- Generated repos must keep their standards reference pinned and validated before shipping changes.
