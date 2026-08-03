#!/usr/bin/env python3
"""Validate privacy, coherence, arithmetic, and export parity for generated fixtures."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
import sqlite3
import subprocess
import sys
import tempfile
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Iterable

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
BANNED_KEYS = re.compile(
    r"(^|_)(password|passcode|pin|ssn|social_security|routing_number|full_account_number|full_pan|pan)($|_)",
    re.IGNORECASE,
)
BANNED_INSTITUTIONS = re.compile(r"\bwells\s+fargo\b", re.IGNORECASE)
SAFE_PHONE = re.compile(r"^\+1-\d{3}-555-01\d{2}$")
SSN_VALUE = re.compile(r"^\d{3}-\d{2}-\d{4}$")
SECRET_VALUE = re.compile(r"^(?:sk-[A-Za-z0-9_-]{16,}|AKIA[A-Z0-9]{16}|Bearer\s+\S+)$")
DATE_KEYS = {
    "date_of_birth",
    "relationship_start_date",
    "opened_date",
    "posted_date",
    "event_date",
    "created_date",
    "as_of_date",
    "period_start",
    "period_end",
    "target_date",
    "next_payment_date",
}


def _hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _digest_add(current: int, payload: str) -> int:
    return (current + int.from_bytes(hashlib.sha256(payload.encode()).digest(), "big")) % (1 << 256)


def _luhn_valid(digits: str) -> bool:
    total = 0
    parity = len(digits) % 2
    for index, character in enumerate(digits):
        number = int(character)
        if index % 2 == parity:
            number *= 2
            if number > 9:
                number -= 9
        total += number
    return total % 10 == 0


def _jsonl(path: Path) -> Iterable[tuple[int, dict[str, Any]]]:
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if line.strip():
                try:
                    value = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise ValueError(f"{path}:{line_number}: invalid JSON: {exc}") from exc
                if not isinstance(value, dict):
                    raise ValueError(f"{path}:{line_number}: record must be an object")
                yield line_number, value


def _walk(value: Any, path: str = "") -> Iterable[tuple[str, Any]]:
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else key
            yield child_path, child
            yield from _walk(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk(child, f"{path}[{index}]")


def _loan_payment(principal_minor: int, annual_rate_bps: int, months: int) -> int:
    monthly_rate = annual_rate_bps / 10_000 / 12
    if monthly_rate == 0:
        return round(principal_minor / months)
    return round(principal_minor * monthly_rate / (1 - math.pow(1 + monthly_rate, -months)))


class Validation:
    def __init__(self, root: Path):
        self.root = root
        self.has_sqlite = (root / "horizon_synthetic.sqlite").is_file()
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.manifest: dict[str, Any] = {}
        self.ids: dict[str, set[str]] = defaultdict(set)
        self.accounts: dict[str, dict[str, Any]] = {}
        self.posted_delta_by_account: dict[str, int] = defaultdict(int)
        self.pending_debits_by_account: dict[str, int] = defaultdict(int)
        self.spend_by_customer_category_day: dict[tuple[str, str], dict[str, int]] = defaultdict(
            lambda: defaultdict(int)
        )
        self.customers: set[str] = set()
        self.merchants: set[str] = set()
        self.unresolved_transaction_refs: set[str] = set()
        self.disputes_by_transaction: dict[str, list[dict[str, Any]]] = defaultdict(list)
        self.actual_counts: dict[str, int] = defaultdict(int)
        self.payload_digests: dict[str, int] = defaultdict(int)
        self.expected_currency: str | None = None

    def error(self, message: str) -> None:
        if len(self.errors) < 500:
            self.errors.append(message)

    def warn(self, message: str) -> None:
        if len(self.warnings) < 500:
            self.warnings.append(message)

    def load_manifest(self) -> None:
        path = self.root / "manifest.json"
        if not path.is_file():
            self.error("manifest.json is missing")
            return
        try:
            self.manifest = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            self.error(f"manifest.json is unreadable: {exc}")
            return
        if self.manifest.get("schema_version") != "1.0.0":
            self.error("manifest schema_version must be 1.0.0")
        if self.manifest.get("synthetic") is not True:
            self.error("manifest synthetic flag must be true")
        if self.manifest.get("institution") != "Horizon Bank":
            self.error("manifest institution must be Horizon Bank")
        try:
            date.fromisoformat(self.manifest["scenario_date"])
        except (KeyError, TypeError, ValueError):
            self.error("manifest scenario_date must be an ISO date")
        configured_currency = self.manifest.get("config", {}).get("dataset", {}).get("currency")
        if not isinstance(configured_currency, str) or not re.fullmatch(r"[A-Z]{3}", configured_currency):
            self.error("manifest config dataset.currency must be an uppercase three-letter code")
        else:
            self.expected_currency = configured_currency

    def validate_file_inventory(self) -> None:
        for sidecar in ("horizon_synthetic.sqlite-wal", "horizon_synthetic.sqlite-shm"):
            if (self.root / sidecar).exists():
                self.error(f"unexpected mutable SQLite sidecar: {sidecar}")
        for relative, expected in self.manifest.get("files", {}).items():
            path = self.root / relative
            try:
                path.resolve().relative_to(self.root.resolve())
            except ValueError:
                self.error(f"manifest file escapes dataset root: {relative}")
                continue
            if not path.is_file():
                self.error(f"manifest file is missing: {relative}")
                continue
            if _hash(path) != expected.get("sha256"):
                self.error(f"hash mismatch: {relative}")
            if path.stat().st_size != expected.get("bytes"):
                self.error(f"byte-size mismatch: {relative}")

    def validate_record(self, collection: str, line_number: int, record: dict[str, Any]) -> None:
        location = f"jsonl/{collection}.jsonl:{line_number}"
        record_id = record.get("id")
        if not isinstance(record_id, str) or not record_id:
            self.error(f"{location}: missing string id")
        elif collection == "transactions" and self.has_sqlite:
            pass
        elif record_id in self.ids[collection]:
            self.error(f"{location}: duplicate id {record_id}")
        else:
            self.ids[collection].add(record_id)
        if record.get("synthetic") is not True:
            self.error(f"{location}: synthetic flag must be true")
        for field_path, value in _walk(record):
            key = field_path.rsplit(".", 1)[-1].split("[", 1)[0]
            if BANNED_KEYS.search(key):
                self.error(f"{location}: unsafe field {field_path}")
            if isinstance(value, str):
                if BANNED_INSTITUTIONS.search(value):
                    self.error(f"{location}: unrelated institution name in {field_path}")
                if "email" in key.lower() and not value.lower().endswith(".example"):
                    self.error(f"{location}: email must use a .example domain")
                if "phone" in key.lower() and not SAFE_PHONE.fullmatch(value):
                    self.error(f"{location}: phone must use a reserved +1-xxx-555-01xx range")
                if SSN_VALUE.fullmatch(value):
                    self.error(f"{location}: SSN-like value in {field_path}")
                if SECRET_VALUE.fullmatch(value):
                    self.error(f"{location}: credential-like value in {field_path}")
                digits = re.sub(r"\D", "", value)
                if re.fullmatch(r"[\d -]+", value) and 13 <= len(digits) <= 19 and _luhn_valid(digits):
                    self.error(f"{location}: payment-card-like value in {field_path}")
                if value.isdigit() and 9 <= len(value) <= 12 and not (
                    "phone" in key.lower() or key in {"postal_code", "display_last4"}
                ):
                    self.error(f"{location}: full routing/account-number-like value in {field_path}")
                if key in DATE_KEYS:
                    try:
                        parsed_date = date.fromisoformat(value)
                        scenario_date = date.fromisoformat(self.manifest["scenario_date"])
                        if key in {"target_date", "next_payment_date"} and parsed_date <= scenario_date:
                            self.error(f"{location}: {field_path} must be after the scenario date")
                        if key not in {"target_date", "next_payment_date"} and parsed_date > scenario_date:
                            self.error(f"{location}: {field_path} must not be after the scenario date")
                    except ValueError:
                        self.error(f"{location}: {field_path} must be an ISO date")
                    except (KeyError, TypeError):
                        self.error(f"{location}: scenario date is unavailable for {field_path}")
                if key in {"occurred_at", "last_seen_at"}:
                    try:
                        timestamp_date = date.fromisoformat(value[:10])
                        if timestamp_date > date.fromisoformat(self.manifest["scenario_date"]):
                            self.error(f"{location}: {field_path} must not be after the scenario date")
                    except (KeyError, TypeError, ValueError):
                        self.error(f"{location}: {field_path} must start with an ISO date")
            if key.endswith("_minor") and (not isinstance(value, int) or isinstance(value, bool)):
                self.error(f"{location}: {field_path} must be integer minor units")
            if key.endswith("_bps") and (not isinstance(value, int) or isinstance(value, bool)):
                self.error(f"{location}: {field_path} must be integer basis points")
            if key == "currency" and self.expected_currency is not None and value != self.expected_currency:
                self.error(
                    f"{location}: {field_path} must match configured currency {self.expected_currency}"
                )

    def load_jsonl(self) -> None:
        jsonl_dir = self.root / "jsonl"
        disputes_path = jsonl_dir / "disputes.jsonl"
        if disputes_path.is_file():
            try:
                for _, record in _jsonl(disputes_path):
                    transaction_id = record.get("transaction_id")
                    if isinstance(transaction_id, str):
                        self.unresolved_transaction_refs.add(transaction_id)
                        self.disputes_by_transaction[transaction_id].append(record)
            except (OSError, ValueError) as exc:
                self.error(str(exc))
        for collection in COLLECTIONS:
            path = jsonl_dir / f"{collection}.jsonl"
            if not path.is_file():
                self.error(f"missing canonical collection: jsonl/{collection}.jsonl")
                continue
            try:
                for line_number, record in _jsonl(path):
                    self.actual_counts[collection] += 1
                    self.payload_digests[collection] = _digest_add(
                        self.payload_digests[collection], _canonical(record)
                    )
                    self.validate_record(collection, line_number, record)
                    if collection == "customers":
                        self.customers.add(record.get("id"))
                    elif collection == "accounts":
                        self.accounts[record.get("id")] = record
                    elif collection == "merchants":
                        self.merchants.add(record.get("id"))
                    elif collection == "transactions":
                        self.unresolved_transaction_refs.discard(record.get("id"))
                        for dispute in self.disputes_by_transaction.get(record.get("id"), []):
                            if record.get("status") != "posted" or record.get("amount_minor", 0) >= 0:
                                self.error(f"disputes/{dispute.get('id')}: transaction must be a posted debit")
                            if dispute.get("customer_id") != record.get("customer_id"):
                                self.error(f"disputes/{dispute.get('id')}: customer does not own transaction")
                            if dispute.get("account_id") != record.get("account_id"):
                                self.error(f"disputes/{dispute.get('id')}: account does not match transaction")
                            if dispute.get("amount_minor") != -record.get("amount_minor", 0):
                                self.error(f"disputes/{dispute.get('id')}: amount does not match transaction")
                        if record.get("status") == "posted":
                            self.posted_delta_by_account[record.get("account_id")] += record.get("amount_minor", 0)
                            if record.get("amount_minor", 0) < 0:
                                key = (record.get("customer_id"), record.get("category"))
                                self.spend_by_customer_category_day[key][record.get("posted_date")] += -record.get(
                                    "amount_minor", 0
                                )
                        elif record.get("status") == "pending" and record.get("amount_minor", 0) < 0:
                            self.pending_debits_by_account[record.get("account_id")] += record.get("amount_minor", 0)
            except (OSError, ValueError) as exc:
                self.error(str(exc))
        expected_counts = self.manifest.get("counts", {})
        for collection in COLLECTIONS:
            if expected_counts.get(collection) != self.actual_counts[collection]:
                self.error(
                    f"count mismatch for {collection}: manifest={expected_counts.get(collection)} "
                    f"actual={self.actual_counts[collection]}"
                )
        for transaction_id in sorted(self.unresolved_transaction_refs):
            self.error(f"disputes: unknown transaction_id {transaction_id}")

    def validate_references_and_finance(self) -> None:
        jsonl_dir = self.root / "jsonl"
        customer_ref_collections = set(COLLECTIONS) - {"customers", "merchants"}
        account_ref_collections = {"cards", "transactions", "budgets", "alerts", "disputes", "delegations", "events", "investments", "incomes"}
        for collection in COLLECTIONS:
            for _, record in _jsonl(jsonl_dir / f"{collection}.jsonl"):
                customer_id = record.get("customer_id")
                if collection in customer_ref_collections and customer_id is not None and customer_id not in self.customers:
                    self.error(f"{collection}/{record.get('id')}: unknown customer_id {customer_id}")
                account_id = record.get("account_id")
                if collection in account_ref_collections and account_id is not None and account_id not in self.accounts:
                    self.error(f"{collection}/{record.get('id')}: unknown account_id {account_id}")
                if collection == "transactions":
                    merchant_id = record.get("merchant_id")
                    if merchant_id is not None and merchant_id not in self.merchants:
                        self.error(f"transactions/{record.get('id')}: unknown merchant_id {merchant_id}")
                    scenario = self.manifest.get("scenario_date")
                    if scenario and record.get("posted_date", "") > scenario:
                        self.error(f"transactions/{record.get('id')}: posted after scenario date")
                    try:
                        earliest = date.fromisoformat(scenario) - timedelta(
                            days=int(self.manifest["config"]["scale"]["history_days"])
                        )
                        if date.fromisoformat(record["posted_date"]) < earliest:
                            self.error(f"transactions/{record.get('id')}: posted before configured history window")
                    except (KeyError, TypeError, ValueError):
                        self.error(f"transactions/{record.get('id')}: cannot verify configured history window")
                elif collection == "cards":
                    limit_minor = record.get("credit_limit_minor", 0)
                    balance_minor = record.get("current_balance_minor", 0)
                    if record.get("available_credit_minor") != limit_minor - balance_minor:
                        self.error(f"cards/{record.get('id')}: available credit does not reconcile")
                    expected_bps = round(balance_minor / limit_minor * 10_000) if limit_minor else 0
                    if record.get("utilization_bps") != expected_bps:
                        self.error(f"cards/{record.get('id')}: utilization does not reconcile")
                elif collection == "goals":
                    if record.get("current_minor", 0) > record.get("target_minor", 0):
                        self.error(f"goals/{record.get('id')}: current amount exceeds target")
                elif collection == "loans":
                    try:
                        expected = _loan_payment(
                            record["principal_balance_minor"],
                            record["annual_rate_bps"],
                            record["remaining_months"],
                        )
                        if abs(record["scheduled_payment_minor"] - expected) > 1:
                            self.error(f"loans/{record.get('id')}: scheduled payment does not reconcile")
                    except (KeyError, TypeError, ZeroDivisionError):
                        self.error(f"loans/{record.get('id')}: incomplete loan fields")
                elif collection == "budgets":
                    try:
                        start = date.fromisoformat(record["period_start"])
                        end = date.fromisoformat(record["period_end"])
                        actual = sum(
                            amount
                            for posted_date, amount in self.spend_by_customer_category_day[
                                (record["customer_id"], record["category"])
                            ].items()
                            if start <= date.fromisoformat(posted_date) <= end
                        )
                        if record["actual_minor"] != actual:
                            self.error(f"budgets/{record.get('id')}: actual amount does not match transactions")
                    except (KeyError, TypeError, ValueError):
                        self.error(f"budgets/{record.get('id')}: incomplete budget fields")

        for account_id, account in self.accounts.items():
            posted_delta = self.posted_delta_by_account[account_id]
            if account["opening_balance_minor"] + posted_delta != account["posted_balance_minor"]:
                self.error(f"accounts/{account_id}: posted balance does not reconcile")
            pending_debits = self.pending_debits_by_account[account_id]
            if account["posted_balance_minor"] + pending_debits != account["available_balance_minor"]:
                self.error(f"accounts/{account_id}: available balance does not reconcile")

    def validate_exports(self) -> None:
        formats = set(self.manifest.get("config", {}).get("outputs", {}).get("formats", []))
        if "csv" in formats:
            for collection in COLLECTIONS:
                path = self.root / "csv" / f"{collection}.csv"
                if not path.is_file():
                    self.error(f"missing CSV export: {path.relative_to(self.root)}")
                    continue
                with path.open(encoding="utf-8", newline="") as handle:
                    count = 0
                    digest = 0
                    for row in csv.DictReader(handle):
                        count += 1
                        try:
                            digest = _digest_add(digest, _canonical(json.loads(row["payload_json"])))
                        except (KeyError, json.JSONDecodeError):
                            self.error(f"CSV payload is invalid for {collection}")
                if count != self.actual_counts[collection]:
                    self.error(f"CSV count mismatch for {collection}: {count}")
                if digest != self.payload_digests[collection]:
                    self.error(f"CSV payload mismatch for {collection}")
        if "mongo" in formats:
            for collection in COLLECTIONS:
                path = self.root / "mongo" / f"{collection}.jsonl"
                if not path.is_file():
                    self.error(f"missing Mongo import export: {path.relative_to(self.root)}")
                elif _hash(path) != _hash(self.root / "jsonl" / f"{collection}.jsonl"):
                    self.error(f"Mongo export differs from canonical JSONL for {collection}")
        if "sqlite" in formats:
            path = self.root / "horizon_synthetic.sqlite"
            if not path.is_file():
                self.error("missing SQLite export")
            else:
                try:
                    with sqlite3.connect(
                        f"file:{path.resolve().as_posix()}?mode=ro&immutable=1", uri=True
                    ) as connection:
                        for collection in COLLECTIONS:
                            count = connection.execute(f'SELECT COUNT(*) FROM "{collection}"').fetchone()[0]
                            if count != self.actual_counts[collection]:
                                self.error(f"SQLite count mismatch for {collection}: {count}")
                            digest = 0
                            for (payload,) in connection.execute(f'SELECT payload FROM "{collection}"'):
                                try:
                                    digest = _digest_add(digest, _canonical(json.loads(payload)))
                                except json.JSONDecodeError:
                                    self.error(f"SQLite payload is invalid for {collection}")
                            if digest != self.payload_digests[collection]:
                                self.error(f"SQLite payload mismatch for {collection}")
                except sqlite3.Error as exc:
                    self.error(f"SQLite export is invalid: {exc}")
        if "bundle-json" in formats:
            path = self.root / "bundle.json"
            if not path.is_file():
                self.error("missing JSON bundle")
            else:
                expected = hashlib.sha256()
                metadata = {
                    key: self.manifest[key]
                    for key in (
                        "schema_version",
                        "dataset_id",
                        "dataset_name",
                        "scenario_date",
                        "synthetic",
                        "institution",
                        "narrative",
                    )
                    if key in self.manifest
                }
                expected.update(b'{"metadata":')
                expected.update(_canonical(metadata).encode())
                for collection in COLLECTIONS:
                    expected.update(f',"{collection}":['.encode())
                    first = True
                    with (self.root / "jsonl" / f"{collection}.jsonl").open("rb") as handle:
                        for line in handle:
                            payload = line.strip()
                            if not payload:
                                continue
                            if not first:
                                expected.update(b",")
                            expected.update(payload)
                            first = False
                    expected.update(b"]")
                expected.update(b"}\n")
                if expected.hexdigest() != _hash(path):
                    self.error("bundle payload does not exactly match canonical JSONL")

    def validate_reproducibility(self) -> None:
        override_count = self.manifest.get("narrative", {}).get("override_count", 0)
        generator = (
            Path(__file__).resolve().parents[2]
            / "generate-horizon-bank-synthetic-data"
            / "scripts"
            / "generate_horizon_data.py"
        )
        if not generator.is_file():
            self.error(f"reproducibility generator is missing: {generator}")
            return
        config = json.loads(json.dumps(self.manifest.get("config", {})))
        if not config:
            self.error("reproducibility check requires manifest.config")
            return
        config.setdefault("outputs", {})["formats"] = ["jsonl"]
        dataset_config = config.setdefault("dataset", {})
        for generated_key in ("resolved_scenario_date", "synthetic", "institution"):
            dataset_config.pop(generated_key, None)
        with tempfile.TemporaryDirectory(prefix="horizon-repro-") as temp:
            temp_root = Path(temp)
            config_path = temp_root / "config.json"
            output_path = temp_root / "output"
            config_path.write_text(json.dumps(config, sort_keys=True), encoding="utf-8")
            command = [
                sys.executable,
                str(generator),
                "--config",
                str(config_path),
                "--out",
                str(output_path),
            ]
            if override_count:
                override_path = temp_root / "narrative-overrides.jsonl"
                overrides = []
                for _, customer in _jsonl(self.root / "jsonl" / "customers.jsonl"):
                    if isinstance(customer.get("profile_summary"), str):
                        overrides.append(
                            {
                                "entity_id": customer["id"],
                                "field": "profile_summary",
                                "text": customer["profile_summary"],
                            }
                        )
                if len(overrides) != override_count:
                    self.error(
                        "manifest narrative override count does not match enriched customer summaries"
                    )
                    return
                override_path.write_text(
                    "".join(_canonical(item) + "\n" for item in overrides),
                    encoding="utf-8",
                )
                command.extend(["--narrative-overrides", str(override_path)])
            completed = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
            )
            if completed.returncode != 0:
                self.error(f"reproducibility generation failed: {completed.stderr.strip()}")
                return
            for collection in COLLECTIONS:
                original = self.root / "jsonl" / f"{collection}.jsonl"
                regenerated = output_path / "jsonl" / f"{collection}.jsonl"
                if not regenerated.is_file() or _hash(original) != _hash(regenerated):
                    self.error(f"reproducibility mismatch for {collection}")

    def run(self, reproducibility_check: bool = False) -> dict[str, Any]:
        if not self.root.is_dir():
            self.error(f"dataset directory does not exist: {self.root}")
            return self.report()
        self.load_manifest()
        if self.manifest:
            self.validate_file_inventory()
        self.load_jsonl()
        if all((self.root / "jsonl" / f"{name}.jsonl").is_file() for name in COLLECTIONS):
            self.validate_references_and_finance()
        if self.manifest:
            self.validate_exports()
        if reproducibility_check and self.manifest and not self.errors:
            self.validate_reproducibility()
        return self.report()

    def report(self) -> dict[str, Any]:
        return {
            "valid": not self.errors,
            "dataset": str(self.root.resolve()),
            "errors": self.errors,
            "warnings": self.warnings,
            "counts": dict(sorted(self.actual_counts.items())),
        }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset", type=Path)
    parser.add_argument("--strict", action="store_true", help="Treat warnings as validation failures")
    parser.add_argument(
        "--reproducibility-check",
        action="store_true",
        help="Regenerate canonical JSONL from manifest.config and compare every collection",
    )
    parser.add_argument("--report", type=Path, help="Optional JSON report path")
    args = parser.parse_args()
    validation = Validation(args.dataset)
    try:
        report = validation.run(args.reproducibility_check)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        report = {
            "valid": False,
            "dataset": str(args.dataset.resolve()),
            "errors": [str(exc)],
            "warnings": [],
            "counts": {},
        }
    if args.strict and report["warnings"]:
        report["valid"] = False
    rendered = json.dumps(report, indent=2, sort_keys=True)
    print(rendered)
    if args.report:
        args.report.write_text(rendered + "\n", encoding="utf-8")
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
