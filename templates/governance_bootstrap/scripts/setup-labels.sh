#!/usr/bin/env bash
set -euo pipefail

REPO_SLUG="{{REPO_SLUG}}"
GOV_REPO="{{GOVERNING_REPO}}"

labels=(
  "ssos"
  "governance"
  "automation"
  "artifact"
  "contract"
  "project-sync"
  "upstream-change"
)

echo "Seeding SSOS governance labels into ${REPO_SLUG}"
for label in "${labels[@]}"; do
  gh label create "$label" --repo "${REPO_SLUG}" --force --description "SSOS governance label (${GOV_REPO})"
done

echo "Labels aligned with ${GOV_REPO}"
