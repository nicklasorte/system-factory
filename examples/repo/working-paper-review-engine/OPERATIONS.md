# Operations

Operating mode: engine_repo (consume_and_produce)  
Standards dependency: spectrum-systems @ main

Operational checklist:
- Review `config/contracts.yaml` before work to confirm consumed/produced artifact types and standards reference.
- Capture provenance in `config/provenance.yaml` for every run (source inputs, run_id, standards version, outputs, timestamps).
- Use `validation/contract_validation.py` to load canonical contracts from `spectrum-systems` and block mismatches early.
- Keep local fixtures bounded; replace them with references to canonical contracts as soon as possible.
- Update `standards_source_version` when upstream changes land, and re-run validation before releasing.

Runbook hooks:
- Input validation: ensure artifacts match `consumed_artifact_types` before orchestration/engine steps.
- Output validation: verify produced artifacts against supported contract versions prior to export.
- Failure policy: fail fast on contract drift and document remediation in PR notes.
