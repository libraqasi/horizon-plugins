# Horizon digital-assets demo data

This project uses a fixed, deterministic Horizon Bank synthetic fixture:

- Config: `data/config/horizon-digital-assets.json`
- Canonical exports: `data/generated/`
- Mutable app database: `data/horizon_app.sqlite`
- SQLite adapter: `data/build_app_db.py`
- Combined app and API server: `server.py` on port `5180`

The target journey is a single-customer digital-assets overview with stablecoin buy/sell review, custody balance, wallet address display, and pending/posted activity filtering. The canonical `agentic-digital-wallet` archetype supplies the synthetic customer, funding accounts, dates, identity-safe contacts, and banking relationships. The project adapter adds a deterministic USDC ledger derived from the generated reserve account; asset balances are recomputed from posted ledger rows.

## Run the packaged demo

From the project root, run:

```bash
npm start
```

Then open `http://127.0.0.1:5180/`. This serves the production interface and
the SQLite API together.

## Regenerate synthetic data (optional)

```bash
python3 "$HOME/.codex/plugins/cache/horizon-bank/horizon-bank-synthetic-data-generator/1.0.0+codex.20260727200151/skills/generate-horizon-bank-synthetic-data/scripts/validate_horizon_config.py" data/config/horizon-digital-assets.json
python3 "$HOME/.codex/plugins/cache/horizon-bank/horizon-bank-synthetic-data-generator/1.0.0+codex.20260727200151/skills/generate-horizon-bank-synthetic-data/scripts/generate_horizon_data.py" --config data/config/horizon-digital-assets.json --out data/generated --force
python3 data/build_app_db.py
```

The generation commands require the Horizon Bank synthetic-data plugin to be
installed. For ordinary demo use, the generated data and app database already
included in this folder are sufficient.

The browser order flow is explicitly simulated: confirming an order writes a pending row to `app_orders` and `asset_transactions`; it does not send a real transaction.
