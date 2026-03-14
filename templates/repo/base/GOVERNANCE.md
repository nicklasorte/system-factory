# Governance

This repository participates in the spectrum-systems “czar” architecture. Canonical rules, schemas, and contracts live in `{{GOVERNING_REPO}}` and `{{STANDARDS_REPO}}`; this repo consumes them and stays aligned.

Expectations:
- Keep `standards_dependency` set to `{{STANDARDS_REPO}}` and honor `standards_enforcement={{STANDARDS_ENFORCEMENT}}`.
- Do not fork canonical contracts or GitHub operating rules; propose upstream changes in `{{GOVERNING_REPO}}` instead.
- Record provenance for every run using `config/provenance.yaml` and keep contract declarations current in `config/contracts.yaml`.
- When standards change, bump `standards_source_version`, revalidate, and document the diff in PR notes.

Roles:
- {{REPO_ROLE}} owners enforce contract compliance and provenance.
- Upstream changes belong in `{{GOVERNING_REPO}}`; local changes should remain temporary and well-scoped.
