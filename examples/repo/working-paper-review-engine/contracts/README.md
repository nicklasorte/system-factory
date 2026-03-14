# Contract Integration

Canonical contract definitions live in `spectrum-systems`. This folder is intentionally light and should only contain adapters or fixtures that reference the upstream source.

Guidelines:
- Do not copy canonical schemas here. Fetch them from `spectrum-systems` at `main`.
- If a temporary fixture is unavoidable, mark it clearly with the upstream reference and removal criteria.
- Keep validation logic in `validation/contract_validation.py` so it can be shared across pipelines.
