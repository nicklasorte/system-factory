# Governed Repository Template

System Factory (Layer 1) generates repositories that inherit constitutional rules from `spectrum-systems` (Layer 2) so operational engines (Layer 3) stay aligned by default.

Expected layout in generated repos:
- README.md – references the governing standards in `spectrum-systems`.
- CLAUDE.md – agent operating guidance.
- CODEX.md – developer guardrails and deterministic editing guidance.
- SYSTEMS.md – lifecycle alignment and stage expectations.
- docs/ – repository guidance plus design-review artifacts that reference canonical contracts from `spectrum-systems`.
- tests/ – pytest harness seeded with baseline structure checks.
- scripts/ – automation hooks such as label bootstrap that stay linked to the governing repo.
- .github/workflows/ – CI that installs dev dependencies and runs `pytest`.

Design-review compatibility:
- Place design-review artifacts under `docs/design-reviews/` (or similar) and map them to the canonical artifact contracts published in `spectrum-systems` before merging changes.
- Declare any new artifact types in `config/contracts.yaml` so downstream engines can validate against the same governance rules.
