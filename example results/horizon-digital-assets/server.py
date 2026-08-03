#!/usr/bin/env python3
"""Serve the Horizon digital-assets demo from its project-owned SQLite database."""

from __future__ import annotations

import argparse
import json
import mimetypes
import sqlite3
from datetime import date, datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse


def connect(db_path: Path) -> sqlite3.Connection:
    db = sqlite3.connect(db_path)
    db.row_factory = sqlite3.Row
    return db


def display_date(value: str) -> str:
    parsed = date.fromisoformat(value)
    return f"{parsed.strftime('%b')} {parsed.day}, {parsed.year}"


def build_dashboard(db_path: Path, requested_customer_id: str | None = None) -> dict:
    with connect(db_path) as db:
        customer_rows = db.execute("SELECT payload FROM customers ORDER BY id").fetchall()
        if not customer_rows:
            raise RuntimeError("The SQLite database does not contain a customer")
        customer = json.loads(customer_rows[0][0])
        if requested_customer_id:
            requested = next((json.loads(row[0]) for row in customer_rows if json.loads(row[0])["id"] == requested_customer_id), None)
            if requested:
                customer = requested
        customer_id = customer["id"]
        metadata = {row["key"]: json.loads(row["value"]) for row in db.execute("SELECT key, value FROM metadata")}
        asset_accounts = [dict(row) for row in db.execute("SELECT * FROM asset_accounts WHERE customer_id = ? ORDER BY custody_type", (customer_id,))]
        balances = {}
        asset_account_views = []
        for account in asset_accounts:
            balance = db.execute("SELECT COALESCE(SUM(amount_minor), 0) FROM asset_transactions WHERE asset_account_id = ? AND status = 'posted'", (account["id"],)).fetchone()[0]
            posted_count = db.execute("SELECT COUNT(*) FROM asset_transactions WHERE asset_account_id = ? AND status = 'posted'", (account["id"],)).fetchone()[0]
            pending_count = db.execute("SELECT COUNT(*) FROM asset_transactions WHERE asset_account_id = ? AND status = 'pending'", (account["id"],)).fetchone()[0]
            balances[account["custody_type"]] = balance
            asset_account_views.append({
                "id": account["id"],
                "label": account["display_label"],
                "custodyType": account["custody_type"],
                "assetSymbol": account["asset_symbol"],
                "network": account["network"],
                "address": account["address"],
                "balanceMinor": balance,
                "postedCount": posted_count,
                "pendingCount": pending_count,
                "status": account["status"],
            })
        activities = []
        for row in db.execute("SELECT event_date, description, activity_type, status, amount_minor, id FROM asset_transactions WHERE customer_id = ? ORDER BY event_date DESC, id DESC LIMIT 100", (customer_id,)):
            activities.append({
                "id": row["id"],
                "date": display_date(row["event_date"]),
                "description": row["description"],
                "type": row["activity_type"],
                "status": row["status"].title(),
                "amountMinor": row["amount_minor"],
                "tone": row["status"],
            })
        wallet = next(account for account in asset_accounts if account["custody_type"] == "wallet")
        canonical_accounts = []
        for row in db.execute("SELECT payload FROM accounts WHERE customer_id = ? ORDER BY id", (customer_id,)):
            account = json.loads(row[0])
            canonical_accounts.append({
                "id": account["id"],
                "productName": account["product_name"],
                "type": account["type"],
                "displayLast4": account["display_last4"],
                "postedBalanceMinor": account["posted_balance_minor"],
                "availableBalanceMinor": account["available_balance_minor"],
                "status": account["status"],
            })
        alerts = [json.loads(row[0]) for row in db.execute("SELECT payload FROM alerts WHERE customer_id = ? ORDER BY event_date DESC", (customer_id,))]
        delegations = [json.loads(row[0]) for row in db.execute("SELECT payload FROM delegations WHERE customer_id = ? ORDER BY id", (customer_id,))]
        recent_actions = [dict(row) for row in db.execute("SELECT action_type, detail, status, created_at FROM app_actions WHERE customer_id = ? ORDER BY created_at DESC LIMIT 5", (customer_id,))]
        posted_activity = sum(1 for activity in activities if activity["status"] == "Posted")
        pending_activity = sum(1 for activity in activities if activity["status"] == "Pending")
        custody_account = next(account for account in asset_account_views if account["custodyType"] == "custody")
        pending_amount = db.execute("SELECT COALESCE(SUM(amount_minor), 0) FROM asset_transactions WHERE asset_account_id = ? AND status = 'pending'", (custody_account["id"],)).fetchone()[0]
        return {
            "synthetic": True,
            "scenarioDate": metadata.get("scenario_date"),
            "customer": {"id": customer_id, "name": customer["name"]["display"], "archetype": customer["archetype"]},
            "balances": {
                "totalDigitalAssetValueMinor": balances.get("custody", 0) + balances.get("wallet", 0),
                "custodyBalanceMinor": balances.get("custody", 0),
                "walletBalanceMinor": balances.get("wallet", 0),
            },
            "asset": {"symbol": "USDC", "network": wallet["network"]},
            "wallet": {"address": wallet["address"], "network": wallet["network"]},
            "activities": activities,
            "activitySummary": {"total": len(activities), "posted": posted_activity, "pending": pending_activity},
            "custody": {"accounts": asset_account_views, "fundingAccounts": canonical_accounts, "alerts": alerts},
            "stablecoins": {"symbol": "USDC", "network": wallet["network"], "custodyBalanceMinor": custody_account["balanceMinor"], "pendingBalanceMinor": pending_amount, "postedActivityCount": posted_activity, "pendingActivityCount": pending_activity},
            "walletDetails": {"balanceMinor": balances.get("wallet", 0), "address": wallet["address"], "network": wallet["network"], "activity": [activity for activity in activities if activity["type"] == "Wallet transfer"], "delegations": delegations, "recentActions": recent_actions},
        }


