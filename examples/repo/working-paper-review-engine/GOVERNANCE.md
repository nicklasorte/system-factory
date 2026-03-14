# Governance

This repository participates in the spectrum-systems “czar” architecture. Canonical rules, schemas, and contracts live in `spectrum-systems`; this repo consumes them and stays aligned.

Expectations:
- Keep `standards_dependency` set to `spectrum-systems` and honor `standards_enforcement=required`.
- Do not fork canonical contracts; propose upstream changes instead.
- Record provenance for every run using `config/provenance.yaml` and keep contract declarations current in `config/contracts.yaml`.
- When standards change, bump `standards_source_version`, revalidate, and document the diff in PR notes.

Roles:
- engine_repo owners enforce contract compliance and provenance.
- Upstream changes belong in `spectrum-systems`; local changes should remain temporary and well-scoped.
