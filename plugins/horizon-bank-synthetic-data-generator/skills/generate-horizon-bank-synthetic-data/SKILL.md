---
name: generate-horizon-bank-synthetic-data
description: Generate reproducible synthetic Horizon Bank personas, households, businesses, accounts, cards, transactions, loans, goals, budgets, alerts, service records, and delegated-payment data. Use for JSON, JSONL, CSV, SQLite, MongoDB import files, local REST fixtures, Python or TypeScript adapters, LLM context builders, voice agents, dashboards, wearables, deterministic calculators, seeded tests, and small through stress-scale prototype datasets.
---

# Generate Horizon Bank Synthetic Data

Generate one canonical, seeded source of truth and adapt it to the prototype rather than maintaining unrelated hand-written fixtures.

The bundled canonical model, exports, REST fixture, and adapter examples are optional starting points. A consuming project may use its own schema, projection, database, API, or language-native types as long as stable relationships, minor-unit money, basis-point rates, scenario dates, synthetic-data safety, deterministic calculations, and reproducibility remain explicit and testable.

## Required workflow

1. Require a decision-complete plan or inspect the project and use `$plan-horizon-bank-synthetic-data`.
2. Read [canonical-model.md](references/canonical-model.md) before changing the config or mapping fields.
3. Read [adapters-and-delivery.md](references/adapters-and-delivery.md) for the target format, database, API, language, or LLM surface.
4. Read [narrative-enrichment.md](references/narrative-enrichment.md) only when model-written bios, notes, dialogue, or summaries are requested.
5. Resolve `GENERATOR_SKILL_DIR` to the absolute directory containing this `SKILL.md`. Start from the closest config in `assets/configs/`. Copy it into the consuming project or a temporary output area; do not edit the bundled preset in place.
6. Validate the config, then generate:

```bash
python3 "$GENERATOR_SKILL_DIR/scripts/validate_horizon_config.py" <config.json>
python3 "$GENERATOR_SKILL_DIR/scripts/generate_horizon_data.py" \
  --config <config.json> --out <output-directory>
```

7. Inspect `manifest.json`, a representative customer, linked accounts, transactions, overlays, and requested exports.
8. Build the thinnest target adapter:
   - map canonical minor-unit money and basis-point rates at the boundary;
   - preserve stable IDs and scenario dates;
   - compute rather than duplicate aggregates;
   - construct compact customer snapshots for LLM prompts;
   - keep state-changing routes inside the consuming project.
9. Run the sibling validation skill:

```bash
python3 "$GENERATOR_SKILL_DIR/../validate-horizon-bank-synthetic-data/scripts/validate_horizon_data.py" \
  <output-directory> --strict --reproducibility-check
```

10. Run the target project’s tests and exercise the acceptance queries from the plan.

## Toolkit

- `scripts/generate_horizon_data.py`: create fixed or rolling seeded data and portable exports.
- `scripts/validate_horizon_config.py`: enforce and resolve the bundled config contract without writing data.
- `scripts/serve_horizon_data.py`: serve the indexed SQLite JSON payload store through a read-only local REST API.
- `assets/configs/`: nine customer archetypes plus an all-archetype small dataset.
- `assets/config.schema.json`: machine-readable generator configuration contract; it does not prescribe a consumer application's schema.
- `references/`: canonical fields, adapter patterns, and controlled narrative enrichment.

## Non-negotiable boundaries

- Use Horizon Bank naming and clearly synthetic metadata.
- Generate financial facts deterministically. Never let an LLM invent or reconcile balances, dates, rates, eligibility, or IDs.
- Use `.example` email domains, reserved 555 phone ranges, opaque IDs, and display-only last four values.
- Never create credentials, SSNs, valid full PANs, routing numbers, or full bank account numbers.
- Keep protected attributes independent from pricing, creditworthiness, risk, fraud, and eligibility.
- Do not copy this plugin into a prototype repository. Copy only generated outputs or a required adapter.
