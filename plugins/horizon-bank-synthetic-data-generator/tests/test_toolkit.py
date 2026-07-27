from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

PLUGIN = Path(__file__).resolve().parents[1]
GENERATE_SKILL = PLUGIN / "skills" / "generate-horizon-bank-synthetic-data"
VALIDATE_SKILL = PLUGIN / "skills" / "validate-horizon-bank-synthetic-data"
GENERATOR = GENERATE_SKILL / "scripts" / "generate_horizon_data.py"
CONFIG_VALIDATOR = GENERATE_SKILL / "scripts" / "validate_horizon_config.py"
VALIDATOR = VALIDATE_SKILL / "scripts" / "validate_horizon_data.py"
SERVER_SCRIPTS = GENERATE_SKILL / "scripts"
CONFIG = GENERATE_SKILL / "assets" / "configs" / "all-archetypes-small.json"

sys.path.insert(0, str(SERVER_SCRIPTS))
from serve_horizon_data import create_server  # noqa: E402


def run_generator(out: Path, *extra: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(GENERATOR), "--config", str(CONFIG), "--out", str(out), *extra],
        check=True,
        capture_output=True,
        text=True,
    )


def hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class ToolkitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temp = tempfile.TemporaryDirectory(prefix="horizon-toolkit-tests-")
        cls.root = Path(cls.temp.name)
        cls.dataset = cls.root / "full"
        run_generator(cls.dataset)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp.cleanup()

    def test_all_archetypes_are_represented(self) -> None:
        customers = [
            json.loads(line)
            for line in (self.dataset / "jsonl" / "customers.jsonl").read_text(encoding="utf-8").splitlines()
        ]
        self.assertEqual(
            {customer["archetype"] for customer in customers},
            {
                "youth-guardian",
                "emerging-adult",
                "everyday-banking",
                "family-homebuyer",
                "affluent-investor",
                "small-business-owner",
                "gig-multi-income",
                "retiree-fixed-income",
                "agentic-digital-wallet",
            },
        )
        self.assertTrue(all(customer["synthetic"] for customer in customers))
        self.assertTrue(all(customer["contact"]["email"].endswith(".example") for customer in customers))
        self.assertTrue(all("555" in customer["contact"]["phone"] for customer in customers))

    def test_named_overlays_create_locatable_financial_states(self) -> None:
        def records(name: str) -> list[dict]:
            path = self.dataset / "jsonl" / f"{name}.jsonl"
            return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]

        customers = records("customers")
        accounts = records("accounts")
        transactions = records("transactions")
        alerts = records("alerts")
        events = records("events")
        expected = {
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
        self.assertEqual({event["type"] for event in events}, expected)
        by_overlay = {
            overlay: customer
            for customer in customers
            for overlay in customer["active_overlays"]
        }
        low_account = next(account for account in accounts if account["customer_id"] == by_overlay["low-balance"]["id"])
        self.assertEqual(low_account["posted_balance_minor"], 4_500)
        overdraft_account = next(
            account for account in accounts if account["customer_id"] == by_overlay["overdraft-risk"]["id"]
        )
        self.assertLess(overdraft_account["available_balance_minor"], 0)
        pending_customer = by_overlay["pending-card-charge"]["id"]
        self.assertTrue(
            any(transaction["customer_id"] == pending_customer and transaction["status"] == "pending" for transaction in transactions)
        )
        fraud_customer = by_overlay["fraud-review"]["id"]
        self.assertTrue(any(alert["customer_id"] == fraud_customer and alert["type"] == "fraud_review" for alert in alerts))

    def test_same_seed_is_byte_deterministic_and_new_seed_changes_ids(self) -> None:
        first = self.root / "deterministic-one"
        second = self.root / "deterministic-two"
        third = self.root / "different-seed"
        run_generator(first, "--formats", "jsonl")
        run_generator(second, "--formats", "jsonl")
        run_generator(third, "--formats", "jsonl", "--seed", "987654")
        for path in sorted((first / "jsonl").glob("*.jsonl")):
            counterpart = second / "jsonl" / path.name
            self.assertEqual(hash_file(path), hash_file(counterpart), path.name)
        first_customer = json.loads((first / "jsonl" / "customers.jsonl").read_text().splitlines()[0])
        third_customer = json.loads((third / "jsonl" / "customers.jsonl").read_text().splitlines()[0])
        self.assertNotEqual(first_customer["id"], third_customer["id"])

    def test_strict_validator_accepts_every_export(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(VALIDATOR),
                str(self.dataset),
                "--strict",
                "--reproducibility-check",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertTrue(report["valid"])
        self.assertEqual(report["errors"], [])

    def test_narrative_slots_accept_only_a_grounded_summary_override(self) -> None:
        raw = json.loads(CONFIG.read_text(encoding="utf-8"))
        raw["narrative"]["mode"] = "slots"
        raw["scale"] = {"preset": "custom", "customers": 1, "history_days": 30}
        slot_config = self.root / "slots-config.json"
        slot_config.write_text(json.dumps(raw), encoding="utf-8")
        slot_output = self.root / "slots"
        subprocess.run(
            [sys.executable, str(GENERATOR), "--config", str(slot_config), "--out", str(slot_output)],
            check=True,
            capture_output=True,
            text=True,
        )
        slot = json.loads((slot_output / "narrative-slots.jsonl").read_text().splitlines()[0])
        override = self.root / "narrative-overrides.jsonl"
        expected = "A concise, fact-grounded synthetic customer summary."
        override.write_text(
            json.dumps({"entity_id": slot["entity_id"], "field": "profile_summary", "text": expected}) + "\n",
            encoding="utf-8",
        )
        enriched = self.root / "enriched"
        subprocess.run(
            [
                sys.executable,
                str(GENERATOR),
                "--config",
                str(slot_config),
                "--out",
                str(enriched),
                "--narrative-overrides",
                str(override),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        customer = json.loads((enriched / "jsonl" / "customers.jsonl").read_text().splitlines()[0])
        self.assertEqual(customer["profile_summary"], expected)
        validation = subprocess.run(
            [
                sys.executable,
                str(VALIDATOR),
                str(enriched),
                "--strict",
                "--reproducibility-check",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(validation.returncode, 0, validation.stdout + validation.stderr)

    def test_every_archetype_preset_generates_and_validates(self) -> None:
        config_dir = GENERATE_SKILL / "assets" / "configs"
        for config in sorted(config_dir.glob("*.json")):
            with self.subTest(config=config.name):
                output = self.root / f"preset-{config.stem}"
                subprocess.run(
                    [
                        sys.executable,
                        str(GENERATOR),
                        "--config",
                        str(config),
                        "--out",
                        str(output),
                        "--formats",
                        "jsonl",
                    ],
                    check=True,
                    capture_output=True,
                    text=True,
                )
                validation = subprocess.run(
                    [sys.executable, str(VALIDATOR), str(output), "--strict"],
                    check=False,
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(validation.returncode, 0, validation.stdout + validation.stderr)

    def test_config_contract_is_enforced_without_generation(self) -> None:
        valid = subprocess.run(
            [sys.executable, str(CONFIG_VALIDATOR), str(CONFIG)],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(valid.returncode, 0, valid.stdout + valid.stderr)
        raw = json.loads(CONFIG.read_text(encoding="utf-8"))
        del raw["dataset"]["timezone"]
        invalid_config = self.root / "missing-timezone.json"
        invalid_config.write_text(json.dumps(raw), encoding="utf-8")
        invalid = subprocess.run(
            [sys.executable, str(CONFIG_VALIDATOR), str(invalid_config)],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(invalid.returncode, 0)
        self.assertIn("timezone", invalid.stderr)

    def test_scale_override_resolves_the_named_preset(self) -> None:
        output = self.root / "scale-override"
        run_generator(output, "--size", "medium", "--customers", "2", "--formats", "jsonl")
        manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["config"]["scale"]["customers"], 2)
        self.assertEqual(manifest["config"]["scale"]["history_days"], 365)
        self.assertEqual(manifest["config"]["scale"]["min_transactions"], 150)
        self.assertEqual(manifest["config"]["scale"]["max_transactions"], 350)

    def test_validator_detects_financial_mutation(self) -> None:
        mutated = self.root / "mutated"
        shutil.copytree(self.dataset, mutated)
        accounts_path = mutated / "jsonl" / "accounts.jsonl"
        lines = accounts_path.read_text(encoding="utf-8").splitlines()
        account = json.loads(lines[0])
        account["opening_balance_minor"] += 1
        lines[0] = json.dumps(account, sort_keys=True, separators=(",", ":"))
        accounts_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(VALIDATOR), str(mutated), "--strict"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        report = json.loads(result.stdout)
        self.assertTrue(any("hash mismatch" in error for error in report["errors"]))
        self.assertTrue(any("posted balance does not reconcile" in error for error in report["errors"]))

    def test_read_only_rest_fixture(self) -> None:
        sidecars = [
            self.dataset / "horizon_synthetic.sqlite-wal",
            self.dataset / "horizon_synthetic.sqlite-shm",
        ]
        self.assertTrue(all(not path.exists() for path in sidecars))
        server = create_server(self.dataset / "horizon_synthetic.sqlite", port=0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base = f"http://127.0.0.1:{server.server_port}"
        try:
            with urlopen(f"{base}/health", timeout=5) as response:
                self.assertEqual(response.status, 200)
                self.assertEqual(response.headers["X-Synthetic-Data"], "true")
                self.assertTrue(json.loads(response.read())["synthetic"])
            with urlopen(f"{base}/v1/customers?limit=1", timeout=5) as response:
                customer = json.loads(response.read())["data"][0]
            with urlopen(f"{base}/v1/customers/{customer['id']}/snapshot", timeout=5) as response:
                snapshot = json.loads(response.read())
                self.assertEqual(snapshot["customer"]["id"], customer["id"])
                self.assertGreater(len(snapshot["accounts"]), 0)
                self.assertIn("disputes", snapshot)
            with urlopen(f"{base}/v1/customers?limit=9", timeout=5) as response:
                customers = json.loads(response.read())["data"]
            disputed_customer = next(
                item for item in customers if "card-dispute" in item["active_overlays"]
            )
            with urlopen(f"{base}/v1/customers/{disputed_customer['id']}/disputes", timeout=5) as response:
                self.assertEqual(len(json.loads(response.read())["data"]), 1)
            with self.assertRaises(HTTPError) as raised:
                urlopen(Request(f"{base}/v1/customers", data=b"{}", method="POST"), timeout=5)
            self.assertEqual(raised.exception.code, 405)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)
        self.assertTrue(all(not path.exists() for path in sidecars))


if __name__ == "__main__":
    unittest.main()
