# Contracts

This repository follows the canonical artifact contracts defined in `spectrum-systems`. It must not redefine or fork those contracts locally. Instead, it declares how it consumes and/or produces artifacts under those contracts.

What this repo does:
- Adopts canonical contracts from `spectrum-systems` (see `config/contracts.yaml`).
- Does not redefine canonical schemas; any local fixtures must be temporary and clearly marked.
- May consume, validate, transform, or emit artifacts under the canonical contracts in `consume_and_produce` mode.
- Any local repo-specific extensions must be documented, bounded in scope, and reconciled upstream.

Contract declaration (machine-readable):
- `config/contracts.yaml` lists `consumed_artifact_types`, `produced_artifact_types`, `supported_contract_versions`, `standards_dependency`, and enforcement mode.
- `contracts/` contains integration notes and placeholders for adapters pointing at `spectrum-systems`.

Alignment tasks:
- Keep `standards_source_repo` pinned to `spectrum-systems` and track `standards_source_version` changes.
- Validate input artifacts before processing and validate outputs before export.
- When standards drift, update the pinned version, re-run validations, and record provenance in `config/provenance.yaml`.
