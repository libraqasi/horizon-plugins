# Horizon Bank Plugins Agent Guide

## Mission

Maintain the independent Horizon Bank plugin marketplace. This repository owns
reusable Horizon Bank skills, plugin manifests, design assets, validation
scripts, and enablement collateral. Product repositories are consumers.

## Canonical structure

- Marketplace manifest: `.agents/plugins/marketplace.json`
- Plugins: `plugins/<plugin-name>/`
- Marketplace validation: `scripts/marketplace/`
- Enablement collateral: `pdf/` and `presentation/`

Keep marketplace `source.path` values relative to this repository root, using
`./plugins/<plugin-name>`.

## Plugin requirements

- Every plugin has `.codex-plugin/plugin.json`.
- Every skill has a complete `SKILL.md` and passes the Codex skill validator.
- Replace the single `+codex.<cachebuster>` suffix when updating a plugin.
- Preserve the Horizon Bank identity and reusable guidance without referring to
  consumer project names.
- Do not duplicate a plugin into a prototype or application repository.
- Keep stock imagery, fonts, logos, icons, starter code, and instructions inside
  the plugin that owns them.
- Validate manifests, skills, marketplace paths, source audits, and rendered
  examples before handoff.

## Adding future plugins

1. Create `plugins/<plugin-name>/`.
2. Add its manifest, skills, and assets.
3. Append its marketplace entry without reordering existing entries.
4. Run the plugin, skill, and marketplace validators.
5. Install or reinstall it from `horizon-bank`.
6. Test it in a new Codex task.

## Consumer boundary

Product prototypes may install and use this marketplace. They must not become
the canonical source of its plugins or marketplace configuration.
