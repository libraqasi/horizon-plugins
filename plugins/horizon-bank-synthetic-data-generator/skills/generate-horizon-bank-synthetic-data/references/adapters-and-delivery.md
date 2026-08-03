# Adapters and delivery

## Flat files

- Use the JSON bundle for human-reviewable or single-customer prototypes.
- Use per-collection JSONL for streaming, Mongo import, or model pipelines.
- Use CSV when a lossless row wrapper is convenient for review or simple imports. Each row keeps indexed identifiers plus the complete canonical record in `payload_json`; it is not a normalized analyst table.
- Preserve canonical IDs, minor units, basis points, and ISO dates in source exports.

## SQLite and MongoDB

- Use generated SQLite as an indexed read-only JSON payload store and for the bundled fixture server. It is not a normalized application database or ORM schema.
- Query the `payload` JSON only after filtering by indexed `id`, `customer_id`, or `account_id`.
- Use `mongo/*.jsonl` and the generated import instructions for MongoDB.
- Add project-specific indexes and mutation routes in the consumer, not in the plugin.

## Python, TypeScript, and application fixtures

- Load canonical records once and map them through a typed adapter.
- Convert minor units to display decimals only at the UI or API boundary.
- Convert basis points to percentages only at the boundary.
- Keep adapter functions pure where possible and test them with stable entity IDs.
- Never hand-copy aggregate values into a second fixture.

These mappings are guidance, not a required application architecture. Consumers may use their own language-native models, schema validators, OpenAPI descriptions, databases, APIs, or offline projections. Keep the adapter thin enough that canonical IDs, units, dates, relationships, and synthetic-data boundaries remain traceable and testable.

## REST fixtures

Start the server with:

```bash
python3 scripts/serve_horizon_data.py --db <dataset.sqlite>
```

Use `/health`, `/v1/metadata`, `/v1/customers`, `/v1/customers/{id}`, `/v1/customers/{id}/accounts`, `/v1/customers/{id}/disputes`, `/v1/accounts/{id}/transactions`, `/v1/customers/{id}/snapshot`, and `/v1/events`.

Bind to `127.0.0.1` by default. The fixture server is read-only and returns `X-Synthetic-Data: true`.

## LLM and voice context

- Build a task-specific snapshot at session or request time.
- Include stable entity IDs when tools or visual navigation need them.
- Include exact financial facts needed for the current task, not the entire relationship.
- Set and test a context-size budget for the target model. If the project has no limit, start at 8 KiB per intent-specific customer snapshot and reduce it when the journey needs less.
- Keep deterministic calculations in code or tool handlers.
- State what the data does not cover instead of inviting model invention.

## Mutable prototypes

Generate a project-owned adapter with explicit commands, validation, and persistence. Define idempotency, pending/posted transitions, transfer double entry, conflict handling, reset behavior, and test isolation before adding write endpoints.
