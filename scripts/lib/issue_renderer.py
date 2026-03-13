from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .system_model import ensure_valid_system, next_stage_id, stage_map


def _format_list(items: List[str]) -> str:
    return "\n".join([f"- {item}" for item in items]) if items else "- (none)"


def render_stage_issue(
    system: Dict, stage_id: Optional[str] = None, system_file: Optional[Path] = None
) -> Tuple[str, str]:
    ensure_valid_system(system)
    target_stage_id = stage_id or next_stage_id(system) or system["current_stage"]
    stages = stage_map(system)
    stage = stages.get(target_stage_id)
    if not stage:
        raise ValueError(f"Stage '{target_stage_id}' not found in system.")

    title = f"[{system['name']}] {stage.get('name', target_stage_id).title()} stage"

    required_files = stage.get("required_files") or []
    if system_file:
        required_files = [str(system_file)] + required_files

    body_lines = [
        f"## Goal",
        stage.get("description", ""),
        "",
        "## Required Files",
        _format_list(required_files),
        "",
        "## Non-Goals",
        _format_list(stage.get("non_goals", [])),
        "",
        "## Checks",
        _format_list(stage.get("checks", [])),
        "",
        "## Definition of Done",
        _format_list(stage.get("definition_of_done", [])),
        "",
        "## Context",
        f"- Objective: {system.get('objective','')}",
        f"- Current Stage: {system.get('current_stage')}",
        f"- System Status: {system.get('status')}",
        f"- Inputs: {', '.join([i['name'] if isinstance(i, dict) else str(i) for i in system.get('inputs', [])]) or 'n/a'}",
        f"- Outputs: {', '.join([o['name'] if isinstance(o, dict) else str(o) for o in system.get('outputs', [])]) or 'n/a'}",
        f"- Dependencies: {', '.join(system.get('dependencies', [])) or 'n/a'}",
        "",
        "## Open Questions",
        _format_list(system.get("open_questions", [])),
    ]

    next_hint = stage.get("next_hint")
    if next_hint:
        body_lines.extend(["", "## Next Stage Hint", next_hint])

    return title, "\n".join(body_lines).strip() + "\n"


def render_completion_issue(system: Dict) -> Tuple[str, str]:
    ensure_valid_system(system)
    title = f"[{system['name']}] Release and completion"
    body = [
        "## Summary",
        f"- Objective: {system.get('objective','')}",
        "- All stages completed and system marked complete.",
        "",
        "## Final Checks",
        "- Verify release artifacts exist.",
        "- Close remaining open questions or convert to follow-ups.",
    ]
    return title, "\n".join(body).strip() + "\n"

