"""Local SQLite-backed server for the Horizon NFT Vault prototype."""
import hashlib
import json
import secrets
import sqlite3
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).parent
OUTPUTS = ROOT / "outputs"
DB = ROOT / "nft_vault.sqlite3"
VAULT_ID = "vault-maya-001"
CATALOG = [
    {"kind": "Fox", "image": "collectibles/fox.svg", "icon": "✦", "art": "fox-art"},
    {"kind": "Golem", "image": "collectibles/robot-golem.svg", "icon": "◈", "art": "robot-art"},
    {"kind": "Oracle", "image": "collectibles/crystal-ball.svg", "icon": "●", "art": "oracle-art"},
]
PREFIXES = {
    "sky": ["Moonbeam", "Cloud", "Starling", "Aurora"],
    "garden": ["Pebble", "Fern", "Willow", "Pollen"],
    "robot": ["Circuit", "Orbit", "Comet", "Beacon"],
}
RARITIES = [("Common", 1000), ("Uncommon", 1800), ("Rare", 2800)]


def connection():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con


def has_column(con, table, column):
    return any(row["name"] == column for row in con.execute(f"PRAGMA table_info({table})"))


def setup_database():
    con = connection()
    con.executescript("""
    CREATE TABLE IF NOT EXISTS vaults (
      id TEXT PRIMARY KEY, child_name TEXT NOT NULL, guardian_status TEXT NOT NULL,
      loot_enabled INTEGER NOT NULL DEFAULT 1
    );
    CREATE TABLE IF NOT EXISTS collectibles (
      id TEXT PRIMARY KEY, vault_id TEXT NOT NULL REFERENCES vaults(id), name TEXT NOT NULL,
      rarity TEXT NOT NULL, estimated_value_cents INTEGER NOT NULL, custody_status TEXT NOT NULL,
      art TEXT NOT NULL DEFAULT 'fox-art', image_path TEXT NOT NULL DEFAULT 'collectibles/fox.svg',
      seed TEXT, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS approvals (
      id TEXT PRIMARY KEY, collectible_id TEXT NOT NULL REFERENCES collectibles(id), action TEXT NOT NULL,
      status TEXT NOT NULL, requested_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS loot_boxes (
      id TEXT PRIMARY KEY, label TEXT NOT NULL, cost_cents INTEGER NOT NULL,
      purchase_enabled INTEGER NOT NULL, odds_disclosed INTEGER NOT NULL
    );
    CREATE TABLE IF NOT EXISTS loot_events (
      id TEXT PRIMARY KEY, vault_id TEXT NOT NULL REFERENCES vaults(id), box_id TEXT NOT NULL,
      reward_json TEXT NOT NULL, status TEXT NOT NULL, created_at TEXT NOT NULL,
      claimed_at TEXT
    );
    """)
    for column, definition in [("loot_enabled", "INTEGER NOT NULL DEFAULT 1")]:
        if not has_column(con, "vaults", column):
            con.execute(f"ALTER TABLE vaults ADD COLUMN {column} {definition}")
    for column, definition in [("art", "TEXT NOT NULL DEFAULT 'fox-art'"), ("image_path", "TEXT NOT NULL DEFAULT 'collectibles/fox.svg'"), ("seed", "TEXT"), ("created_at", "TEXT")]:
        if not has_column(con, "collectibles", column):
            con.execute(f"ALTER TABLE collectibles ADD COLUMN {column} {definition}")
    con.execute("INSERT OR IGNORE INTO vaults (id, child_name, guardian_status, loot_enabled) VALUES (?, ?, ?, 1)", (VAULT_ID, "Maya", "parent approval on"))
    con.executemany("INSERT OR IGNORE INTO loot_boxes VALUES (?, ?, 0, 0, 0)", [("box-sky", "Sky box"), ("box-garden", "Garden box"), ("box-robot", "Robot box")])
    con.executemany("INSERT OR IGNORE INTO collectibles (id, vault_id, name, rarity, estimated_value_cents, custody_status, art, image_path, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", [
        ("nft-042", VAULT_ID, "Skyline Fox #042", "Common", 1200, "custodial", "fox-art", "collectibles/fox.svg", "2026-06-18T12:00:00+00:00"),
        ("nft-117", VAULT_ID, "Garden Robot #117", "Rare", 2800, "custodial", "robot-art", "collectibles/robot-golem.svg", "2026-06-12T12:00:00+00:00"),
    ])
    con.execute("UPDATE collectibles SET art = 'fox-art', image_path = 'collectibles/fox.svg', created_at = COALESCE(created_at, '2026-06-18T12:00:00+00:00') WHERE id = 'nft-042'")
    con.execute("UPDATE collectibles SET art = 'robot-art', image_path = 'collectibles/robot-golem.svg', created_at = COALESCE(created_at, '2026-06-12T12:00:00+00:00') WHERE id = 'nft-117'")
    con.execute("DELETE FROM collectibles WHERE name = 'Copper Bot #811'")
    con.commit()
    con.close()


