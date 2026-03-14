# Playbook: Review Hardening

Goal: improve reliability, safety, and performance.

## Steps
- Confirm `current_stage` is `review-hardening` and review test coverage.
- Identify failure modes, timeouts, and rate limits.
- Add guards, retries, and telemetry where appropriate.
- Update documentation with operational expectations.
- Validate and run tests.

## Definition of done
- Known risks mitigated or explicitly accepted.
- Monitoring/logging in place for critical paths.
- Tests cover key failure scenarios.
- Stage status set to `done` with notes for operators.
