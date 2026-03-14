# GitHub Operations (SSOS)

This repository is part of the SSOS / czar org. Governance and canonical contracts live in `{{GOVERNING_REPO}}`; keep this linkage explicit and current.

What this adds:
- Issue templates under `.github/ISSUE_TEMPLATE/` that require governance alignment.
- Project automation workflow `.github/workflows/ssos-project-automation.yml` (set `PROJECT_AUTOMATION_TOKEN` and `{{GITHUB_PROJECT_NUMBER}}`).
- Label bootstrap script `scripts/setup-labels.sh` to align labels across repos.

Expectations:
- Do not redefine canonical contracts here; propose changes in `{{GOVERNING_REPO}}` first.
- Keep project automation enabled unless explicitly waived; it links work to the SSOS control plane.
- When disabling automation, document the reason and the compensating control.
