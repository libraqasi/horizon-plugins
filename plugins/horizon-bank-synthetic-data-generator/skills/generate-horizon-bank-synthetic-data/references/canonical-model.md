# Canonical Horizon synthetic data model

## Configuration

Use `schema_version`, `dataset.name`, `seed`, `scenario_date`, `time_mode`, `timezone`, `locale`, `currency`, `scale`, `archetypes`, `modules`, `overlays`, `outputs.formats`, and `narrative.mode`.

- `time_mode: fixed` requires an ISO scenario date.
- `time_mode: rolling` resolves today once in the configured IANA timezone, records it, and never changes while serving.
- CLI overrides win over config values and are written to `manifest.json`.
- Money uses integer minor units plus ISO currency. Rates use integer basis points.
- `currency` is propagated to every generated monetary record. `locale` is recorded as scenario metadata for consumer adapters; it does not localize names, narrative, addresses, or display formatting.

The canonical collections are a reusable source model, not a mandatory consumer contract. Projects may select, project, rename, or adapt fields for their own schemas while preserving stable IDs, relationships, units, dates, synthetic markers, and validated financial invariants.

## Core collections

- `customers`: synthetic identity, safe contact details, archetype, active overlays, and profile narrative.
- `households`: customer-to-guardian, partner, dependent, or household relationships.
- `businesses`: owner links and business operating attributes.
- `accounts`: type, product, opening/current balance, currency, status, and date.
- `transactions`: account/customer/merchant links, direction, signed amount, status, category, and date.
- `merchants`: reusable fictional merchant catalog.
- `events`: selected overlays and their linked entities.

## Optional collections

- `cards`, `incomes`, `loans`, `investments`, `budgets`, `goals`, `rewards`
- `alerts`, `service_interactions`, `devices`, `disputes`, `delegations`

Use dispute statuses `submitted`, `under_review`, `provisional_credit_issued`, `resolved_customer_favor`, `resolved_merchant_favor`, or `withdrawn`. A dispute must reference one posted debit owned by the same customer and account. Any provisional or final credit must be a separate linked posted credit; do not silently alter the original transaction.

## Required invariants

- Use stable opaque IDs derived from schema version, seed, entity type, and sequence.
- Keep credits positive and debits negative; also include an explicit `direction`.
- Reconcile posted transactions as `posted = opening + sum(posted signed amounts)`.
- Exclude pending transactions from posted account balance.
- Derive available credit and utilization from limit and amount owed.
- Derive budget spending from transactions in the declared budget window.
- Derive goal percent, net worth, cash flow, and loan payment instead of duplicating editable values.
- Link every non-null foreign key to a real entity.
- Keep dates inside the history window unless a field is explicitly future-looking.

## Safe identity

Use `.example` emails, reserved 555-01xx phone numbers with synthetic extensions, fictional street lines, opaque account IDs, and last-four display values. Do not create secrets or full regulated identifiers.
