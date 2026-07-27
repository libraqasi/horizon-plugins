#!/usr/bin/env python3
"""Validate the local Codex marketplace catalog and plugin structure."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
MARKETPLACE_PATH = REPOSITORY_ROOT / ".agents" / "plugins" / "marketplace.json"


def load_object(path: Path, errors: list[str]) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"Missing file: {path.relative_to(REPOSITORY_ROOT)}")
        return None
    except json.JSONDecodeError as exc:
        errors.append(
            f"Invalid JSON in {path.relative_to(REPOSITORY_ROOT)}: "
            f"line {exc.lineno}, column {exc.colno}: {exc.msg}"
        )
        return None

    if not isinstance(value, dict):
        errors.append(f"Expected a JSON object: {path.relative_to(REPOSITORY_ROOT)}")
        return None
    return value


def require_string(
    value: dict[str, Any], key: str, label: str, errors: list[str]
) -> str | None:
    candidate = value.get(key)
    if not isinstance(candidate, str) or not candidate.strip():
        errors.append(f"{label} must define a non-empty string '{key}'")
        return None
    return candidate


def resolve_plugin_path(
    source: dict[str, Any], label: str, errors: list[str]
) -> Path | None:
    if source.get("source") != "local":
        errors.append(f"{label} source.source must be 'local'")
        return None

    relative_source = require_string(source, "path", f"{label} source", errors)
    if relative_source is None:
        return None

    candidate = (REPOSITORY_ROOT / relative_source).resolve()
    try:
        candidate.relative_to(REPOSITORY_ROOT)
    except ValueError:
        errors.append(f"{label} source path escapes the repository: {relative_source}")
        return None

    if not candidate.is_dir():
        errors.append(f"{label} source directory does not exist: {relative_source}")
        return None
    return candidate


def validate_declared_path(
    plugin_root: Path,
    declared_path: str,
    label: str,
    errors: list[str],
    *,
    directory: bool = False,
) -> Path | None:
    candidate = (plugin_root / declared_path).resolve()
    try:
        candidate.relative_to(plugin_root.resolve())
    except ValueError:
        errors.append(f"{label} escapes its plugin directory: {declared_path}")
        return None

    exists = candidate.is_dir() if directory else candidate.is_file()
    if not exists:
        kind = "directory" if directory else "file"
        errors.append(f"{label} {kind} does not exist: {declared_path}")
        return None
    return candidate


def validate_plugin(
    entry: dict[str, Any], index: int, names: set[str], errors: list[str]
) -> None:
    label = f"plugins[{index}]"
    catalog_name = require_string(entry, "name", label, errors)
    if catalog_name is not None:
        if catalog_name in names:
            errors.append(f"Duplicate plugin name in marketplace: {catalog_name}")
        names.add(catalog_name)

    source = entry.get("source")
    if not isinstance(source, dict):
        errors.append(f"{label} must define an object 'source'")
        return

    plugin_root = resolve_plugin_path(source, label, errors)
    if plugin_root is None:
        return

    manifest_path = plugin_root / ".codex-plugin" / "plugin.json"
    manifest = load_object(manifest_path, errors)
    if manifest is None:
        return

    manifest_name = require_string(manifest, "name", f"{label} manifest", errors)
    require_string(manifest, "version", f"{label} manifest", errors)
    require_string(manifest, "description", f"{label} manifest", errors)
    if catalog_name and manifest_name and catalog_name != manifest_name:
        errors.append(
            f"{label} name '{catalog_name}' does not match manifest name "
            f"'{manifest_name}'"
        )

    skills_path = manifest.get("skills")
    if not isinstance(skills_path, str) or not skills_path.strip():
        errors.append(f"{label} manifest must define a non-empty string 'skills'")
    else:
        skills_root = validate_declared_path(
            plugin_root,
            skills_path,
            f"{label} skills",
            errors,
            directory=True,
        )
        if skills_root is not None:
            skill_files = sorted(skills_root.glob("*/SKILL.md"))
            if not skill_files:
                errors.append(f"{label} has no skill directories containing SKILL.md")

    interface = manifest.get("interface")
    if not isinstance(interface, dict):
        errors.append(f"{label} manifest must define an object 'interface'")
        return

    for field in ("composerIcon", "logo"):
        declared_asset = interface.get(field)
        if not isinstance(declared_asset, str) or not declared_asset.strip():
            errors.append(f"{label} interface must define a non-empty '{field}'")
            continue
        validate_declared_path(
            plugin_root, declared_asset, f"{label} interface.{field}", errors
        )


def main() -> int:
    errors: list[str] = []
    marketplace = load_object(MARKETPLACE_PATH, errors)
    if marketplace is None:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    marketplace_name = require_string(
        marketplace, "name", "marketplace", errors
    )
    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        errors.append("marketplace must define a non-empty array 'plugins'")
    else:
        names: set[str] = set()
        for index, entry in enumerate(plugins):
            if not isinstance(entry, dict):
                errors.append(f"plugins[{index}] must be an object")
                continue
            validate_plugin(entry, index, names, errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(
        f"Validated marketplace '{marketplace_name}' with "
        f"{len(plugins)} plugin(s)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
