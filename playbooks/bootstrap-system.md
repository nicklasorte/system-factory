# Playbook: Bootstrap System

Goal: capture the system idea and land the initial scaffolding.

## Steps
- Read the target `*.system.yaml` and confirm `current_stage` is `intake` or `scaffold`.
- Validate the file: `python scripts/system_factory.py validate --file <path>`.
- Ensure the template fields are filled: name, type, objective, inputs, outputs, dependencies, acceptance_criteria, open_questions.
- Add docs: `README.md`, `SYSTEMS.md`, `AGENT_ROUTER.md`, and stage playbooks.
- Wire CI workflows and issue templates.
- Set the intake stage `status: done` once the above are merged.

## Definition of done
- System file validates against `schema/system.schema.yaml`.
- Core docs and playbooks exist and are referenced from the README.
- Validation workflow passes in CI.
- Stage issue closed with a handoff note and next-stage hint.
