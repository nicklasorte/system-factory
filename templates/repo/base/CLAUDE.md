# Claude Instructions

- Stay within the role `{{REPO_ROLE}}` and respect contract mode `{{CONTRACT_MODE}}` and system layer `{{SYSTEM_LAYER}}`.
- Treat `{{GOVERNING_REPO}}` as the governing source for schemas, contracts, and GitHub operating rules; do not fork them locally.
- Keep docs and playbooks concise, actionable, and aligned with `config/contracts.yaml`, `config/provenance.yaml`, and governance bootstrap assets.
- Record open questions and next steps in context with contract and provenance updates, including upstream actions in `{{GOVERNING_REPO}}`.
- Note standards reference changes (`{{STANDARDS_VERSION}}`) and governance alignment (`{{GOVERNANCE_BOOTSTRAP_STATUS}}`) in handoffs and PR descriptions.
