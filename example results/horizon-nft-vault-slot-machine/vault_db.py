"""Project-owned SQLite fixture for the Horizon NFT Vault prototype."""
import sqlite3
from pathlib import Path

DB = Path(__file__).with_name("nft_vault.sqlite3")

def seed(path=DB):
    con = sqlite3.connect(path)
    con.executescript("""
    PRAGMA foreign_keys = ON;
    CREATE TABLE IF NOT EXISTS vaults (id TEXT PRIMARY KEY, child_name TEXT NOT NULL, guardian_status TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS collectibles (id TEXT PRIMARY KEY, vault_id TEXT NOT NULL REFERENCES vaults(id), name TEXT NOT NULL, rarity TEXT NOT NULL, estimated_value_cents INTEGER NOT NULL, custody_status TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS approvals (id TEXT PRIMARY KEY, collectible_id TEXT NOT NULL REFERENCES collectibles(id), action TEXT NOT NULL, status TEXT NOT NULL, requested_at TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS loot_boxes (id TEXT PRIMARY KEY, label TEXT NOT NULL, cost_cents INTEGER NOT NULL, purchase_enabled INTEGER NOT NULL, odds_disclosed INTEGER NOT NULL);
    """)
    con.execute("INSERT OR IGNORE INTO vaults VALUES ('vault-maya-001','Maya','parent approval on')")
    con.executemany("INSERT OR IGNORE INTO collectibles VALUES (?,?,?,?,?,?)", [('nft-042','vault-maya-001','Skyline Fox #042','Common',1200,'custodial'),('nft-117','vault-maya-001','Garden Robot #117','Rare',2800,'custodial')])
    con.executemany("INSERT OR IGNORE INTO loot_boxes VALUES (?,?,?,?,?)", [('box-sky','Sky box',0,0,0),('box-garden','Garden box',0,0,0),('box-robot','Robot box',0,0,0)])
    con.commit(); con.close(); print(f"Seeded {path}")

if __name__ == "__main__": seed()
