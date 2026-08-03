# Financial Twin Offer Studio

Standalone Horizon Bank prototype for an illustrative, local Financial Twin
life-simulation experience. It is self-contained: source code, local assets,
flat JSON scenario data, built output, and the installed `node_modules` folder
are included.

## Run locally

From this directory:

```bash
npm run dev
```

Then open the URL shown by Vite (normally `http://localhost:5173/`).

## Build a production bundle

```bash
npm run build
```

The production files are emitted to `dist/`.

## If dependencies need to be restored

`node_modules/` is included for immediate local use. If it has been removed,
restore the locked versions with:

```bash
npm install
```

## Project contents

- `src/` — React UI and deterministic simulator logic.
- `public/data/` — local synthetic customer snapshot and scenario JSON.
- `public/assets/` — images, logo assets, and fonts used by the prototype.
- `dist/` — the most recently built static bundle.

All Financial Twin outcomes are illustrative, local, and educational; they do
not represent actual financial terms, savings, rewards, eligibility, or account
activity.
