# Versioning and Drift Policy

- Pin `constitution.source.reference` to an immutable ref (tag or release) for production; `main` is acceptable only for active development with heightened verification.
- Treat constitution updates as upstream dependencies: read the `spectrum-systems` changelog, assess breaking changes, and bump the reference only after the engine passes its regression and governance checks.
- Update `sync.last_synced_ref` whenever the pinned reference changes and record any migrations or notable diffs in the PR notes.
- Do not fork or edit governance artifacts locally. If a temporary exception is unavoidable, document the owner, deadline, and cleanup steps, and keep the diff minimal.
- Block releases when the pinned reference is stale or when required artifacts (rules profile, prompt registry, provenance standard, error taxonomy, contracts) are missing or mismatched.
- When drift is detected, stop rollouts, realign to the pinned constitution, and prefer backporting fixes to `spectrum-systems` rather than maintaining long-lived local patches.
