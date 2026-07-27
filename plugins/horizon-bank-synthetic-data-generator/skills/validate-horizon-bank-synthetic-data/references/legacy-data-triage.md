# Legacy synthetic-data triage

## Inventory before editing

- Find every JSON, JSONL, CSV, SQL, database, fixture module, prompt literal, test fixture, and documentation sample.
- Trace which copy is actually loaded at runtime.
- Extract schemas and scalar types before comparing values.
- Identify customer facts duplicated in prompts, UI code, and service code.

## Frequent defects

- One customer has different names in narrative, prompt, and JSON.
- Documentation describes old dates or values after fixture edits.
- Currency alternates between strings, floats, signed values, and positive values.
- Duplicate or malformed keys silently split data.
- Account summaries disagree with transaction history.
- Derived totals are hand-maintained and stale.
- Relative dates such as “Friday” have no scenario date.
- Full contact, account, card, or authentication data is included for realism.
- LLM prompts receive an entire banking relationship rather than a task-specific view.

## Migration

1. Choose the runtime source of truth.
2. Map it to the canonical model without copying unsafe identifiers.
3. Normalize IDs, dates, money, rates, directions, statuses, and relationships.
4. Recompute aggregates from canonical facts.
5. Generate fresh target adapters and prompt context.
6. Remove or clearly retire duplicated runtime fixtures.
7. Validate both canonical output and the consuming experience.

Do not preserve a legacy defect solely for backward compatibility. Add an explicit adapter only when the consumer contract requires it.
