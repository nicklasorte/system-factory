# Constitution Integration

This template assumes every operational engine inherits its governance from the `spectrum-systems` constitution. The `config/constitution.yaml` file pins the source repository, reference, and the specific artifacts each engine must honor.

## Setup
- Pin a working copy of `spectrum-systems` at the `constitution.source.reference` listed in `config/constitution.yaml`.
- Wire the artifacts under `governance` into your engine pipeline (rules profile, prompt registry, provenance standard, error taxonomy, and architectural contracts).
- Implement adapters in `src/` that load these artifacts and block or log deviations early in the request flow.

## Ongoing checks
- Before merging, confirm `config/constitution.yaml` still points to a valid ref and matches the expected profiles in `spectrum-systems`.
- When the constitution changes, bump `constitution.source.reference`, rerun engine tests, and document any migration notes in the PR description.
- If a temporary exception is required, note it and add a cleanup task to restore alignment.

## Verification
- Keep CI coverage that validates references and schema parity with `spectrum-systems`.
- Update `sync.last_synced_ref` after each verified sync so the next maintainer knows the provenance of the wiring.
