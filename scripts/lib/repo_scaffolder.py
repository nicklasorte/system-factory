from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

import yaml

from .system_model import slugify

DEFAULT_REGISTRY_PATH = Path("templates/repo-roles.yaml")
DEFAULT_PRESET_REGISTRY_PATH = Path("templates/repo-presets.yaml")
DEFAULT_GOVERNANCE_BOOTSTRAP_ROOT = Path("templates/governance_bootstrap")
DEFAULT_TEMPLATE_ROOT = Path("templates/repo/base")


class RepoScaffoldError(Exception):
    """Raised when repo scaffolding cannot proceed."""


@dataclass
class RoleProfile:
    name: str
    template_path: Path
    description: str
    contract_mode: str
    primary_artifact_types: List[str]
    consumed_artifact_types: List[str]
    produced_artifact_types: List[str]
    supported_contract_versions: List[str]
    standards_dependency: str
    standards_source_version: str
    standards_enforcement: str


@dataclass
class PresetProfile:
    name: str
    role: str
    description: str
    system_layer: str
    governing_repo: str
    include_governance_bootstrap: bool
    include_project_automation: bool
    include_issue_templates: bool
    include_label_script: bool
    github_project_number: Optional[str]
    recommended_labels: List[str]
    recommended_docs: List[str]
    automation_hooks: List[str]
    metadata_notes: List[str]


def load_repo_roles(registry_path: Path = DEFAULT_REGISTRY_PATH) -> Dict[str, RoleProfile]:
    if not registry_path.exists():
        raise RepoScaffoldError(f"Repo role registry not found at {registry_path}")
    registry = yaml.safe_load(registry_path.read_text()) or {}
    roles: Dict[str, RoleProfile] = {}
    for role_name, cfg in (registry.get("roles") or {}).items():
        template_path = Path(cfg.get("template_path", DEFAULT_TEMPLATE_ROOT))
        roles[role_name] = RoleProfile(
            name=role_name,
            template_path=template_path,
            description=cfg.get("description", ""),
            contract_mode=cfg.get("contract_mode", "consume"),
            primary_artifact_types=cfg.get("primary_artifact_types", []),
            consumed_artifact_types=cfg.get("consumed_artifact_types", []),
            produced_artifact_types=cfg.get("produced_artifact_types", []),
            supported_contract_versions=cfg.get("supported_contract_versions", []),
            standards_dependency=cfg.get("standards_dependency", "spectrum-systems"),
            standards_source_version=cfg.get("standards_source_version", "main"),
            standards_enforcement=cfg.get("standards_enforcement", "required"),
        )
    if not roles:
        raise RepoScaffoldError("No roles defined in registry.")
    return roles


def load_repo_presets(registry_path: Path = DEFAULT_PRESET_REGISTRY_PATH) -> Dict[str, PresetProfile]:
    if not registry_path.exists():
        raise RepoScaffoldError(f"Repo preset registry not found at {registry_path}")
    registry = yaml.safe_load(registry_path.read_text()) or {}
    presets: Dict[str, PresetProfile] = {}
    for preset_name, cfg in (registry.get("presets") or {}).items():
        presets[preset_name] = PresetProfile(
            name=preset_name,
            role=cfg.get("role", ""),
            description=cfg.get("description", ""),
            system_layer=cfg.get("system_layer", "Factory"),
            governing_repo=cfg.get("governing_repo", "nicklasorte/spectrum-systems"),
            include_governance_bootstrap=cfg.get("include_governance_bootstrap", True),
            include_project_automation=cfg.get("include_project_automation", True),
            include_issue_templates=cfg.get("include_issue_templates", True),
            include_label_script=cfg.get("include_label_script", True),
            github_project_number=str(cfg.get("github_project_number", "") or ""),
            recommended_labels=cfg.get("recommended_labels", []),
            recommended_docs=cfg.get("recommended_docs", []),
            automation_hooks=cfg.get("automation_hooks", []),
            metadata_notes=cfg.get("metadata_notes", []),
        )
    if not presets:
        raise RepoScaffoldError("No presets defined in registry.")
    return presets


