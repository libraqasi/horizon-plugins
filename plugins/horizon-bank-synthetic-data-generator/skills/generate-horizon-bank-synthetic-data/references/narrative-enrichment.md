# Controlled narrative enrichment

Use narrative enrichment only when template text is insufficient for voice, conversational, or storytelling surfaces.

## Workflow

1. Generate deterministic data with `narrative.mode` set to `slots`.
2. Read `narrative-slots.jsonl`. Each slot contains an entity ID, allowed field, and facts.
3. Write one concise override per requested slot without adding unsupported numbers, dates, products, identities, decisions, or outcomes.
4. Save JSONL records shaped as:

```json
{"entity_id":"cust_...","field":"profile_summary","text":"A concise fact-grounded summary."}
```

5. Regenerate with `--narrative-overrides <file>`.
6. Run strict validation and inspect the resulting prompt/context view.

## Allowed fields

- `customers.profile_summary`
- transaction or service notes only when the target adapter explicitly declares the field
- customer-facing alert copy that does not change alert state

## Prohibited changes

Do not change IDs, relationships, names, dates, money, currency, rates, balances, product status, eligibility, risk, fraud decisions, or calculated recommendations. Do not introduce a numeric fact that is absent from the supplied slot facts.
