# Horizon Bank Digital Assets Demo

A runnable, SQLite-backed Horizon Bank prototype for digital-asset custody,
USDC buy/sell simulation, wallet controls, and activity review. All customer
and transaction information is synthetic and is included in this folder.

## Run the demo

From this folder, run:

```bash
npm start
```

Then open [http://127.0.0.1:5180/](http://127.0.0.1:5180/) in a browser on the
same Mac. The server serves the built React app, its CSS/JavaScript assets, and
the SQLite API from one process.

To open the demo from another device on the same network, use this Mac's LAN IP
and port `5180`, for example `http://<mac-lan-ip>:5180/`.

## Included dependencies and data

- `node_modules/` — installed React/Vite dependencies, included for immediate local use.
- `dist/` — the production web bundle served by `npm start`.
- `data/horizon_app.sqlite` — the mutable application database.
- `data/generated/` — reproducible synthetic source data and exports.
- `server.py` — combined static web server and SQLite API.

No external service or real banking, wallet, or blockchain connection is used.
Submitting a buy or sell action writes a simulated pending record to the local
SQLite database only.

## Develop or rebuild

Use `npm run dev` for Vite development mode. After modifying frontend files,
run `npm run build` before `npm start` so the production bundle is refreshed.

If dependencies are removed, restore them with:

```bash
npm ci
```

## Project layout

- `src/` — React interface and styles.
- `public/` — Horizon brand assets and fonts.
- `data/` — synthetic data configuration, generated data, and SQLite adapter.
- `outputs/` — captured design-review images.
- `server.py` — production server and API routes.