def render_placeholders(content: str, replacements: Dict[str, str]) -> str:
    rendered = content
    for key, value in replacements.items():
        rendered = rendered.replace(key, str(value))
    return rendered


def _target_root(output: Path, slug: str) -> Path:
    if output.suffix:
        return output
    return output / slug


def _default_system_layer(role: str) -> str:
    mapping = {
        "engine_repo": "Engine",
        "orchestration_repo": "Orchestrator",
        "library_repo": "Knowledge",
        "analysis_repo": "Advisor",
        "standards_repo": "Governance",
    }
    return mapping.get(role, "Factory")


def _governance_include_filter(
    rel: Path,
    include_governance_bootstrap: bool,
    include_project_automation: bool,
    include_issue_templates: bool,
    include_label_script: bool,
) -> bool:
    if not include_governance_bootstrap:
        return False
    parts = rel.parts
    if parts[:2] == (".github", "ISSUE_TEMPLATE"):
        return include_issue_templates
    if parts[:2] == (".github", "workflows"):
        return include_project_automation
    if parts[:1] == ("scripts",):
        return include_label_script
    return True


def _render_template_tree(
    src_root: Path,
    dest_root: Path,
    replacements: Dict[str, str],
    created: List[Path],
    include_filter=None,
) -> None:
    for src in src_root.rglob("*"):
        if src.is_dir():
            continue
        rel = src.relative_to(src_root)
        if include_filter and not include_filter(rel):
            continue
        dest = dest_root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        rendered = render_placeholders(src.read_text(), replacements)
        dest.write_text(rendered)
        created.append(dest)


