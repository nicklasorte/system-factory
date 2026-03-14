# Working Paper Review Engine

Role: engine_repo  
Contract mode: consume_and_produce  
System layer: Engine  
Governance bootstrap: enabled (SSOS control-plane assets applied)  
Governing repo: nicklasorte/spectrum-systems  
Standards: nicklasorte/spectrum-systems @ main

This repository is scaffolded by system-factory to be contract-aware from day one. It inherits canonical artifact contracts from `nicklasorte/spectrum-systems` and must not redefine them locally. Contract declarations live in `config/contracts.yaml`, provenance expectations in `config/provenance.yaml`, and validation stubs in `validation/contract_validation.py`.

Governance linkage: This repo is part of the SSOS / czar org and governed by `nicklasorte/spectrum-systems`. Local logic must not redefine canonical contracts or workflows without coordinating changes in that governing repo first.

Key docs:
- `CONTRACTS.md` – contract alignment and local extension policy
- `ARCHITECTURE.md` – how this repo consumes and emits artifacts under the contracts
- `GOVERNANCE.md` – linkage to the spectrum-systems “czar” repository
- `OPERATIONS.md` – operating guidance with provenance and validation checkpoints
- `SYSTEMS.md` – lifecycle notes and stage expectations

Start by reviewing `config/contracts.yaml` to confirm the declared `consumed_artifact_types` and `produced_artifact_types`. Keep the standards reference aligned with `nicklasorte/spectrum-systems`; do not fork canonical schemas here.