class AppHandler(BaseHTTPRequestHandler):
    db_path: Path
    static_dir: Path

    def send_json(self, status: int, value: dict) -> None:
        body = json.dumps(value, separators=(",", ":")).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Synthetic-Data", "true")
        self.end_headers()
        self.wfile.write(body)

    def serve_static(self, request_path: str) -> None:
        """Serve the production React bundle, with an SPA fallback for app routes."""
        root = self.static_dir.resolve()
        relative_path = request_path.lstrip("/") or "index.html"
        candidate = (root / relative_path).resolve()
        if root not in candidate.parents and candidate != root:
            self.send_error(403)
            return
        if not candidate.is_file():
            candidate = root / "index.html"
        try:
            body = candidate.read_bytes()
        except OSError:
            self.send_error(404)
            return
        content_type = mimetypes.guess_type(candidate.name)[0] or "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8" if content_type.startswith("text/") or content_type in {"application/javascript", "application/json"} else content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"
        query = parse_qs(parsed.query)
        if path == "/api/health":
            self.send_json(200, {"ok": True, "synthetic": True, "database": str(self.db_path)})
            return
        if path in {"/api/dashboard", "/api/activity", "/api/custody", "/api/stablecoins", "/api/wallet"}:
            dashboard = build_dashboard(self.db_path, query.get("customer_id", [None])[0])
            if path == "/api/activity":
                self.send_json(200, {"synthetic": True, "activities": dashboard["activities"]})
            elif path == "/api/custody":
                self.send_json(200, {"synthetic": True, "custody": dashboard["custody"]})
            elif path == "/api/stablecoins":
                self.send_json(200, {"synthetic": True, "stablecoins": dashboard["stablecoins"]})
            elif path == "/api/wallet":
                self.send_json(200, {"synthetic": True, "wallet": dashboard["walletDetails"]})
            else:
                self.send_json(200, dashboard)
            return
        self.serve_static(parsed.path)

    def do_POST(self) -> None:
        path = urlparse(self.path).path.rstrip("/") or "/"
        if path == "/api/actions":
            try:
                length = int(self.headers.get("Content-Length", "0"))
                payload = json.loads(self.rfile.read(length) or b"{}")
                action_type = payload.get("actionType")
                detail = payload.get("detail")
                allowed_actions = {"wallet_receive", "wallet_send", "funding_review"}
                if action_type not in allowed_actions or not detail:
                    raise ValueError("actionType and detail are required")
                with connect(self.db_path) as db:
                    customer_id = db.execute("SELECT id FROM customers ORDER BY id LIMIT 1").fetchone()[0]
                    action_id = f"action_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}"
                    db.execute("INSERT INTO app_actions VALUES (?, ?, ?, ?, ?, 'recorded', 1)", (action_id, customer_id, datetime.now(timezone.utc).isoformat(), action_type, detail))
                    db.commit()
                self.send_json(201, {"synthetic": True, "actionId": action_id, "dashboard": build_dashboard(self.db_path)})
            except (ValueError, TypeError, sqlite3.Error, KeyError) as error:
                self.send_json(400, {"error": str(error)})
            return
        if path != "/api/orders":
            self.send_json(404, {"error": "not_found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length) or b"{}")
            direction = payload.get("direction")
            amount_minor = int(payload.get("amountMinor", 0))
            if direction not in {"buy", "sell"} or amount_minor <= 0:
                raise ValueError("direction and a positive amountMinor are required")
            with connect(self.db_path) as db:
                customer_id = db.execute("SELECT id FROM customers ORDER BY id LIMIT 1").fetchone()[0]
                account_id = db.execute("SELECT id FROM asset_accounts WHERE customer_id = ? AND custody_type = 'custody'", (customer_id,)).fetchone()[0]
                created_at = datetime.now(timezone.utc).isoformat()
                order_id = f"order_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}"
                asset_amount_minor = amount_minor if direction == "buy" else round(amount_minor / 0.999)
                signed_asset_amount = asset_amount_minor if direction == "buy" else -asset_amount_minor
                db.execute("INSERT INTO app_orders VALUES (?, ?, ?, ?, ?, ?, ?, 'pending', 1)", (order_id, account_id, customer_id, created_at, direction, amount_minor, asset_amount_minor))
                db.execute("INSERT INTO asset_transactions VALUES (?, ?, ?, date('now'), ?, ?, 'pending', ?, ?, 'USDC', 'user-confirmed simulated order', 1)", (order_id, account_id, customer_id, f"USDC {direction}", "Stablecoin purchase" if direction == "buy" else "Stablecoin sale", signed_asset_amount, amount_minor))
                db.commit()
            dashboard = build_dashboard(self.db_path)
            self.send_json(201, {"synthetic": True, "orderId": order_id, "dashboard": dashboard})
        except (ValueError, TypeError, sqlite3.Error, KeyError) as error:
            self.send_json(400, {"error": str(error)})

    def log_message(self, format: str, *args: object) -> None:
        print(f"{self.client_address[0]} - {format % args}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=Path("data/horizon_app.sqlite"))
    parser.add_argument("--static-dir", type=Path, default=Path("dist"))
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=5180)
    args = parser.parse_args()
    if not args.db.is_file():
        raise SystemExit(f"SQLite database not found: {args.db}")
    if not args.static_dir.is_dir():
        raise SystemExit(f"Production bundle not found: {args.static_dir}")
    handler = type("BoundAppHandler", (AppHandler,), {"db_path": args.db.resolve(), "static_dir": args.static_dir.resolve()})
    server = ThreadingHTTPServer((args.host, args.port), handler)
    print(f"Serving Horizon digital-assets app API at http://{args.host}:{server.server_port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
