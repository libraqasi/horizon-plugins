# Horizon NFT Vault — Slot-Machine Rewards

An interactive Horizon Bank prototype for a custodial digital-asset vault. It includes the slot-machine loot-box flow, themed collectible artwork, and a SQLite-backed vault so reward openings, claims, and collection state persist locally.

## Included runtime

- `server.py` — local HTTP server and JSON API.
- `vault_db.py` — SQLite fixture helpers.
- `nft_vault.sqlite3` — persisted vault, collectible, and loot-event data.
- `outputs/` — the web UI, Horizon Bank assets, and collectible SVG artwork.

## Requirements

Python 3 with its standard library. No package installation or external service is required; SQLite is provided by Python's built-in `sqlite3` module.

## Run locally

```bash
cd "/Users/rameshyarlagadda/Desktop/-0- Wells Fargo Work/Horizon Bank Plugins/example results/horizon-nft-vault-slot-machine"
python3 server.py
```

Keep that terminal open, then visit <http://127.0.0.1:8787/>. The server binds only to `127.0.0.1`, so the vault stays local to this machine.

## Persistent data

Actions such as opening a reward and claiming it into the vault write to `nft_vault.sqlite3`. Keep this file when moving or backing up the example if you want to retain the current collection and event history.
