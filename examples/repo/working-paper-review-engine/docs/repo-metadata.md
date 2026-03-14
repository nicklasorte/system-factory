# Repository Metadata

- Repo: Working Paper Review Engine (working-paper-review-engine)
- System layer: Engine
- Governing repo: nicklasorte/spectrum-systems
- Governance bootstrap: enabled (SSOS control-plane assets applied)
- Recommended labels: ssos, engine, governance-aligned, contract-checked
- Automation hooks: project_sync, label_bootstrap, governance_checks
- Recommended docs to keep fresh: governance_linkage, contracts, operations, provenance

Guidance:
- Keep the governing repo reference current; update both docs and automation when the source changes.
- Record contract and standards versions in `config/contracts.yaml` and provenance for every release.
- Link issues and PRs to the SSOS project defined in `99` when automation is enabled.
- Metadata notes:
  - Primary artifacts should declare consumed and produced contracts.
  - Keep compatibility notes synced with spectrum-systems releases.
