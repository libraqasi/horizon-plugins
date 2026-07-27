# Validation rules

## Structure and reproducibility

- Require a supported schema version, manifest, resolved config, collection counts, and SHA-256 hashes.
- Require unique IDs and valid customer, account, merchant, transaction, household, business, dispute, and delegation references.
- Regenerate a fixed config and compare every canonical JSONL hash with the inspected dataset.

## Financial consistency

- Reconcile posted account activity from opening to current balance.
- Exclude pending activity from the posted ledger.
- Verify card available credit and utilization.
- Verify budget windows and category totals from transactions.
- Verify current goal amount does not exceed target unless overfunding is explicit.
- Verify loan monthly payment from principal, APR, and term.
- Keep money integral in minor units and rates integral in basis points.

## Dates and state

- Parse every declared ISO date.
- Keep historical events inside the configured window.
- Keep future due/target dates after the scenario date.
- Require explicit status for pending, posted, disputed, late, and review states.
- Require overlays to reference affected entities.

## Synthetic-data safety

- Require `synthetic: true`.
- Require `.example` emails and reserved 555-01xx phone ranges.
- Reject passwords, PINs, security answers, SSNs, routing numbers, full account numbers, valid full PANs, API keys, and access tokens.
- Reject reusable non-Horizon bank identity and consumer-project names.
- Use opaque IDs and display-only last four values.

## Export parity

- Compare JSONL counts to the manifest.
- Compare CSV, Mongo JSONL, SQLite, and bundle payloads—not only row counts—to canonical JSONL.
- Open SQLite exports in immutable read-only mode and reject mutable `-wal` or `-shm` sidecars.
- Inspect representative joined snapshots, not only raw files.
- Treat privacy, identity, relationship, date, and arithmetic failures as errors in every mode.
