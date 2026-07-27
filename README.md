# Horizon Bank Plugins

This repository is the canonical home for reusable Horizon Bank plugins, skills,
design assets, validation tools, and the Horizon Bank Codex marketplace.
Product prototypes consume this marketplace; they do not own or vendor its
source.

## Repository layout

```text
.
├── .agents/plugins/marketplace.json
├── plugins/
│   ├── horizon-bank-design/
│   └── horizon-bank-synthetic-data-generator/
├── scripts/marketplace/
├── pdf/
└── presentation/
```

Future plugins belong under `plugins/<plugin-name>/`. Add each plugin to
`.agents/plugins/marketplace.json` with a repository-relative source path such
as `./plugins/<plugin-name>`.

## Install from this local checkout

```bash
codex plugin marketplace add "/absolute/path/to/Horizon Bank Plugins"
codex plugin add horizon-bank-design@horizon-bank
codex plugin add horizon-bank-synthetic-data-generator@horizon-bank
```

Start a new Codex task after installing or updating a plugin so the refreshed
skills are loaded.

## Install after publishing to GitHub or GitLab

GitHub:

```bash
codex plugin marketplace add OWNER/REPOSITORY
codex plugin add horizon-bank-design@horizon-bank
```

GitLab or another Git host:

```bash
codex plugin marketplace add https://gitlab.com/GROUP/REPOSITORY.git
codex plugin add horizon-bank-design@horizon-bank
```

The repository root must contain `.agents/plugins/marketplace.json`. Preserve
the layout above when publishing.

## Validate

```bash
python3 scripts/marketplace/validate_marketplace.py
python3 plugins/horizon-bank-design/skills/build-horizon-bank-ui/scripts/audit_horizon_ui.py \
  --strict plugins/horizon-bank-design/skills/build-horizon-bank-ui/assets/starter
python3 plugins/horizon-bank-synthetic-data-generator/skills/generate-horizon-bank-synthetic-data/scripts/generate_horizon_data.py \
  --config plugins/horizon-bank-synthetic-data-generator/skills/generate-horizon-bank-synthetic-data/assets/configs/all-archetypes-small.json \
  --out /tmp/horizon-synthetic-data
python3 plugins/horizon-bank-synthetic-data-generator/skills/validate-horizon-bank-synthetic-data/scripts/validate_horizon_data.py \
  /tmp/horizon-synthetic-data --strict --reproducibility-check
```

The Codex plugin and skill validators should also pass before publishing.

## Update an existing plugin

Use the Codex plugin-creator cachebuster helper, validate the repository, and
then reinstall from the `horizon-bank` marketplace. Do not copy the plugin into
consumer product repositories.