def scaffold_repo(
    name: str,
    role: str,
    output: Path,
    registry_path: Path = DEFAULT_REGISTRY_PATH,
    preset_registry_path: Path = DEFAULT_PRESET_REGISTRY_PATH,
    contract_mode: Optional[str] = None,
    primary_artifact_types: Optional[List[str]] = None,
    standards_version: Optional[str] = None,
    include_governance_bootstrap: Optional[bool] = None,
    include_project_automation: Optional[bool] = None,
    include_issue_templates: Optional[bool] = None,
    include_label_script: Optional[bool] = None,
    governing_repo: Optional[str] = None,
    github_project_number: Optional[str] = None,
    system_layer: Optional[str] = None,
    preset: Optional[str] = None,
) -> List[Path]:
    roles = load_repo_roles(registry_path)
    if role not in roles:
        known = ", ".join(sorted(roles.keys()))
        raise RepoScaffoldError(f"Unknown role '{role}'. Known roles: {known}")

    preset_profile: Optional[PresetProfile] = None
    if preset:
        presets = load_repo_presets(preset_registry_path)
        if preset not in presets:
            known_presets = ", ".join(sorted(presets.keys()))
            raise RepoScaffoldError(f"Unknown preset '{preset}'. Known presets: {known_presets}")
        preset_profile = presets[preset]
        if preset_profile.role and preset_profile.role != role:
            raise RepoScaffoldError(
                f"Preset '{preset}' expects role '{preset_profile.role}', but '{role}' was provided."
            )

    profile = roles[role]
    template_root = profile.template_path or DEFAULT_TEMPLATE_ROOT
    if not template_root.exists():
        raise RepoScaffoldError(f"Template path not found for role '{role}': {template_root}")

    slug = slugify(name)
    dest_root = _target_root(output, slug)
    dest_root.mkdir(parents=True, exist_ok=True)

    primary_types = primary_artifact_types or profile.primary_artifact_types
    consumed_types = profile.consumed_artifact_types or primary_types
    produced_types = profile.produced_artifact_types or primary_types
    contract_mode_value = contract_mode or profile.contract_mode
    standards_version_value = standards_version or profile.standards_source_version
    governance_repo_value = governing_repo or (preset_profile.governing_repo if preset_profile else "nicklasorte/spectrum-systems")
    system_layer_value = system_layer or (preset_profile.system_layer if preset_profile else _default_system_layer(role))
    github_project_number_value = (
        str(github_project_number)
        if github_project_number is not None
        else (preset_profile.github_project_number if preset_profile else "")
    ) or "<set-project-number>"
    include_governance_value = (
        include_governance_bootstrap
        if include_governance_bootstrap is not None
        else (preset_profile.include_governance_bootstrap if preset_profile else True)
    )
    include_project_value = (
        include_project_automation
        if include_project_automation is not None
        else (preset_profile.include_project_automation if preset_profile else include_governance_value)
    )
    include_issue_templates_value = (
        include_issue_templates
        if include_issue_templates is not None
        else (preset_profile.include_issue_templates if preset_profile else include_governance_value)
    )
    include_label_script_value = (
        include_label_script
        if include_label_script is not None
        else (preset_profile.include_label_script if preset_profile else include_governance_value)
    )

    consumed_block = "\n".join([f"  - {item}" for item in consumed_types]) if consumed_types else "  - define_inputs"
    produced_block = "\n".join([f"  - {item}" for item in produced_types]) if produced_types else "  - define_outputs"
    primary_block = "\n".join([f"  - {item}" for item in primary_types]) if primary_types else "  - define_primary_artifacts"
    supported_block = (
        "\n".join([f"  - {item}" for item in profile.supported_contract_versions])
        if profile.supported_contract_versions
        else "  - v1"
    )

    replacements = {
        "{{REPO_NAME}}": name,
        "{{REPO_SLUG}}": slug,
        "{{REPO_ROLE}}": role,
        "{{CONTRACT_MODE}}": contract_mode_value,
        "{{PRIMARY_ARTIFACT_TYPES}}": ", ".join(primary_types) if primary_types else "",
        "{{CONSUMED_ARTIFACT_TYPES}}": ", ".join(consumed_types) if consumed_types else "",
        "{{PRODUCED_ARTIFACT_TYPES}}": ", ".join(produced_types) if produced_types else "",
        "{{SUPPORTED_CONTRACT_VERSIONS}}": ", ".join(profile.supported_contract_versions),
        "{{STANDARDS_REPO}}": profile.standards_dependency,
        "{{STANDARDS_VERSION}}": standards_version_value,
        "{{STANDARDS_ENFORCEMENT}}": profile.standards_enforcement,
        "{{PRIMARY_ARTIFACT_TYPES_BLOCK}}": primary_block,
        "{{CONSUMED_ARTIFACT_TYPES_BLOCK}}": consumed_block,
        "{{PRODUCED_ARTIFACT_TYPES_BLOCK}}": produced_block,
        "{{SUPPORTED_CONTRACT_VERSIONS_BLOCK}}": supported_block,
        "{{GOVERNING_REPO}}": governance_repo_value,
        "{{SYSTEM_LAYER}}": system_layer_value,
        "{{GOVERNANCE_BOOTSTRAP_STATUS}}": (
            "enabled (SSOS control-plane assets applied)"
            if include_governance_value
            else "disabled (manually link to governing repo before release)"
        ),
        "{{GITHUB_PROJECT_NUMBER}}": github_project_number_value,
        "{{SSOS_DECLARATION}}": (
            f"This repo is part of the SSOS / czar org and governed by {governance_repo_value}."
        ),
        "{{CANONICAL_CONTRACT_RULE}}": (
            f"{governance_repo_value} owns canonical schemas and contracts. "
            "Propose changes upstream before adopting locally."
        ),
    }

    created: List[Path] = []
    _render_template_tree(template_root, dest_root, replacements, created)

    governance_filter = lambda rel: _governance_include_filter(  # noqa: E731
        rel,
        include_governance_value,
        include_project_value,
        include_issue_templates_value,
        include_label_script_value,
    )
    if DEFAULT_GOVERNANCE_BOOTSTRAP_ROOT.exists():
        _render_template_tree(
            DEFAULT_GOVERNANCE_BOOTSTRAP_ROOT,
            dest_root,
            replacements,
            created,
            include_filter=governance_filter,
        )
    return created
