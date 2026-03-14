# Architecture

This {{REPO_ROLE}} is anchored to the canonical standards published in `{{STANDARDS_REPO}}` and governed by `{{GOVERNING_REPO}}`. It inherits artifact contracts rather than redefining them. The architecture assumes:

- Contract mode: {{CONTRACT_MODE}} – this repo will {{CONTRACT_MODE}} artifacts defined upstream.
- System layer: {{SYSTEM_LAYER}}
- Primary artifact types: {{PRIMARY_ARTIFACT_TYPES}}
- Supported contract versions: {{SUPPORTED_CONTRACT_VERSIONS}}

Flow expectations:
- Load canonical contracts from `{{STANDARDS_REPO}}` (see `config/contracts.yaml` for reference and version pins).
- Validate incoming artifacts against the canonical schemas before processing.
- Transform or orchestrate work while preserving provenance (`config/provenance.yaml`).
- Validate outbound artifacts before export and fail cleanly on mismatches.

Adapters and validation stubs live in `validation/contract_validation.py` and should be extended to pull the canonical schemas from `{{STANDARDS_REPO}}` at the pinned reference. Avoid copying schema content into this repo; rely on the source of truth instead.
