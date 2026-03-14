# Architecture

This engine_repo is anchored to the canonical standards published in `spectrum-systems`. It inherits artifact contracts rather than redefining them. The architecture assumes:

- Contract mode: consume_and_produce – this repo will consume_and_produce artifacts defined upstream.
- Primary artifact types: working_paper_markdown, review_packet
- Supported contract versions: v1

Flow expectations:
- Load canonical contracts from `spectrum-systems` (see `config/contracts.yaml` for reference and version pins).
- Validate incoming artifacts against the canonical schemas before processing.
- Transform or orchestrate work while preserving provenance (`config/provenance.yaml`).
- Validate outbound artifacts before export and fail cleanly on mismatches.

Adapters and validation stubs live in `validation/contract_validation.py` and should be extended to pull the canonical schemas from `spectrum-systems` at the pinned reference. Avoid copying schema content into this repo; rely on the source of truth instead.
