# {{REPO_NAME}}

Role: {{REPO_ROLE}}  
Contract mode: {{CONTRACT_MODE}}  
Standards: {{STANDARDS_REPO}} @ {{STANDARDS_VERSION}}

This repository is scaffolded by system-factory to be contract-aware from day one. It inherits canonical artifact contracts from `{{STANDARDS_REPO}}` and must not redefine them locally. Contract declarations live in `config/contracts.yaml`, provenance expectations in `config/provenance.yaml`, and validation stubs in `validation/contract_validation.py`.

Key docs:
- `CONTRACTS.md` – contract alignment and local extension policy
- `ARCHITECTURE.md` – how this repo consumes and emits artifacts under the contracts
- `GOVERNANCE.md` – linkage to the spectrum-systems “czar” repository
- `OPERATIONS.md` – operating guidance with provenance and validation checkpoints
- `SYSTEMS.md` – lifecycle notes and stage expectations

Start by reviewing `config/contracts.yaml` to confirm the declared `consumed_artifact_types` and `produced_artifact_types`. Keep the standards reference aligned with `{{STANDARDS_REPO}}`; do not fork canonical schemas here.
