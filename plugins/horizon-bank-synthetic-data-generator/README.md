# Horizon Bank Synthetic Data Generator

Reusable Codex skills and a dependency-free Python toolkit for planning, generating, serving, adapting, and validating synthetic banking data for Horizon Bank prototypes.

## Skills

- `plan-horizon-bank-synthetic-data`: inspect a target project and produce a decision-complete data brief.
- `generate-horizon-bank-synthetic-data`: generate one seeded source of truth and portable exports.
- `validate-horizon-bank-synthetic-data`: audit privacy, relationships, dates, arithmetic, reproducibility, and export parity.

## Quick start

```bash
GENERATOR_SKILL="skills/generate-horizon-bank-synthetic-data"
VALIDATOR_SKILL="skills/validate-horizon-bank-synthetic-data"

python3 "$GENERATOR_SKILL/scripts/generate_horizon_data.py" \
  --config "$GENERATOR_SKILL/assets/configs/all-archetypes-small.json" \
  --out /tmp/horizon-synthetic-data

python3 "$VALIDATOR_SKILL/scripts/validate_horizon_data.py" \
  /tmp/horizon-synthetic-data --strict --reproducibility-check
```

The generated manifest records the resolved seed, scenario date, configuration, collection counts, and SHA-256 hashes. Canonical JSONL is always emitted; configs may also request a human-reviewable JSON bundle, lossless CSV payload wrappers, an indexed read-only SQLite JSON payload store, and MongoDB import JSONL. These are portable starting points, not mandatory application schemas; consuming projects may map them into their own types, projections, databases, or APIs.

Start the local read-only fixture API with:

```bash
python3 "$GENERATOR_SKILL/scripts/serve_horizon_data.py" \
  --db /tmp/horizon-synthetic-data/horizon_synthetic.sqlite
```

Generated identities are explicitly synthetic. The toolkit does not create credentials, SSNs, routing numbers, full account numbers, or valid full payment-card numbers.
