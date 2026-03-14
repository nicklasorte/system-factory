from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

import yaml

from .system_model import slugify

DEFAULT_REGISTRY_PATH = Path("templates/repo-roles.yaml")
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


def render_placeholders(content: str, replacements: Dict[str, str]) -> str:
    rendered = content
    for key, value in replacements.items():
        rendered = rendered.replace(key, value)
    return rendered


def _target_root(output: Path, slug: str) -> Path:
    if output.suffix:
        return output
    return output / slug


def scaffold_repo(
    name: str,
    role: str,
    output: Path,
    registry_path: Path = DEFAULT_REGISTRY_PATH,
    contract_mode: Optional[str] = None,
    primary_artifact_types: Optional[List[str]] = None,
    standards_version: Optional[str] = None,
) -> List[Path]:
    roles = load_repo_roles(registry_path)
    if role not in roles:
        known = ", ".join(sorted(roles.keys()))
        raise RepoScaffoldError(f"Unknown role '{role}'. Known roles: {known}")

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
    }

    created: List[Path] = []
    for src in template_root.rglob("*"):
        if src.is_dir():
            continue
        rel = src.relative_to(template_root)
        dest = dest_root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        rendered = render_placeholders(src.read_text(), replacements)
        dest.write_text(rendered)
        created.append(dest)
    return created
