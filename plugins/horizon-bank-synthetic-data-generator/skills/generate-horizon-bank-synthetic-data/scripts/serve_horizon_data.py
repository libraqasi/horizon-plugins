#!/usr/bin/env python3
"""Serve a generated Horizon Bank SQLite fixture through a read-only local API."""

from __future__ import annotations

import argparse
import json
import sqlite3
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, unquote, urlparse


def _connect(db_path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(f"file:{db_path.resolve().as_posix()}?mode=ro&immutable=1", uri=True)
    connection.row_factory = sqlite3.Row
    return connection


def _payloads(connection: sqlite3.Connection, table: str, where: str = "", values: tuple[Any, ...] = (), limit: int = 100, offset: int = 0) -> list[dict[str, Any]]:
    query = f'SELECT payload FROM "{table}"'
    if where:
        query += f" WHERE {where}"
    query += " ORDER BY id LIMIT ? OFFSET ?"
    rows = connection.execute(query, (*values, limit, offset)).fetchall()
    return [json.loads(row["payload"]) for row in rows]


def _one(connection: sqlite3.Connection, table: str, record_id: str) -> dict[str, Any] | None:
    row = connection.execute(f'SELECT payload FROM "{table}" WHERE id = ?', (record_id,)).fetchone()
    return json.loads(row["payload"]) if row else None


def _integer(query: dict[str, list[str]], name: str, default: int, maximum: int) -> int:
    try:
        return max(0, min(maximum, int(query.get(name, [str(default)])[0])))
    except ValueError:
        return default


def make_handler(db_path: Path) -> type[BaseHTTPRequestHandler]:
    class FixtureHandler(BaseHTTPRequestHandler):
        server_version = "HorizonSyntheticFixture/1.0"

        def _send(self, status: int, value: Any, head_only: bool = False) -> None:
            body = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Synthetic-Data", "true")
            self.end_headers()
            if not head_only:
                self.wfile.write(body)

        def _route(self, head_only: bool = False) -> None:
            parsed = urlparse(self.path)
            path = parsed.path.rstrip("/") or "/"
            query = parse_qs(parsed.query)
            limit = _integer(query, "limit", 100, 500)
            offset = _integer(query, "offset", 0, 1_000_000)
            segments = [unquote(item) for item in path.split("/") if item]
            try:
                with _connect(db_path) as connection:
                    if path == "/health":
                        self._send(200, {"ok": True, "synthetic": True}, head_only)
                        return
                    if path == "/v1/metadata":
                        rows = connection.execute("SELECT key, value FROM metadata ORDER BY key").fetchall()
                        self._send(200, {row["key"]: json.loads(row["value"]) for row in rows}, head_only)
                        return
                    if path == "/v1/customers":
                        data = _payloads(connection, "customers", limit=limit, offset=offset)
                        self._send(200, {"data": data, "limit": limit, "offset": offset}, head_only)
                        return
                    if len(segments) == 3 and segments[:2] == ["v1", "customers"]:
                        customer = _one(connection, "customers", segments[2])
                        self._send(200 if customer else 404, customer or {"error": "customer_not_found"}, head_only)
                        return
                    if len(segments) == 4 and segments[:2] == ["v1", "customers"] and segments[3] == "accounts":
                        customer = _one(connection, "customers", segments[2])
                        if not customer:
                            self._send(404, {"error": "customer_not_found"}, head_only)
                            return
                        data = _payloads(connection, "accounts", "customer_id = ?", (segments[2],), limit, offset)
                        self._send(200, {"data": data, "limit": limit, "offset": offset}, head_only)
                        return
                    if len(segments) == 4 and segments[:2] == ["v1", "customers"] and segments[3] == "disputes":
                        customer = _one(connection, "customers", segments[2])
                        if not customer:
                            self._send(404, {"error": "customer_not_found"}, head_only)
                            return
                        data = _payloads(connection, "disputes", "customer_id = ?", (segments[2],), limit, offset)
                        self._send(200, {"data": data, "limit": limit, "offset": offset}, head_only)
                        return
                    if len(segments) == 4 and segments[:2] == ["v1", "accounts"] and segments[3] == "transactions":
                        account = _one(connection, "accounts", segments[2])
                        if not account:
                            self._send(404, {"error": "account_not_found"}, head_only)
                            return
                        data = _payloads(connection, "transactions", "account_id = ?", (segments[2],), limit, offset)
                        self._send(200, {"data": data, "limit": limit, "offset": offset}, head_only)
                        return
                    if len(segments) == 4 and segments[:2] == ["v1", "customers"] and segments[3] == "snapshot":
                        customer = _one(connection, "customers", segments[2])
                        if not customer:
                            self._send(404, {"error": "customer_not_found"}, head_only)
                            return
                        customer_id = segments[2]
                        snapshot = {
                            "customer": customer,
                            "accounts": _payloads(connection, "accounts", "customer_id = ?", (customer_id,), 25, 0),
                            "cards": _payloads(connection, "cards", "customer_id = ?", (customer_id,), 25, 0),
                            "goals": _payloads(connection, "goals", "customer_id = ?", (customer_id,), 25, 0),
                            "alerts": _payloads(connection, "alerts", "customer_id = ?", (customer_id,), 25, 0),
                            "disputes": _payloads(connection, "disputes", "customer_id = ?", (customer_id,), 25, 0),
                            "events": _payloads(connection, "events", "customer_id = ?", (customer_id,), 25, 0),
                            "synthetic": True,
                        }
                        self._send(200, snapshot, head_only)
                        return
                    if path == "/v1/events":
                        customer_id = query.get("customer_id", [None])[0]
                        if customer_id:
                            data = _payloads(connection, "events", "customer_id = ?", (customer_id,), limit, offset)
                        else:
                            data = _payloads(connection, "events", limit=limit, offset=offset)
                        self._send(200, {"data": data, "limit": limit, "offset": offset}, head_only)
                        return
                    self._send(404, {"error": "not_found"}, head_only)
            except sqlite3.Error as exc:
                self._send(500, {"error": "fixture_database_error", "detail": str(exc)}, head_only)

        def do_GET(self) -> None:
            self._route(False)

        def do_HEAD(self) -> None:
            self._route(True)

        def _read_only(self) -> None:
            self._send(405, {"error": "read_only_fixture"})

        do_POST = _read_only
        do_PUT = _read_only
        do_PATCH = _read_only
        do_DELETE = _read_only

        def log_message(self, format: str, *args: Any) -> None:
            print(f"{self.client_address[0]} - {format % args}")

    return FixtureHandler


def create_server(db_path: Path, host: str = "127.0.0.1", port: int = 8787) -> ThreadingHTTPServer:
    if not db_path.is_file():
        raise FileNotFoundError(db_path)
    return ThreadingHTTPServer((host, port), make_handler(db_path))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, required=True, help="Generated horizon_synthetic.sqlite")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8787)
    args = parser.parse_args()
    if args.host not in {"127.0.0.1", "localhost", "::1"}:
        parser.error("The fixture server binds only to a local interface")
    try:
        server = create_server(args.db, args.host, args.port)
    except (OSError, sqlite3.Error) as exc:
        parser.error(str(exc))
    print(f"Serving synthetic fixtures at http://{args.host}:{server.server_port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
