import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml

STANDARD_STAGE_ORDER: List[str] = [
    "intake",
    "scaffold",
    "contracts",
    "core-engine",
    "review-hardening",
    "release",
]

VALID_STAGE_STATUS = {"planned", "in_progress", "blocked", "done"}
VALID_SYSTEM_STATUS = {"planned", "in_progress", "blocked", "complete"}


class ValidationError(Exception):
    """Raised when a system definition does not meet the expected shape."""


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return slug or "system"


def load_system_file(path: Path) -> Dict:
    data = yaml.safe_load(path.read_text())
    if not isinstance(data, dict):
        raise ValidationError(f"{path} did not contain a YAML object")
    return data


def dump_system_file(system: Dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(system, sort_keys=False))


def _validate_stage(stage: Dict, index: int) -> List[str]:
    errors: List[str] = []
    required_fields = ["id", "name", "description", "status", "definition_of_done"]
    for field in required_fields:
        if field not in stage or stage[field] in (None, "", []):
            errors.append(f"stage[{index}].{field} is required")
    status = stage.get("status")
    if status and status not in VALID_STAGE_STATUS:
        errors.append(
            f"stage[{index}].status must be one of {sorted(VALID_STAGE_STATUS)}"
        )
    dod = stage.get("definition_of_done")
    if dod is not None and not isinstance(dod, list):
        errors.append(f"stage[{index}].definition_of_done must be a list")
    required_files = stage.get("required_files")
    if required_files is not None and not isinstance(required_files, list):
        errors.append(f"stage[{index}].required_files must be a list if provided")
    checks = stage.get("checks")
    if checks is not None and not isinstance(checks, list):
        errors.append(f"stage[{index}].checks must be a list if provided")
    non_goals = stage.get("non_goals")
    if non_goals is not None and not isinstance(non_goals, list):
        errors.append(f"stage[{index}].non_goals must be a list if provided")
    outputs = stage.get("outputs")
    if outputs is not None and not isinstance(outputs, list):
        errors.append(f"stage[{index}].outputs must be a list if provided")
    return errors


def _validate_stage_sequence(stage_ids: List[str]) -> List[str]:
    errors: List[str] = []
    known_ids = [sid for sid in stage_ids if sid]
    duplicates = sorted({sid for sid in known_ids if known_ids.count(sid) > 1})
    if duplicates:
        errors.append(f"duplicate stage ids: {', '.join(duplicates)}")
    missing = [sid for sid in STANDARD_STAGE_ORDER if sid not in known_ids]
    if missing:
        errors.append(f"missing stage ids: {', '.join(missing)}")
    extras = [sid for sid in known_ids if sid not in STANDARD_STAGE_ORDER]
    if extras:
        errors.append(f"unknown stage ids: {', '.join(extras)}")
    if not duplicates and not missing and not extras and known_ids != STANDARD_STAGE_ORDER:
        errors.append(
            "stages must follow the standard order "
            f"{' -> '.join(STANDARD_STAGE_ORDER)}"
        )
    return errors


def validate_system(system: Dict) -> List[str]:
    errors: List[str] = []
    required_fields = [
        "name",
        "type",
        "objective",
        "current_stage",
        "status",
        "stages",
        "inputs",
        "outputs",
        "dependencies",
        "acceptance_criteria",
        "open_questions",
    ]
    for field in required_fields:
        if field not in system or system[field] in (None, ""):
            errors.append(f"{field} is required")
    status = system.get("status")
    if status and status not in VALID_SYSTEM_STATUS:
        errors.append(f"status must be one of {sorted(VALID_SYSTEM_STATUS)}")
    stages = system.get("stages")
    if not isinstance(stages, list) or not stages:
        errors.append("stages must be a non-empty list")
    else:
        for index, stage in enumerate(stages):
            if not isinstance(stage, dict):
                errors.append(f"stage[{index}] must be an object")
                continue
            errors.extend(_validate_stage(stage, index))
        stage_ids = [stage.get("id") for stage in stages if isinstance(stage, dict)]
        errors.extend(_validate_stage_sequence(stage_ids))
        current_stage = system.get("current_stage")
        if current_stage and current_stage not in stage_ids:
            errors.append(
                f"current_stage '{current_stage}' is not present in stages list"
            )
    for list_field in ["inputs", "outputs", "dependencies", "acceptance_criteria", "open_questions"]:
        if list_field in system and not isinstance(system.get(list_field), list):
            errors.append(f"{list_field} must be a list")
    return errors


def ensure_valid_system(system: Dict) -> None:
    errors = validate_system(system)
    if errors:
        raise ValidationError("\n".join(errors))


def stage_map(system: Dict) -> Dict[str, Dict]:
    ensure_valid_system(system)
    return {stage["id"]: stage for stage in system["stages"]}


def is_stage_done(stage: Dict) -> bool:
    return stage.get("status") == "done"


def next_stage_id(system: Dict) -> Optional[str]:
    ensure_valid_system(system)
    ids = [stage["id"] for stage in system["stages"]]
    current = system["current_stage"]
    if current not in ids:
        raise ValidationError(f"current_stage '{current}' is not in stage list")
    index = ids.index(current)
    if not is_stage_done(system["stages"][index]):
        return None
    if index + 1 < len(ids):
        return ids[index + 1]
    return None


@dataclass
class AdvanceResult:
    changed: bool
    next_stage: Optional[str]
    completed: bool
    message: str


def advance_system(system: Dict) -> AdvanceResult:
    ensure_valid_system(system)
    current_id = system["current_stage"]
    stages = system["stages"]
    current_stage = next((s for s in stages if s["id"] == current_id), None)
    if not current_stage:
        raise ValidationError(f"Current stage '{current_id}' not found")
    if not is_stage_done(current_stage):
        return AdvanceResult(
            changed=False,
            next_stage=None,
            completed=False,
            message="Current stage is not marked done; no advancement performed.",
        )
    ids = [stage["id"] for stage in stages]
    idx = ids.index(current_id)
    if idx == len(stages) - 1:
        system["status"] = "complete"
        return AdvanceResult(
            changed=True,
            next_stage=None,
            completed=True,
            message="Final stage completed. System marked complete.",
        )
    next_id = ids[idx + 1]
    system["current_stage"] = next_id
    for stage in stages:
        if stage["id"] == next_id and stage.get("status") == "planned":
            stage["status"] = "in_progress"
    system["status"] = "in_progress"
    return AdvanceResult(
        changed=True,
        next_stage=next_id,
        completed=False,
        message=f"Advanced to {next_id}.",
    )


def list_system_files(paths: Optional[List[str]] = None) -> List[Path]:
    search_roots = [Path(p) for p in (paths or ["systems", "examples"]) if Path(p).exists()]
    files: List[Path] = []
    for root in search_roots:
        files.extend(root.rglob("*.system.yaml"))
    return sorted(files)


def system_summary(system: Dict) -> str:
    ensure_valid_system(system)
    ids = [stage["id"] for stage in system["stages"]]
    status_line = f"{system['name']} ({system['type']}) - {system['status']}"
    stage_line = f"current_stage={system['current_stage']} | stages={ ' -> '.join(ids)}"
    return f"{status_line}\n{stage_line}"


def serialize_issue_payload(payload: List[Dict], path: Path) -> None:
    path.write_text(json.dumps(payload, indent=2))
