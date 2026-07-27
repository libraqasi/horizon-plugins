#!/usr/bin/env python3
"""Validate and resolve a Horizon Bank synthetic-data config without generating data."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from horizon_data_core import resolve_config


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config", type=Path)
    parser.add_argument("--print-resolved", action="store_true")
    args = parser.parse_args()
    try:
        resolved = resolve_config(json.loads(args.config.read_text(encoding="utf-8")))
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"config validation failed: {exc}", file=sys.stderr)
        return 1
    if args.print_resolved:
        print(json.dumps(resolved, indent=2, sort_keys=True))
    else:
        print(f"Config is valid: {args.config.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
