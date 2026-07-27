#!/usr/bin/env python3
"""Deterministic, dependency-free synthetic banking data engine."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import random
import shutil
import sqlite3
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable

SCHEMA_VERSION = "1.0.0"
ARCHETYPES = [
    "youth-guardian",
    "emerging-adult",
    "everyday-banking",
    "family-homebuyer",
    "affluent-investor",
    "small-business-owner",
    "gig-multi-income",
    "retiree-fixed-income",
    "agentic-digital-wallet",
]
COLLECTIONS = [
    "customers",
    "households",
    "businesses",
    "accounts",
    "cards",
    "merchants",
    "transactions",
    "incomes",
    "loans",
    "investments",
    "budgets",
    "goals",
    "rewards",
    "alerts",
    "service_interactions",
    "devices",
    "disputes",
    "delegations",
    "events",
]
MODULES = set(COLLECTIONS) - {"customers", "merchants", "events"}
OVERLAYS = {
    "payday",
    "low-balance",
    "overdraft-risk",
    "pending-card-charge",
    "card-dispute",
    "fraud-review",
    "missed-payment",
    "travel",
    "move-home",
    "job-change",
    "healthcare-expense",
    "new-dependent",
}
SCALE_PRESETS = {
    "small": {"customers": 9, "history_days": 90, "min_transactions": 25, "max_transactions": 75},
    "medium": {"customers": 500, "history_days": 365, "min_transactions": 150, "max_transactions": 350},
    "large": {"customers": 10_000, "history_days": 730, "min_transactions": 400, "max_transactions": 900},
}
FIRST_NAMES = ["Avery", "Jordan", "Casey", "Riley", "Morgan", "Taylor", "Cameron", "Quinn", "Skyler"]
LAST_NAMES = ["Rivera", "Chen", "Patel", "Brooks", "Nguyen", "Johnson", "Garcia", "Williams", "Davis"]
CITIES = [
    ("Charlotte", "NC", "28202"),
    ("Austin", "TX", "78701"),
    ("Denver", "CO", "80202"),
    ("Seattle", "WA", "98101"),
    ("Chicago", "IL", "60601"),
    ("Phoenix", "AZ", "85004"),
]
MERCHANTS = [
    ("Fresh Basket", "groceries"),
    ("Metro Transit", "transportation"),
    ("Harbor Coffee", "dining"),
    ("Cloudline Mobile", "utilities"),
    ("Northstar Pharmacy", "healthcare"),
    ("Juniper Market", "shopping"),
    ("Civic Energy", "utilities"),
    ("Lumen Travel", "travel"),
]
ACCOUNT_BLUEPRINTS = {
    "youth-guardian": [("checking", "Horizon Clear Access"), ("savings", "Horizon Goal Savings")],
    "emerging-adult": [("checking", "Horizon Everyday Checking"), ("savings", "Horizon Goal Savings")],
    "everyday-banking": [("checking", "Horizon Everyday Checking"), ("savings", "Horizon Way2Save")],
    "family-homebuyer": [("checking", "Horizon Everyday Checking"), ("savings", "Horizon Home Reserve")],
    "affluent-investor": [("checking", "Horizon Premier Checking"), ("savings", "Horizon Platinum Savings"), ("investment", "Horizon Advisory Portfolio")],
    "small-business-owner": [("business_checking", "Horizon Initiate Business Checking"), ("business_savings", "Horizon Business Market Rate")],
    "gig-multi-income": [("checking", "Horizon Everyday Checking"), ("savings", "Horizon Tax Reserve")],
    "retiree-fixed-income": [("checking", "Horizon Prime Checking"), ("savings", "Horizon Platinum Savings"), ("investment", "Horizon Retirement Portfolio")],
    "agentic-digital-wallet": [("checking", "Horizon Digital Checking"), ("savings", "Horizon Smart Reserve")],
}


def stable_id(seed: int, kind: str, *parts: object) -> str:
    material = ":".join([SCHEMA_VERSION, str(seed), kind, *(str(part) for part in parts)])
    return f"{kind[:4]}_{hashlib.sha256(material.encode()).hexdigest()[:20]}"


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def iso_day(value: date) -> str:
    return value.isoformat()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    if not path.exists():
        return
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def validate_input_config(raw: dict[str, Any]) -> None:
    """Dependency-free enforcement of assets/config.schema.json."""
    if not isinstance(raw, dict):
        raise ValueError("config must be a JSON object")
    required_top = {"schema_version", "dataset", "scale", "archetypes", "modules", "outputs"}
    allowed_top = required_top | {"overlays", "narrative"}
    missing = sorted(required_top - set(raw))
    extra = sorted(set(raw) - allowed_top)
    if missing or extra:
        raise ValueError(f"config keys are invalid; missing={missing}, unexpected={extra}")

    dataset = raw.get("dataset")
    dataset_required = {"name", "seed", "scenario_date", "time_mode", "timezone", "locale", "currency"}
    if not isinstance(dataset, dict):
        raise ValueError("dataset must be an object")
    missing = sorted(dataset_required - set(dataset))
    extra = sorted(set(dataset) - dataset_required)
    if missing or extra:
        raise ValueError(f"dataset keys are invalid; missing={missing}, unexpected={extra}")
    if not isinstance(dataset["name"], str) or not dataset["name"].strip():
        raise ValueError("dataset.name must be a non-empty string")
    if not isinstance(dataset["seed"], int) or isinstance(dataset["seed"], bool):
        raise ValueError("dataset.seed must be an integer")
    if not isinstance(dataset["scenario_date"], str):
        raise ValueError("dataset.scenario_date must be an ISO date string")
    date.fromisoformat(dataset["scenario_date"])
    if dataset["time_mode"] not in {"fixed", "rolling"}:
        raise ValueError("dataset.time_mode must be fixed or rolling")
    if not isinstance(dataset["timezone"], str) or "/" not in dataset["timezone"]:
        raise ValueError("dataset.timezone must be an IANA-style timezone")
    if not isinstance(dataset["locale"], str) or len(dataset["locale"]) < 2:
        raise ValueError("dataset.locale must be a locale string")
    if (
        not isinstance(dataset["currency"], str)
        or len(dataset["currency"]) != 3
        or dataset["currency"] != dataset["currency"].upper()
    ):
        raise ValueError("dataset.currency must be an uppercase three-letter code")

    scale = raw.get("scale")
    allowed_scale = {"preset", "customers", "history_days", "min_transactions", "max_transactions"}
    if not isinstance(scale, dict) or "preset" not in scale or set(scale) - allowed_scale:
        raise ValueError("scale must contain a valid preset and only supported scale keys")
    if scale["preset"] not in {"small", "medium", "large", "custom"}:
        raise ValueError("scale.preset must be small, medium, large, or custom")
    for key in allowed_scale - {"preset"}:
        if key in scale and (not isinstance(scale[key], int) or isinstance(scale[key], bool) or scale[key] < 0):
            raise ValueError(f"scale.{key} must be a non-negative integer")

    archetypes = raw.get("archetypes")
    if not isinstance(archetypes, dict) or set(archetypes) - {"include", "weights"}:
        raise ValueError("archetypes must contain only include and optional weights")
    included = archetypes.get("include")
    if not isinstance(included, list) or not included or any(not isinstance(item, str) for item in included):
        raise ValueError("archetypes.include must be a non-empty string array")

    modules = raw.get("modules")
    if (
        not isinstance(modules, list)
        or any(not isinstance(item, str) for item in modules)
        or len(modules) != len(set(modules))
        or set(modules) - MODULES
    ):
        raise ValueError("modules must be a unique array of supported module names")
    overlays = raw.get("overlays", [])
    if (
        not isinstance(overlays, list)
        or any(not isinstance(item, str) for item in overlays)
        or len(overlays) != len(set(overlays))
        or set(overlays) - OVERLAYS
    ):
        raise ValueError("overlays must be a unique array of supported overlay names")

    outputs = raw.get("outputs")
    if not isinstance(outputs, dict) or set(outputs) != {"formats"}:
        raise ValueError("outputs must contain only formats")
    formats = outputs["formats"]
    supported_formats = {"bundle-json", "jsonl", "csv", "sqlite", "mongo"}
    if (
        not isinstance(formats, list)
        or not formats
        or any(not isinstance(item, str) for item in formats)
        or len(formats) != len(set(formats))
        or set(formats) - supported_formats
    ):
        raise ValueError("outputs.formats must be a non-empty unique array of supported formats")
    narrative = raw.get("narrative", {"mode": "template"})
    if not isinstance(narrative, dict) or set(narrative) - {"mode"}:
        raise ValueError("narrative may contain only mode")
    if narrative.get("mode", "template") not in {"none", "template", "slots"}:
        raise ValueError("narrative.mode must be none, template, or slots")


def resolve_config(raw: dict[str, Any], overrides: dict[str, Any] | None = None) -> dict[str, Any]:
    validate_input_config(raw)
    config = json.loads(json.dumps(raw))
    if config.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(f"schema_version must be {SCHEMA_VERSION}")
    dataset = config.setdefault("dataset", {})
    scale = config.setdefault("scale", {})
    overrides = overrides or {}
    for key in ("seed", "scenario_date"):
        if overrides.get(key) is not None:
            dataset[key] = overrides[key]
    if overrides.get("size"):
        scale["preset"] = overrides["size"]
        scale.update(SCALE_PRESETS[overrides["size"]])
    if overrides.get("customers") is not None:
        scale["customers"] = overrides["customers"]
        scale["preset"] = "custom"
    if overrides.get("history_days") is not None:
        scale["history_days"] = overrides["history_days"]
        scale["preset"] = "custom"
    if overrides.get("formats"):
        config.setdefault("outputs", {})["formats"] = overrides["formats"]

    preset_name = scale.get("preset", "small")
    if preset_name in SCALE_PRESETS:
        preset = SCALE_PRESETS[preset_name]
        for key, value in preset.items():
            scale.setdefault(key, value)
    elif preset_name != "custom":
        raise ValueError(f"Unknown scale preset: {preset_name}")
    scale.setdefault("customers", 9)
    scale.setdefault("history_days", 90)
    scale.setdefault("min_transactions", 25)
    scale.setdefault("max_transactions", 75)
    if not 1 <= int(scale["customers"]) <= 100_000:
        raise ValueError("customers must be between 1 and 100000")
    if not 1 <= int(scale["history_days"]) <= 3650:
        raise ValueError("history_days must be between 1 and 3650")
    if int(scale["min_transactions"]) > int(scale["max_transactions"]):
        raise ValueError("min_transactions cannot exceed max_transactions")

    if dataset.get("time_mode", "fixed") == "rolling":
        dataset["scenario_date"] = date.today().isoformat()
    scenario_date = date.fromisoformat(dataset.get("scenario_date", "2026-07-27"))
    dataset["resolved_scenario_date"] = scenario_date.isoformat()
    dataset.setdefault("seed", 4242)
    dataset.setdefault("name", "horizon-synthetic-data")
    dataset.setdefault("locale", "en-US")
    dataset.setdefault("currency", "USD")
    dataset.setdefault("timezone", "America/New_York")
    dataset.setdefault("time_mode", "fixed")
    dataset["synthetic"] = True
    dataset["institution"] = "Horizon Bank"

    included = config.setdefault("archetypes", {}).setdefault("include", ARCHETYPES)
    unknown = sorted(set(included) - set(ARCHETYPES))
    if unknown or not included:
        raise ValueError(f"Unknown or empty archetype selection: {unknown}")
    weights = config["archetypes"].get("weights")
    if weights is not None:
        if not isinstance(weights, dict) or sorted(weights) != sorted(included):
            raise ValueError("archetype weights must provide exactly one value for every included archetype")
        if any(not isinstance(value, (int, float)) or value < 0 for value in weights.values()) or sum(weights.values()) <= 0:
            raise ValueError("archetype weights must be non-negative and total more than zero")
    formats = config.setdefault("outputs", {}).setdefault("formats", ["bundle-json", "jsonl"])
    supported = {"bundle-json", "jsonl", "csv", "sqlite", "mongo"}
    unsupported = sorted(set(formats) - supported)
    if unsupported:
        raise ValueError(f"Unsupported output formats: {unsupported}")
    config.setdefault("modules", ["accounts", "transactions"])
    config.setdefault("overlays", [])
    narrative = config.setdefault("narrative", {"mode": "template"})
    if narrative.get("mode", "template") not in {"none", "template", "slots"}:
        raise ValueError("narrative.mode must be none, template, or slots")
    return config


class DatasetWriter:
    """Streams canonical JSONL, with optional SQLite export."""

    def __init__(self, out_dir: Path, include_sqlite: bool):
        self.out_dir = out_dir
        self.jsonl_dir = out_dir / "jsonl"
        self.jsonl_dir.mkdir(parents=True)
        self.handles = {
            name: (self.jsonl_dir / f"{name}.jsonl").open("w", encoding="utf-8", newline="\n")
            for name in COLLECTIONS
        }
        self.counts: dict[str, int] = defaultdict(int)
        self.connection: sqlite3.Connection | None = None
        if include_sqlite:
            self.connection = sqlite3.connect(out_dir / "horizon_synthetic.sqlite")
            self.connection.execute("PRAGMA journal_mode=WAL")
            self.connection.execute("CREATE TABLE metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL)")
            for name in COLLECTIONS:
                self.connection.execute(
                    f'CREATE TABLE "{name}" ('
                    "id TEXT PRIMARY KEY, customer_id TEXT, account_id TEXT, event_date TEXT, payload TEXT NOT NULL)"
                )
                self.connection.execute(f'CREATE INDEX "idx_{name}_customer" ON "{name}" (customer_id)')
                self.connection.execute(f'CREATE INDEX "idx_{name}_account" ON "{name}" (account_id)')

    def write(self, collection: str, record: dict[str, Any]) -> None:
        if collection not in self.handles:
            raise KeyError(collection)
        encoded = canonical_json(record)
        self.handles[collection].write(encoded + "\n")
        self.counts[collection] += 1
        if self.connection is not None:
            record_id = record.get("id")
            self.connection.execute(
                f'INSERT INTO "{collection}" (id, customer_id, account_id, event_date, payload) VALUES (?, ?, ?, ?, ?)',
                (
                    record_id,
                    record.get("customer_id"),
                    record.get("account_id"),
                    record.get("event_date") or record.get("posted_date") or record.get("created_date"),
                    encoded,
                ),
            )
            if self.counts[collection] % 5000 == 0:
                self.connection.commit()

    def close(self, metadata: dict[str, Any]) -> None:
        for handle in self.handles.values():
            handle.close()
        if self.connection is not None:
            for key, value in metadata.items():
                self.connection.execute(
                    "INSERT OR REPLACE INTO metadata (key, value) VALUES (?, ?)",
                    (key, canonical_json(value)),
                )
            self.connection.commit()
            self.connection.execute("PRAGMA wal_checkpoint(TRUNCATE)")
            self.connection.execute("PRAGMA journal_mode=DELETE")
            self.connection.close()


def _payment_minor(principal_minor: int, annual_rate_bps: int, remaining_months: int) -> int:
    monthly_rate = annual_rate_bps / 10_000 / 12
    if monthly_rate == 0:
        return round(principal_minor / remaining_months)
    return round(principal_minor * monthly_rate / (1 - math.pow(1 + monthly_rate, -remaining_months)))


def _transaction_count(scale: dict[str, Any], rng: random.Random) -> int:
    minimum = int(scale["min_transactions"])
    maximum = int(scale["max_transactions"])
    history_days = int(scale["history_days"])
    return min(history_days * 4, rng.randint(minimum, maximum))


def _base_balance(archetype: str, rng: random.Random) -> int:
    ranges = {
        "youth-guardian": (15_000, 120_000),
        "emerging-adult": (25_000, 250_000),
        "everyday-banking": (120_000, 700_000),
        "family-homebuyer": (300_000, 1_800_000),
        "affluent-investor": (2_000_000, 12_000_000),
        "small-business-owner": (600_000, 4_000_000),
        "gig-multi-income": (60_000, 500_000),
        "retiree-fixed-income": (350_000, 2_000_000),
        "agentic-digital-wallet": (100_000, 800_000),
    }
    return rng.randint(*ranges[archetype])


def _narrative(archetype: str, overlays: list[str], mode: str) -> dict[str, Any]:
    if mode == "none":
        return {}
    facts = {
        "archetype": archetype,
        "active_overlays": overlays,
        "institution": "Horizon Bank",
        "synthetic": True,
    }
    if mode == "slots":
        return {"profile_summary": None, "narrative_facts": facts}
    overlay_text = f" Current scenario: {', '.join(overlays)}." if overlays else ""
    return {
        "profile_summary": f"Synthetic Horizon Bank customer representing the {archetype} archetype.{overlay_text}",
        "narrative_facts": facts,
    }


def _make_transactions(
    seed: int,
    customer_index: int,
    customer_id: str,
    account_id: str,
    scenario: date,
    history_days: int,
    count: int,
    merchant_records: list[dict[str, Any]],
    overlays: list[str],
    rng: random.Random,
) -> list[dict[str, Any]]:
    transactions: list[dict[str, Any]] = []
    for index in range(count):
        days_ago = int(index * max(1, history_days - 1) / max(1, count - 1))
        posted = scenario - timedelta(days=days_ago)
        is_income = index % 12 == 0
        if is_income:
            amount = rng.randint(75_000, 185_000)
            merchant_id = None
            description = "Synthetic direct deposit"
            category = "income"
            direction = "credit"
        else:
            merchant = merchant_records[index % len(merchant_records)]
            amount = -rng.randint(450, 18_500)
            merchant_id = merchant["id"]
            description = merchant["name"]
            category = merchant["category"]
            direction = "debit"
        pending_overlay = "pending-card-charge" in overlays or "overdraft-risk" in overlays
        status = "pending" if index == 1 and pending_overlay else "posted"
        if index == 1 and "overdraft-risk" in overlays:
            amount = -8_000
        transactions.append(
            {
                "id": stable_id(seed, "transaction", customer_index, index),
                "customer_id": customer_id,
                "account_id": account_id,
                "merchant_id": merchant_id,
                "posted_date": iso_day(posted),
                "event_date": iso_day(posted),
                "description": description,
                "category": category,
                "direction": direction,
                "amount_minor": amount,
                "currency": "USD",
                "status": status,
                "synthetic": True,
            }
        )
    return transactions


def load_narrative_overrides(override_path: Path) -> dict[str, str]:
    """Load whitelisted LLM-authored summaries without allowing financial edits."""
    content = override_path.read_text(encoding="utf-8")
    if content.lstrip().startswith("["):
        raw = json.loads(content)
    else:
        raw = [json.loads(line) for line in content.splitlines() if line.strip()]
    if not isinstance(raw, list):
        raise ValueError("Narrative overrides must be a JSON array or JSONL records")
    result: dict[str, str] = {}
    for item in raw:
        if not isinstance(item, dict) or item.get("field") != "profile_summary":
            raise ValueError("Narrative overrides may only target profile_summary")
        entity_id, value = item.get("entity_id"), item.get("value", item.get("text"))
        if not isinstance(entity_id, str) or not isinstance(value, str) or not value.strip() or len(value) > 800:
            raise ValueError("Narrative override needs entity_id and a 1–800 character string value")
        result[entity_id] = value.strip()
    return result


def generate(
    config: dict[str, Any],
    out_dir: Path,
    narrative_overrides: dict[str, str] | None = None,
) -> dict[str, Any]:
    dataset = config["dataset"]
    scale = config["scale"]
    formats = set(config["outputs"]["formats"])
    modules = set(config["modules"])
    seed = int(dataset["seed"])
    scenario = date.fromisoformat(dataset["resolved_scenario_date"])
    customers_count = int(scale["customers"])
    history_days = int(scale["history_days"])
    selected_archetypes = config["archetypes"]["include"]
    archetype_weights = config["archetypes"].get("weights")
    configured_overlays = config.get("overlays", [])
    narrative_mode = config.get("narrative", {}).get("mode", "template")
    if narrative_overrides:
        valid_override_ids = {stable_id(seed, "customer", index) for index in range(customers_count)}
        unknown_override_ids = sorted(set(narrative_overrides) - valid_override_ids)
        if unknown_override_ids:
            raise ValueError(f"Narrative overrides reference unknown customer IDs: {unknown_override_ids[:5]}")
    writer = DatasetWriter(out_dir, "sqlite" in formats)
    narrative_slot_handle = (
        (out_dir / "narrative-slots.jsonl").open("w", encoding="utf-8", newline="\n")
        if narrative_mode == "slots"
        else None
    )

    merchant_records = [
        {
            "id": stable_id(seed, "merchant", index),
            "name": name,
            "category": category,
            "synthetic": True,
        }
        for index, (name, category) in enumerate(MERCHANTS)
    ]
    if "transactions" in modules:
        for merchant in merchant_records:
            writer.write("merchants", merchant)

    for customer_index in range(customers_count):
        rng = random.Random(f"{seed}:customer:{customer_index}")
        archetype = (
            rng.choices(
                selected_archetypes,
                weights=[archetype_weights[name] for name in selected_archetypes],
                k=1,
            )[0]
            if archetype_weights
            else selected_archetypes[customer_index % len(selected_archetypes)]
        )
        customer_id = stable_id(seed, "customer", customer_index)
        first = FIRST_NAMES[customer_index % len(FIRST_NAMES)]
        last = LAST_NAMES[(customer_index * 5 + seed) % len(LAST_NAMES)]
        city, state, postal = CITIES[customer_index % len(CITIES)]
        customer_overlays = [
            overlay
            for overlay_index, overlay in enumerate(configured_overlays)
            if overlay_index % customers_count == customer_index
        ]
        birth_year = {
            "youth-guardian": 2012,
            "emerging-adult": 2004,
            "retiree-fixed-income": 1955,
        }.get(archetype, 1980 + (customer_index % 18))
        customer = {
            "id": customer_id,
            "archetype": archetype,
            "name": {"first": first, "last": last, "display": f"{first} {last}"},
            "date_of_birth": f"{birth_year}-{(customer_index % 12) + 1:02d}-{(customer_index % 27) + 1:02d}",
            "contact": {
                "email": f"{first.lower()}.{last.lower()}.{customer_index}@horizon-demo.example",
                "phone": f"+1-212-555-{100 + customer_index % 100:04d}",
            },
            "address": {
                "line1": f"{100 + customer_index} Demo Avenue",
                "city": city,
                "state": state,
                "postal_code": postal,
                "country": "US",
            },
            "preferred_language": "en-US",
            "relationship_start_date": iso_day(scenario - timedelta(days=365 * (1 + customer_index % 12))),
            "active_overlays": customer_overlays,
            "synthetic": True,
            **_narrative(archetype, customer_overlays, narrative_mode),
        }
        if narrative_overrides and customer_id in narrative_overrides:
            customer["profile_summary"] = narrative_overrides[customer_id]
        writer.write("customers", customer)
        if narrative_slot_handle is not None:
            narrative_slot_handle.write(
                canonical_json(
                    {
                        "entity_id": customer_id,
                        "field": "profile_summary",
                        "facts": customer["narrative_facts"],
                    }
                )
                + "\n"
            )

        if "households" in modules and (
            archetype in {"youth-guardian", "family-homebuyer", "affluent-investor", "retiree-fixed-income"}
            or "new-dependent" in customer_overlays
        ):
            writer.write(
                "households",
                {
                    "id": stable_id(seed, "household", customer_index),
                    "customer_id": customer_id,
                    "member_count": 2 + customer_index % 3,
                    "relationship": "primary",
                    "synthetic": True,
                },
            )
        business_id = None
        if "businesses" in modules and archetype == "small-business-owner":
            business_id = stable_id(seed, "business", customer_index)
            writer.write(
                "businesses",
                {
                    "id": business_id,
                    "customer_id": customer_id,
                    "legal_name": f"{last} Studio LLC",
                    "industry": "professional_services",
                    "employee_count": 4 + customer_index % 8,
                    "annual_revenue_minor": rng.randint(18_000_000, 75_000_000),
                    "currency": "USD",
                    "synthetic": True,
                },
            )

        account_blueprints = ACCOUNT_BLUEPRINTS[archetype]
        account_ids = [stable_id(seed, "account", customer_index, account_index) for account_index in range(len(account_blueprints))]
        primary_account_id = account_ids[0]
        transaction_records = []
        if "transactions" in modules:
            transaction_records = _make_transactions(
                seed,
                customer_index,
                customer_id,
                primary_account_id,
                scenario,
                history_days,
                _transaction_count(scale, rng),
                merchant_records,
                customer_overlays,
                rng,
            )
        posted_sum = sum(item["amount_minor"] for item in transaction_records if item["status"] == "posted")
        pending_debits = sum(item["amount_minor"] for item in transaction_records if item["status"] == "pending" and item["amount_minor"] < 0)
        desired_primary = (
            4_500
            if "low-balance" in customer_overlays
            else 5_500
            if "overdraft-risk" in customer_overlays
            else _base_balance(archetype, rng)
        )

        for account_index, ((account_type, product_name), account_id) in enumerate(zip(account_blueprints, account_ids)):
            desired = desired_primary if account_index == 0 else max(25_000, desired_primary * (account_index + 2))
            opening = desired - posted_sum if account_index == 0 else desired
            account = {
                "id": account_id,
                "customer_id": customer_id,
                "business_id": business_id if account_type.startswith("business") else None,
                "type": account_type,
                "product_name": product_name,
                "display_last4": f"{(seed + customer_index * 37 + account_index * 101) % 10_000:04d}",
                "opened_date": iso_day(scenario - timedelta(days=400 + customer_index * 17)),
                "opening_balance_minor": opening,
                "posted_balance_minor": desired,
                "available_balance_minor": desired + (pending_debits if account_index == 0 else 0),
                "currency": "USD",
                "status": "open",
                "synthetic": True,
            }
            writer.write("accounts", account)

        for transaction in transaction_records:
            writer.write("transactions", transaction)

        if "cards" in modules:
            card_id = stable_id(seed, "card", customer_index)
            limit_minor = max(100_000, min(5_000_000, desired_primary * 3))
            current_balance = rng.randint(0, max(1, int(limit_minor * 0.65)))
            writer.write(
                "cards",
                {
                    "id": card_id,
                    "customer_id": customer_id,
                    "account_id": primary_account_id,
                    "network": "Visa",
                    "product_name": "Horizon Active Cash",
                    "display_last4": f"{(seed * 3 + customer_index * 71) % 10_000:04d}",
                    "credit_limit_minor": limit_minor,
                    "current_balance_minor": current_balance,
                    "available_credit_minor": limit_minor - current_balance,
                    "utilization_bps": round(current_balance / limit_minor * 10_000),
                    "currency": "USD",
                    "status": "active",
                    "synthetic": True,
                },
            )

        if "incomes" in modules:
            income_sources = 3 if archetype == "gig-multi-income" else 1
            for income_index in range(income_sources):
                writer.write(
                    "incomes",
                    {
                        "id": stable_id(seed, "income", customer_index, income_index),
                        "customer_id": customer_id,
                        "account_id": primary_account_id,
                        "source": (
                            "Synthetic new employer"
                            if income_index == 0 and "job-change" in customer_overlays
                            else "Synthetic employer"
                            if income_index == 0
                            else f"Synthetic platform {income_index}"
                        ),
                        "cadence": "biweekly" if income_index == 0 else "variable",
                        "typical_amount_minor": rng.randint(65_000, 220_000),
                        "currency": "USD",
                        "synthetic": True,
                    },
                )

        if "loans" in modules and archetype in {"emerging-adult", "family-homebuyer", "affluent-investor", "small-business-owner"}:
            loan_type = "mortgage" if archetype == "family-homebuyer" else "installment"
            principal = rng.randint(1_500_000, 35_000_000 if loan_type == "mortgage" else 4_500_000)
            rate_bps = rng.randint(350, 825)
            months = rng.randint(18, 300 if loan_type == "mortgage" else 72)
            writer.write(
                "loans",
                {
                    "id": stable_id(seed, "loan", customer_index),
                    "customer_id": customer_id,
                    "type": loan_type,
                    "principal_balance_minor": principal,
                    "annual_rate_bps": rate_bps,
                    "remaining_months": months,
                    "scheduled_payment_minor": _payment_minor(principal, rate_bps, months),
                    "next_payment_date": iso_day(scenario + timedelta(days=14)),
                    "currency": "USD",
                    "status": "late" if "missed-payment" in customer_overlays else "current",
                    "synthetic": True,
                },
            )

        if "investments" in modules and archetype in {"affluent-investor", "retiree-fixed-income"}:
            market_value = desired_primary * 12
            writer.write(
                "investments",
                {
                    "id": stable_id(seed, "investment", customer_index),
                    "customer_id": customer_id,
                    "account_id": account_ids[-1],
                    "portfolio_name": "Horizon Balanced Growth" if archetype == "affluent-investor" else "Horizon Retirement Income",
                    "market_value_minor": market_value,
                    "cost_basis_minor": round(market_value * 0.82),
                    "currency": "USD",
                    "as_of_date": iso_day(scenario),
                    "synthetic": True,
                },
            )

        recent_cutoff = scenario - timedelta(days=29)
        if "budgets" in modules:
            categories = {"groceries", "dining", "transportation", "shopping"}
            for budget_index, category in enumerate(sorted(categories)):
                actual = -sum(
                    transaction["amount_minor"]
                    for transaction in transaction_records
                    if transaction["status"] == "posted"
                    and transaction["category"] == category
                    and date.fromisoformat(transaction["posted_date"]) >= recent_cutoff
                )
                writer.write(
                    "budgets",
                    {
                        "id": stable_id(seed, "budget", customer_index, budget_index),
                        "customer_id": customer_id,
                        "category": category,
                        "period_start": iso_day(recent_cutoff),
                        "period_end": iso_day(scenario),
                        "limit_minor": max(25_000, actual + 10_000),
                        "actual_minor": actual,
                        "currency": "USD",
                        "synthetic": True,
                    },
                )

        if "goals" in modules:
            target = max(100_000, desired_primary * 4)
            writer.write(
                "goals",
                {
                    "id": stable_id(seed, "goal", customer_index),
                    "customer_id": customer_id,
                    "name": "Emergency reserve",
                    "target_minor": target,
                    "current_minor": min(target, max(0, desired_primary)),
                    "target_date": iso_day(scenario + timedelta(days=365)),
                    "currency": "USD",
                    "synthetic": True,
                },
            )

        if "rewards" in modules:
            writer.write(
                "rewards",
                {
                    "id": stable_id(seed, "reward", customer_index),
                    "customer_id": customer_id,
                    "program": "Horizon Rewards",
                    "available_points": rng.randint(500, 45_000),
                    "as_of_date": iso_day(scenario),
                    "synthetic": True,
                },
            )

        if "alerts" in modules:
            alert_kind = (
                "low_balance"
                if "low-balance" in customer_overlays
                else "fraud_review"
                if "fraud-review" in customer_overlays
                else "missed_payment"
                if "missed-payment" in customer_overlays
                else "weekly_summary"
            )
            writer.write(
                "alerts",
                {
                    "id": stable_id(seed, "alert", customer_index),
                    "customer_id": customer_id,
                    "account_id": primary_account_id,
                    "type": alert_kind,
                    "created_date": iso_day(scenario),
                    "status": "unread",
                    "message": (
                        "Synthetic low-balance scenario"
                        if alert_kind == "low_balance"
                        else "Synthetic fraud-review scenario"
                        if alert_kind == "fraud_review"
                        else "Synthetic missed-payment scenario"
                        if alert_kind == "missed_payment"
                        else "Synthetic weekly account summary"
                    ),
                    "synthetic": True,
                },
            )

        if "service_interactions" in modules:
            writer.write(
                "service_interactions",
                {
                    "id": stable_id(seed, "service", customer_index),
                    "customer_id": customer_id,
                    "channel": "voice" if customer_index % 2 == 0 else "chat",
                    "topic": "account_summary",
                    "occurred_at": f"{scenario.isoformat()}T14:30:00Z",
                    "resolution": "self_service",
                    "synthetic": True,
                },
            )

        if "devices" in modules:
            writer.write(
                "devices",
                {
                    "id": stable_id(seed, "device", customer_index),
                    "customer_id": customer_id,
                    "type": "mobile",
                    "nickname": "Synthetic phone",
                    "trusted": True,
                    "last_seen_at": f"{scenario.isoformat()}T13:45:00Z",
                    "synthetic": True,
                },
            )

        if "card-dispute" in customer_overlays and "disputes" in modules and transaction_records:
            disputed = next(
                (
                    item
                    for item in transaction_records
                    if item["amount_minor"] < 0 and item["status"] == "posted"
                ),
                transaction_records[0],
            )
            writer.write(
                "disputes",
                {
                    "id": stable_id(seed, "dispute", customer_index),
                    "customer_id": customer_id,
                    "account_id": primary_account_id,
                    "transaction_id": disputed["id"],
                    "opened_date": iso_day(scenario),
                    "amount_minor": -disputed["amount_minor"],
                    "currency": "USD",
                    "status": "under_review",
                    "synthetic": True,
                },
            )

        if "delegations" in modules and archetype in {"youth-guardian", "small-business-owner", "retiree-fixed-income", "agentic-digital-wallet"}:
            writer.write(
                "delegations",
                {
                    "id": stable_id(seed, "delegation", customer_index),
                    "customer_id": customer_id,
                    "account_id": primary_account_id,
                    "delegate_display_name": "Synthetic delegate",
                    "scope": ["view_balances", "draft_payment"],
                    "requires_primary_approval": True,
                    "status": "active",
                    "synthetic": True,
                },
            )

        for overlay in customer_overlays:
            writer.write(
                "events",
                {
                    "id": stable_id(seed, "event", customer_index, overlay),
                    "customer_id": customer_id,
                    "account_id": primary_account_id,
                    "event_date": iso_day(scenario),
                    "type": overlay,
                    "state": "active",
                    "synthetic": True,
                },
            )

    if narrative_slot_handle is not None:
        narrative_slot_handle.close()
    dataset_id = stable_id(seed, "dataset", dataset["name"], scenario.isoformat(), customers_count)
    preliminary_metadata = {
        "schema_version": SCHEMA_VERSION,
        "dataset_id": dataset_id,
        "dataset_name": dataset["name"],
        "scenario_date": scenario.isoformat(),
        "synthetic": True,
        "institution": "Horizon Bank",
        "narrative": {
            "mode": narrative_mode,
            "override_count": len(narrative_overrides or {}),
        },
    }
    writer.close(preliminary_metadata)

    if "csv" in formats:
        export_csv(out_dir)
    if "mongo" in formats:
        export_mongo(out_dir)
    if "bundle-json" in formats:
        export_bundle(out_dir, preliminary_metadata)

    files: dict[str, dict[str, Any]] = {}
    for path in sorted(item for item in out_dir.rglob("*") if item.is_file() and item.name != "manifest.json"):
        relative = path.relative_to(out_dir).as_posix()
        files[relative] = {"sha256": sha256_file(path), "bytes": path.stat().st_size}
    manifest = {
        **preliminary_metadata,
        "config": config,
        "counts": {name: writer.counts.get(name, 0) for name in COLLECTIONS},
        "files": files,
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def export_csv(out_dir: Path) -> None:
    csv_dir = out_dir / "csv"
    csv_dir.mkdir()
    fields = ["id", "customer_id", "account_id", "event_date", "payload_json"]
    for collection in COLLECTIONS:
        with (csv_dir / f"{collection}.csv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            for record in read_jsonl(out_dir / "jsonl" / f"{collection}.jsonl"):
                writer.writerow(
                    {
                        "id": record.get("id", ""),
                        "customer_id": record.get("customer_id", ""),
                        "account_id": record.get("account_id", ""),
                        "event_date": record.get("event_date") or record.get("posted_date") or record.get("created_date") or "",
                        "payload_json": canonical_json(record),
                    }
                )


def export_mongo(out_dir: Path) -> None:
    mongo_dir = out_dir / "mongo"
    mongo_dir.mkdir()
    for collection in COLLECTIONS:
        source = out_dir / "jsonl" / f"{collection}.jsonl"
        shutil.copyfile(source, mongo_dir / f"{collection}.jsonl")
    commands = [
        "# Each line is one MongoDB document. Choose your own local test database name.",
        *[
            f"mongoimport --db horizon_synthetic --collection {name} --file {name}.jsonl"
            for name in COLLECTIONS
        ],
    ]
    (mongo_dir / "IMPORT.md").write_text("\n".join(commands) + "\n", encoding="utf-8")


def export_bundle(out_dir: Path, metadata: dict[str, Any]) -> None:
    path = out_dir / "bundle.json"
    with path.open("w", encoding="utf-8") as handle:
        handle.write('{"metadata":')
        handle.write(canonical_json(metadata))
        for collection in COLLECTIONS:
            handle.write(f',"{collection}":[')
            first = True
            for record in read_jsonl(out_dir / "jsonl" / f"{collection}.jsonl"):
                if not first:
                    handle.write(",")
                handle.write(canonical_json(record))
                first = False
            handle.write("]")
        handle.write("}\n")


def prepare_output(out_dir: Path, force: bool = False) -> None:
    resolved = out_dir.expanduser().resolve()
    if resolved == Path(resolved.anchor) or resolved == Path.home().resolve():
        raise ValueError("Refusing to use a filesystem root or home directory as output")
    if resolved.exists():
        entries = list(resolved.iterdir())
        if entries and not force:
            raise FileExistsError(f"Output directory is not empty: {resolved}; pass --force to replace generated files")
        allowed = {
            "manifest.json",
            "bundle.json",
            "narrative-slots.jsonl",
            "horizon_synthetic.sqlite",
            "horizon_synthetic.sqlite-shm",
            "horizon_synthetic.sqlite-wal",
            "jsonl",
            "csv",
            "mongo",
        }
        unexpected = sorted(item.name for item in entries if item.name not in allowed)
        if unexpected:
            raise ValueError(f"Refusing --force because output contains unknown files: {unexpected}")
        if force:
            for item in entries:
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
    resolved.mkdir(parents=True, exist_ok=True)
