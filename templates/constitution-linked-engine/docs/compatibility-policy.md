# Compatibility Policy

- Pin the constitution reference in `config/constitution.yaml` (use a tagged release for production, `main` for active development).
- Treat changes in the constitution as upstream dependencies: read the changelog, identify breaking changes, and only bump the reference after the engine passes regression tests.
- Temporary divergences require an explicit exception, an owner, and a removal date; keep the diff from `spectrum-systems` as small as possible.
- Update `sync.last_synced_ref` and note any migrations whenever the reference changes.
- Block releases if the pinned reference is stale or if required artifacts (rules profile, prompt registry, provenance standard, error taxonomy, contracts) are missing or outdated.
