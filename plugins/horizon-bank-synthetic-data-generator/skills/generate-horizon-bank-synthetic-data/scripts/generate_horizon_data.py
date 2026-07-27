#!/usr/bin/env python3
"""Generate portable Horizon Bank synthetic data from a JSON config."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from horizon_data_core import generate, load_narrative_overrides, prepare_output, resolve_config


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True, help="JSON generation config")
    parser.add_argument("--out", type=Path, required=True, help="New or known generated output directory")
    parser.add_argument("--seed", type=int)
    parser.add_argument("--scenario-date")
    parser.add_argument("--size", choices=["small", "medium", "large"])
    parser.add_argument("--customers", type=int)
    parser.add_argument("--history-days", type=int)
    parser.add_argument("--formats", nargs="+", choices=["bundle-json", "jsonl", "csv", "sqlite", "mongo"])
    parser.add_argument("--narrative-overrides", type=Path)
    parser.add_argument("--force", action="store_true", help="Replace only recognized generated files")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        raw = json.loads(args.config.read_text(encoding="utf-8"))
        config = resolve_config(
            raw,
            {
                "seed": args.seed,
                "scenario_date": args.scenario_date,
                "size": args.size,
                "customers": args.customers,
                "history_days": args.history_days,
                "formats": args.formats,
            },
        )
        prepare_output(args.out, args.force)
        narrative_overrides = load_narrative_overrides(args.narrative_overrides) if args.narrative_overrides else None
        manifest = generate(config, args.out.expanduser().resolve(), narrative_overrides)
        print(
            json.dumps(
                {
                    "dataset_id": manifest["dataset_id"],
                    "output": str(args.out.expanduser().resolve()),
                    "counts": manifest["counts"],
                },
                indent=2,
            )
        )
        return 0
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"generation failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
