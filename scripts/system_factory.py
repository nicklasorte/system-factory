#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
from typing import Dict, List

from lib.issue_renderer import render_completion_issue, render_stage_issue
from lib.system_model import (
    AdvanceResult,
    ValidationError,
    advance_system,
    dump_system_file,
    ensure_valid_system,
    list_system_files,
    load_system_file,
    next_stage_id,
    serialize_issue_payload,
    slugify,
    validate_system,
)


def _read_template(template_path: Path) -> str:
    return template_path.read_text()


def _render_template(content: str, name: str, type_: str, objective: str) -> str:
    return (
        content.replace("{{SYSTEM_NAME}}", name)
        .replace("{{SYSTEM_TYPE}}", type_)
        .replace("{{SYSTEM_OBJECTIVE}}", objective)
    )


def cmd_create(args: argparse.Namespace) -> int:
    template_path = Path(args.template)
    if not template_path.exists():
        print(f"Template not found: {template_path}", file=sys.stderr)
        return 1
    output_root = Path(args.output)
    system_slug = args.slug or slugify(args.name)
    if output_root.suffix:
        output_path = output_root
    else:
        output_root.mkdir(parents=True, exist_ok=True)
        output_path = output_root / f"{system_slug}.system.yaml"
    rendered = _render_template(
        _read_template(template_path), args.name, args.type, args.objective
    )
    output_path.write_text(rendered)
    if args.print_path_only:
        print(output_path)
    else:
        print(f"Created system file at {output_path}")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    files: List[Path] = []
    if args.all:
        files = list_system_files()
    if args.file:
        files.extend([Path(f) for f in args.file])
    if not files:
        print("No system files provided. Use --file or --all.", file=sys.stderr)
        return 1
    errors_found = False
    for path in files:
        try:
            system = load_system_file(path)
            errs = validate_system(system)
            if errs:
                errors_found = True
                print(f"[INVALID] {path}")
                for err in errs:
                    print(f"  - {err}")
            else:
                print(f"[OK] {path}")
        except ValidationError as exc:
            errors_found = True
            print(f"[INVALID] {path}: {exc}")
        except FileNotFoundError:
            errors_found = True
            print(f"[MISSING] {path}")
    return 1 if errors_found else 0


def cmd_next_stage(args: argparse.Namespace) -> int:
    path = Path(args.file)
    system = load_system_file(path)
    try:
        ensure_valid_system(system)
    except ValidationError as exc:
        print(exc, file=sys.stderr)
        return 1
    nxt = next_stage_id(system)
    if nxt:
        print(nxt)
        return 0
    print("No next stage (either final or current stage not marked done).")
    return 0


def cmd_render_issue(args: argparse.Namespace) -> int:
    path = Path(args.file)
    system = load_system_file(path)
    stage = args.stage
    try:
        ensure_valid_system(system)
    except ValidationError as exc:
        print(exc, file=sys.stderr)
        return 1
    title, body = render_stage_issue(system, stage_id=stage, system_file=path)
    if args.output:
        out_path = Path(args.output)
        out_path.write_text(body)
        print(f"Wrote issue body to {out_path}")
    else:
        print(f"# {title}\n\n{body}")
    return 0


def _advance_single(path: Path) -> Dict:
    system = load_system_file(path)
    result = advance_system(system)
    if result.changed:
        dump_system_file(system, path)
    payload = {"file": str(path), "changed": result.changed, "message": result.message}
    if result.next_stage:
        title, body = render_stage_issue(system, stage_id=result.next_stage, system_file=path)
        payload.update({"issue_title": title, "issue_body": body, "type": "stage"})
    elif result.completed:
        title, body = render_completion_issue(system)
        payload.update({"issue_title": title, "issue_body": body, "type": "completion"})
    return payload


def cmd_advance(args: argparse.Namespace) -> int:
    files = [Path(f) for f in args.files]
    if not files:
        print("No files supplied to advance.", file=sys.stderr)
        return 1
    payloads: List[Dict] = []
    for path in files:
        try:
            payload = _advance_single(path)
            payloads.append(payload)
            print(f"{path}: {payload.get('message')}")
        except ValidationError as exc:
            print(f"{path}: validation failed - {exc}", file=sys.stderr)
            return 1
        except FileNotFoundError:
            print(f"{path}: file not found", file=sys.stderr)
            return 1
    if args.issue_output:
        serialize_issue_payload(payloads, Path(args.issue_output))
        print(f"Wrote issue payload to {args.issue_output}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="System factory helpers.")
    sub = parser.add_subparsers(dest="command", required=True)

    create = sub.add_parser("create", help="Create a system file from the template.")
    create.add_argument("--name", required=True)
    create.add_argument("--type", required=True)
    create.add_argument("--objective", required=True)
    create.add_argument(
        "--template", default="templates/system-template.yaml", help="Path to template."
    )
    create.add_argument(
        "--output",
        default="systems",
        help="Output file or directory. Defaults to systems/{slug}.system.yaml",
    )
    create.add_argument("--slug", help="Optional explicit slug for the system file name.")
    create.add_argument(
        "--print-path-only",
        action="store_true",
        help="Print only the created file path (useful in automation).",
    )
    create.set_defaults(func=cmd_create)

    validate = sub.add_parser("validate", help="Validate system files.")
    validate.add_argument("--file", nargs="*", help="Specific system file(s) to validate.")
    validate.add_argument("--all", action="store_true", help="Validate all known system files.")
    validate.set_defaults(func=cmd_validate)

    nxt = sub.add_parser("next-stage", help="Compute the next stage for a system.")
    nxt.add_argument("--file", required=True, help="Path to a system file.")
    nxt.set_defaults(func=cmd_next_stage)

    render = sub.add_parser("render-issue", help="Render issue body for a stage.")
    render.add_argument("--file", required=True, help="System file path.")
    render.add_argument("--stage", help="Stage id. Defaults to next stage if available.")
    render.add_argument("--output", help="Optional path to write the body.")
    render.set_defaults(func=cmd_render_issue)

    advance = sub.add_parser("advance", help="Advance systems after merge.")
    advance.add_argument("--files", nargs="+", required=True, help="System files to advance.")
    advance.add_argument(
        "--issue-output",
        help="Path to write JSON payload describing issues to open after advancement.",
    )
    advance.set_defaults(func=cmd_advance)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())