def reward_for(box_id, used_names):
    """Create a server-selected collectible that has not appeared in this vault before."""
    for _ in range(64):
        seed = secrets.token_hex(16)
        value = int(hashlib.sha256(f"{box_id}:{seed}".encode()).hexdigest(), 16)
        item = CATALOG[value % len(CATALOG)]
        rarity, cents = RARITIES[(value >> 4) % len(RARITIES)]
        prefix = PREFIXES[box_id][(value >> 8) % len(PREFIXES[box_id])]
        name = f"{prefix} {item['kind']} #{(value % 900) + 100}"
        if name not in used_names:
            return {"seed": seed, "name": name, "rarity": rarity, "value_cents": cents, **item}
    raise RuntimeError("No new reward is available for this vault.")


class VaultHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(OUTPUTS), **kwargs)

    def json_response(self, status, payload):
        data = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def read_json(self):
        size = int(self.headers.get("Content-Length", "0"))
        return json.loads(self.rfile.read(size) or b"{}")

    def do_GET(self):
        if urlparse(self.path).path == "/api/vault":
            con = connection()
            vault = dict(con.execute("SELECT id, child_name, guardian_status, loot_enabled FROM vaults WHERE id = ?", (VAULT_ID,)).fetchone())
            collectibles = [dict(row) for row in con.execute("SELECT id, name, rarity, estimated_value_cents, custody_status, art, image_path, created_at FROM collectibles WHERE vault_id = ? ORDER BY created_at DESC", (VAULT_ID,))]
            con.close()
            self.json_response(HTTPStatus.OK, {"vault": vault, "collectibles": collectibles})
            return
        super().do_GET()

    def do_POST(self):
        path = urlparse(self.path).path
        payload = self.read_json()
        if path == "/api/loot/open":
            box_id = payload.get("box")
            if box_id not in PREFIXES:
                self.json_response(HTTPStatus.BAD_REQUEST, {"error": "Unknown loot box."}); return
            con = connection()
            enabled = con.execute("SELECT loot_enabled FROM vaults WHERE id = ?", (VAULT_ID,)).fetchone()[0]
            if not enabled:
                con.close(); self.json_response(HTTPStatus.CONFLICT, {"error": "Loot boxes are turned off by parent controls."}); return
            used_names = {row["name"] for row in con.execute("SELECT name FROM collectibles WHERE vault_id = ?", (VAULT_ID,))}
            for row in con.execute("SELECT reward_json FROM loot_events WHERE vault_id = ?", (VAULT_ID,)):
                used_names.add(json.loads(row["reward_json"])["name"])
            reward = reward_for(box_id, used_names)
            event_id = f"loot-{secrets.token_hex(8)}"
            now = datetime.now(timezone.utc).isoformat()
            con.execute("INSERT INTO loot_events VALUES (?, ?, ?, ?, 'opened', ?, NULL)", (event_id, VAULT_ID, box_id, json.dumps(reward), now))
            con.commit(); con.close()
            self.json_response(HTTPStatus.CREATED, {"event_id": event_id, "reward": reward}); return
        if path == "/api/loot/claim":
            event_id = payload.get("event_id")
            con = connection()
            event = con.execute("SELECT reward_json, status FROM loot_events WHERE id = ? AND vault_id = ?", (event_id, VAULT_ID)).fetchone()
            if not event or event["status"] != "opened":
                con.close(); self.json_response(HTTPStatus.CONFLICT, {"error": "This reward is no longer available."}); return
            reward = json.loads(event["reward_json"])
            collectible_id = f"nft-{secrets.token_hex(8)}"
            now = datetime.now(timezone.utc).isoformat()
            con.execute("INSERT INTO collectibles VALUES (?, ?, ?, ?, ?, 'custodial', ?, ?, ?, ?)", (collectible_id, VAULT_ID, reward["name"], reward["rarity"], reward["value_cents"], reward["art"], reward["image"], reward["seed"], now))
            con.execute("UPDATE loot_events SET status = 'claimed', claimed_at = ? WHERE id = ?", (now, event_id))
            con.commit(); con.close()
            self.json_response(HTTPStatus.CREATED, {"id": collectible_id, **reward}); return
        if path == "/api/controls":
            enabled = bool(payload.get("loot_enabled"))
            con = connection(); con.execute("UPDATE vaults SET loot_enabled = ? WHERE id = ?", (int(enabled), VAULT_ID)); con.commit(); con.close()
            self.json_response(HTTPStatus.OK, {"loot_enabled": enabled}); return
        if path == "/api/trades":
            con = connection()
            collectible = con.execute("SELECT id FROM collectibles WHERE vault_id = ? ORDER BY created_at LIMIT 1", (VAULT_ID,)).fetchone()
            approval_id = f"approval-{secrets.token_hex(8)}"
            now = datetime.now(timezone.utc).isoformat()
            con.execute("INSERT INTO approvals VALUES (?, ?, 'trade', 'pending_parent_review', ?)", (approval_id, collectible[0], now))
            con.commit(); con.close()
            self.json_response(HTTPStatus.CREATED, {"id": approval_id, "status": "pending_parent_review"}); return
        self.json_response(HTTPStatus.NOT_FOUND, {"error": "Not found."})


if __name__ == "__main__":
    setup_database()
    print("Horizon NFT Vault running at http://127.0.0.1:8787")
    ThreadingHTTPServer(("127.0.0.1", 8787), VaultHandler).serve_forever()
