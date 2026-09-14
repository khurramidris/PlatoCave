#!/usr/bin/env python3
"""Acquire and inspect the exact engine sources without installing/running them.

The inventory is static discovery, not a runtime API specification or proof of
feature correctness. It deliberately imports no engine code.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import subprocess
import sys
import tomllib
from pathlib import Path
from typing import Any

PROJECT = Path(__file__).resolve().parents[1]
HTTP_METHODS = {"get", "post", "put", "patch", "delete", "head", "options", "websocket"}


def git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    ).stdout.strip()


def read_lock() -> dict[str, Any]:
    lock = json.loads((PROJECT / "engines.lock.json").read_text())
    if lock.get("schema_version") != 1:
        raise ValueError("Unsupported engine lock schema")
    for item in lock["engines"]:
        if not re.fullmatch(r"[0-9a-f]{40}", item["commit"]):
            raise ValueError("Engine commit must be a full Git SHA")
        if Path(item["directory"]).name != item["directory"]:
            raise ValueError("Engine directory must be a single path component")
    return lock


def verify(root: Path, item: dict[str, Any]) -> None:
    if not (root / ".git").exists():
        raise ValueError(f"Missing checkout: {root}; run sync first")
    actual = git(root, "rev-parse", "HEAD")
    if actual != item["commit"]:
        raise ValueError(f"{item['id']}: expected {item['commit']}, found {actual}")
    if git(root, "status", "--porcelain", "--untracked-files=all"):
        raise ValueError(f"{item['id']}: checkout has changes; use a clean inspection checkout")


def sync(root: Path, item: dict[str, Any]) -> None:
    if root.exists():
        if not (root / ".git").exists():
            raise ValueError(f"Refusing to replace existing non-Git directory: {root}")
        if git(root, "status", "--porcelain", "--untracked-files=all"):
            raise ValueError(f"Refusing to change a dirty checkout: {root}")
    else:
        root.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["git", "clone", "--depth", "1", "--no-checkout", item["repository"], str(root)],
            check=True,
        )
    # Fetch the exact commit from the locked source, never an implicitly moving branch.
    try:
        git(root, "cat-file", "-e", item["commit"] + "^{commit}")
    except subprocess.CalledProcessError:
        git(root, "fetch", "--depth", "1", item["repository"], item["commit"])
    git(root, "checkout", "--detach", item["commit"])
    verify(root, item)


def literal(node: ast.AST) -> Any:
    try:
        return ast.literal_eval(node)
    except (ValueError, TypeError):
        return None


def parse(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def routes(path: Path, source_root: Path, mount_prefix: str = "") -> list[dict[str, Any]]:
    tree = parse(path)
    prefixes: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            if isinstance(node.value.func, ast.Name) and node.value.func.id == "APIRouter":
                prefix = next((literal(k.value) for k in node.value.keywords if k.arg == "prefix"), "")
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        prefixes[target.id] = prefix or ""
    found = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for dec in node.decorator_list:
            if not isinstance(dec, ast.Call) or not isinstance(dec.func, ast.Attribute):
                continue
            if dec.func.attr not in HTTP_METHODS or not dec.args:
                continue
            route = literal(dec.args[0])
            if not isinstance(route, str):
                raise ValueError(f"Nonliteral route requires manual inspection: {path}:{node.lineno}")
            owner = dec.func.value.id if isinstance(dec.func.value, ast.Name) else ""
            found.append({
                "method": dec.func.attr.upper(),
                "path": mount_prefix + prefixes.get(owner, "") + route,
                "handler": node.name,
                "source": str(path.relative_to(source_root)),
                "line": node.lineno,
            })
    return sorted(found, key=lambda x: (x["path"], x["method"]))


def paths(root: Path, directory: str, pattern: str) -> list[str]:
    return sorted(str(p.relative_to(root)) for p in (root / directory).glob(pattern))


def cli_declarations(root: Path, files: list[Path]) -> list[dict[str, Any]]:
    found = []
    for file in sorted(files):
        for node in ast.walk(parse(file)):
            if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
                continue
            method = node.func.attr
            if method not in {"command", "add_typer", "add_parser", "add_argument"}:
                continue
            args = [literal(a) for a in node.args]
            kwargs = {k.arg: literal(k.value) for k in node.keywords if k.arg}
            found.append({
                "source": str(file.relative_to(root)), "line": node.lineno,
                "declaration": method, "args": args, "keywords": kwargs,
            })
    return found


def inventory(root: Path, item: dict[str, Any]) -> dict[str, Any]:
    verify(root, item)
    data: dict[str, Any] = {
        "id": item["id"], "repository": item["repository"], "commit": item["commit"],
        "verification": "clean pinned source; no engine execution performed",
    }
    if item["id"] == "agentsociety2":
        base = root / "packages/agentsociety2/agentsociety2"
        app = base / "backend/app.py"
        mount_prefixes = {}
        for node in ast.walk(parse(app)):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if node.func.attr == "include_router" and node.args:
                    arg = node.args[0]
                    if isinstance(arg, ast.Attribute) and isinstance(arg.value, ast.Name):
                        mount_prefixes[arg.value.id] = next(
                            (literal(k.value) for k in node.keywords if k.arg == "prefix"), ""
                        )
        data["api_routes"] = routes(app, root)
        for name, prefix in sorted(mount_prefixes.items()):
            data["api_routes"].extend(routes(base / f"backend/routers/{name}.py", root, prefix))
        data["environment_classes"] = []
        for file in sorted((base / "contrib/env").rglob("*.py")):
            for node in parse(file).body:
                if isinstance(node, ast.ClassDef) and any(
                    isinstance(b, ast.Name) and b.id == "EnvBase" for b in node.bases
                ):
                    data["environment_classes"].append({"name": node.name, "source": str(file.relative_to(root))})
        data["router_sources"] = paths(root, str((base / "env").relative_to(root)), "router_*.py")
        data["extension_commands"] = json.loads((root / "extension/package.json").read_text())["contributes"]["commands"]
        data["extension_skills"] = paths(root, "extension/skills", "**/SKILL.md")
        data["cli_declarations"] = cli_declarations(root, [base / "society/cli.py", base / "society/workspace.py"])
        data["console_scripts"] = tomllib.loads((root / "packages/agentsociety2/pyproject.toml").read_text())["project"]["scripts"]
    elif item["id"] == "matraix":
        data["api_routes"] = routes(root / "application/playground/backend/api/app.py", root)
        schema = json.loads((root / "persona/schema/dimensions.json").read_text())
        data["persona_dimension_count"] = len(schema["dimensions"])
        data["tasks"] = paths(root, "application/tasks", "*/task.toml")
        data["persona_scripts"] = paths(root, "persona", "**/scripts/**/*.py")
        data["persona_agent_sources"] = paths(root, "environment/agents/matraix/agents/persona", "*.py")
        data["runtime_environment_sources"] = paths(root, "environment/runtime/harbor/environments", "**/*.py")
        data["cli_declarations"] = cli_declarations(root, [root / "src/matraix/cli.py", *list((root / "environment/runtime/harbor/cli").rglob("*.py"))])
        data["console_scripts"] = tomllib.loads((root / "pyproject.toml").read_text())["project"]["scripts"]
    else:
        raise ValueError(f"No inventory implementation for {item['id']}")
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sources-root", type=Path, default=PROJECT / "engines")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("sync", help="Clone/checkout pinned sources; refuse dirty checkouts")
    commands.add_parser("verify", help="Verify exact clean revisions without network access")
    inv = commands.add_parser("inventory", help="Statically inspect source entry points")
    inv.add_argument("--output", type=Path, default=PROJECT / "docs/source_inventory.json")
    args = parser.parse_args()
    lock = read_lock()
    report = {"schema_version": 1, "baseline_date": lock["inspected_on"], "method": "static source inventory, not runtime validation", "engines": []}
    for item in lock["engines"]:
        root = args.sources_root.resolve() / item["directory"]
        if args.command == "sync":
            sync(root, item)
        elif args.command == "verify":
            verify(root, item)
        else:
            report["engines"].append(inventory(root, item))
        print(f"{item['id']}: {args.command} complete at {item['commit']}")
    if args.command == "inventory":
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Inventory written to {args.output}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        print(f"Engine source operation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
