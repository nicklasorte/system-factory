# Constitution-Linked Engine Source

Use this folder for the operational engine code that enforces the constitution link. Build adapters that:
- Load governance artifacts declared in `config/constitution.yaml`.
- Validate requests and outputs against the rules profile, prompt registry, provenance standard, error taxonomy, and architectural contracts.
- Emit provenance metadata so downstream systems can audit which constitution reference was applied.
