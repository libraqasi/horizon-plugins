---
name: validate-horizon-bank-synthetic-data
description: Validate synthetic Horizon Bank banking datasets and adapters for schema, privacy, safety, dates, reproducibility, referential integrity, ledger reconciliation, derived financial values, export parity, LLM narrative grounding, and prototype truth boundaries. Use before handing off generated JSON, JSONL, CSV, SQLite, MongoDB, REST fixtures, personas, transactions, customer context, seeded databases, or imported legacy mock data.
---

# Validate Horizon Bank Synthetic Data

Treat synthetic data as production code: prove that every exported view comes from coherent facts and cannot be mistaken for real customer records.

## Required workflow

1. Read [validation-rules.md](references/validation-rules.md) for every audit.
2. Read [legacy-data-triage.md](references/legacy-data-triage.md) when reviewing hand-written, imported, or prompt-embedded mock data.
3. Identify the canonical dataset and every derived export or adapter. Do not validate one file while ignoring duplicated facts elsewhere.
4. Resolve `VALIDATOR_SKILL_DIR` to the absolute directory containing this `SKILL.md`. For generated canonical data, run:

```bash
python3 "$VALIDATOR_SKILL_DIR/scripts/validate_horizon_data.py" \
  <dataset-directory> --strict --reproducibility-check
```

For imported legacy fixtures that have no generator config, omit `--reproducibility-check` and document why.

5. Fix errors at the canonical source or generation rule. Regenerate derived outputs instead of patching JSON, CSV, SQLite, Mongo files, prompts, or UI fixtures independently.
6. Verify target-specific behavior:
   - exact fields and types match the consumer;
   - compact LLM context contains only relevant facts and stable IDs;
   - deterministic calculators use canonical amounts;
   - read-only demos do not imply completed money movement;
   - mutable adapters persist and reconcile state as planned.
7. Re-run validation, project tests, and acceptance queries. Report record counts, scenario date, seed, archetypes, overlays, formats, and any intentional warnings.

## Strict acceptance gate

Require all of the following:

- manifest hashes and collection counts match;
- IDs are unique and all relationships resolve;
- posted transactions reconcile account balances;
- card limits, available credit, utilization, budgets, goals, and loan payments agree;
- dates fit the declared history window and scenario date;
- flat files, SQLite, and Mongo exports contain the same canonical records;
- all records are explicitly synthetic and use safe identifiers;
- no credentials, SSNs, valid card numbers, routing numbers, full account numbers, or unsafe contact details exist;
- no consumer-project identity or non-Horizon bank identity leaks into reusable data;
- the same fixed config and seed reproduce the same canonical output.

Do not downgrade privacy, arithmetic, identity, or relationship failures to warnings.
