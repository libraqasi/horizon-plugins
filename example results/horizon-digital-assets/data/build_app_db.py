#!/usr/bin/env python3
"""Create the project-owned mutable SQLite adapter from a Horizon fixture."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sqlite3
from datetime import date, timedelta
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path("data/generated/horizon_synthetic.sqlite"))
    parser.add_argument("--out", type=Path, default=Path("data/horizon_app.sqlite"))
    return parser.parse_args()


def money(value: int) -> int:
    return max(0, int(value))


def safe_wallet_address(customer_id: str) -> str:
    return "0x" + hashlib.sha256(("horizon-wallet:" + customer_id).encode()).hexdigest()[:40]


def create_adapter(source: Path, target: Path) -> None:
    if not source.is_file():
        raise FileNotFoundError(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        target.unlink()
    shutil.copy2(source, target)

    with sqlite3.connect(target) as db:
        db.row_factory = sqlite3.Row
        customer_rows = db.execute("SELECT payload FROM customers ORDER BY id").fetchall()
        if not customer_rows:
            raise RuntimeError("The generated fixture does not contain a customer")
        scenario_date = date.fromisoformat(json.loads(db.execute("SELECT value FROM metadata WHERE key = 'scenario_date'").fetchone()[0]))

        db.executescript(
            """
            CREATE TABLE asset_accounts (
              id TEXT PRIMARY KEY,
              customer_id TEXT NOT NULL,
              asset_symbol TEXT NOT NULL,
              network TEXT NOT NULL,
              custody_type TEXT NOT NULL,
              address TEXT NOT NULL,
              display_label TEXT NOT NULL,
              status TEXT NOT NULL,
              source_account_id TEXT NOT NULL,
              synthetic INTEGER NOT NULL DEFAULT 1
            );
            CREATE TABLE asset_transactions (
              id TEXT PRIMARY KEY,
              asset_account_id TEXT NOT NULL,
              customer_id TEXT NOT NULL,
              event_date TEXT NOT NULL,
              description TEXT NOT NULL,
              activity_type TEXT NOT NULL,
              status TEXT NOT NULL,
              amount_minor INTEGER NOT NULL,
              fiat_amount_minor INTEGER,
              asset_symbol TEXT NOT NULL,
              source_rule TEXT NOT NULL,
              synthetic INTEGER NOT NULL DEFAULT 1
            );
            CREATE TABLE app_orders (
              id TEXT PRIMARY KEY,
              asset_account_id TEXT NOT NULL,
              customer_id TEXT NOT NULL,
              created_at TEXT NOT NULL,
              direction TEXT NOT NULL,
              fiat_amount_minor INTEGER NOT NULL,
              asset_amount_minor INTEGER NOT NULL,
              status TEXT NOT NULL,
              synthetic INTEGER NOT NULL DEFAULT 1
            );
            CREATE TABLE app_actions (
              id TEXT PRIMARY KEY,
              customer_id TEXT NOT NULL,
              created_at TEXT NOT NULL,
              action_type TEXT NOT NULL,
              detail TEXT NOT NULL,
              status TEXT NOT NULL,
              synthetic INTEGER NOT NULL DEFAULT 1
            );
            CREATE INDEX asset_accounts_customer_idx ON asset_accounts(customer_id);
            CREATE INDEX asset_transactions_account_date_idx ON asset_transactions(asset_account_id, event_date DESC);
            CREATE INDEX asset_transactions_customer_date_idx ON asset_transactions(customer_id, event_date DESC);
            CREATE INDEX app_actions_customer_date_idx ON app_actions(customer_id, created_at DESC);
            """
        )

        # The digital-asset extension is deterministic and explicitly synthetic. Its
        # seed amounts are proportions of the generated reserve account, while all
        # balances displayed by the app are recomputed from these ledger rows.
        account_rows = []
        asset_rows = []
        for customer_row in customer_rows:
            customer_record = json.loads(customer_row["payload"])
            customer_id = customer_record["id"]
            accounts = [
                json.loads(row["payload"])
                for row in db.execute("SELECT payload FROM accounts WHERE customer_id = ? ORDER BY id", (customer_id,)).fetchall()
            ]
            if not accounts:
                continue
            reserve = next((account for account in accounts if account["type"] == "savings"), accounts[0])
            reserve_minor = money(reserve["posted_balance_minor"])
            custody_id = f"asset_custody_{customer_id[5:]}"
            wallet_id = f"asset_wallet_{customer_id[5:]}"
            address = safe_wallet_address(customer_id)
            account_rows.extend([
                (custody_id, customer_id, "custody", address, "Horizon custody", reserve["id"]),
                (wallet_id, customer_id, "wallet", address, "Digital wallet", reserve["id"]),
            ])
            ratios = [
                ("01", custody_id, 30, "USDC receive", "Wallet transfer", "posted", 0.14, None, "reserve_balance * 0.14"),
                ("02", custody_id, 75, "USDC buy", "Stablecoin purchase", "posted", 0.22, 0.22, "reserve_balance * 0.22"),
                ("03", custody_id, 120, "USDC receive", "Wallet transfer", "posted", 0.18, None, "reserve_balance * 0.18"),
                ("04", custody_id, 165, "USDC send", "Wallet transfer", "posted", -0.06, None, "-(reserve_balance * 0.06)"),
                ("05", custody_id, 210, "USDC buy", "Stablecoin purchase", "posted", 0.17, 0.17, "reserve_balance * 0.17"),
                ("06", custody_id, 255, "USDC send", "Wallet transfer", "posted", -0.04, None, "-(reserve_balance * 0.04)"),
                ("07", custody_id, 300, "USDC buy", "Stablecoin purchase", "posted", 0.12, 0.12, "reserve_balance * 0.12"),
                ("08", custody_id, 0, "USDC buy", "Stablecoin purchase", "pending", 0.08, 0.08, "reserve_balance * 0.08"),
                ("09", wallet_id, 45, "USDC receive", "Wallet transfer", "posted", 0.05, None, "reserve_balance * 0.05"),
                ("10", wallet_id, 95, "USDC send", "Wallet transfer", "posted", -0.015, None, "-(reserve_balance * 0.015)"),
                ("11", wallet_id, 180, "USDC receive", "Wallet transfer", "posted", 0.035, None, "reserve_balance * 0.035"),
                ("12", wallet_id, 275, "USDC send", "Wallet transfer", "posted", -0.01, None, "-(reserve_balance * 0.01)"),
            ]
            for suffix, asset_account_id, days_ago, description, activity_type, status, ratio, fiat_ratio, rule in ratios:
                amount = int(reserve_minor * ratio)
                fiat_amount = int(reserve_minor * fiat_ratio) if fiat_ratio is not None else None
                asset_rows.append((f"asset_tx_{customer_id[5:]}_{suffix}", asset_account_id, customer_id, (scenario_date - timedelta(days=days_ago)).isoformat(), description, activity_type, status, amount, fiat_amount, rule))

        db.executemany(
            "INSERT INTO asset_accounts VALUES (?, ?, 'USDC', 'Ethereum (ERC-20)', ?, ?, ?, 'active', ?, 1)",
            account_rows,
        )
        db.executemany(
            "INSERT INTO asset_transactions (id, asset_account_id, customer_id, event_date, description, activity_type, status, amount_minor, fiat_amount_minor, asset_symbol, source_rule, synthetic) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'USDC', ?, 1)",
            asset_rows,
        )
        db.execute(
            "INSERT OR REPLACE INTO metadata (key, value) VALUES ('app_extension', ?)",
            (json.dumps({"name": "horizon-digital-assets-ui", "synthetic": True, "customer_count": len(account_rows) // 2, "asset_account_count": len(account_rows), "asset_transaction_count": len(asset_rows), "derivation": "USDC ledger rows use deterministic proportions of each generated reserve account; balances are computed from posted ledger rows."}),),
        )
        db.commit()


if __name__ == "__main__":
    args = parse_args()
    create_adapter(args.source, args.out)
    print(f"Created mutable Horizon app database at {args.out.resolve()}")
