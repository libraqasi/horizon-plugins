---
name: plan-horizon-bank-synthetic-data
description: Inspect and plan synthetic Horizon Bank customer and financial data for prototypes before generation. Use when a developer needs to decide personas, schemas, scale, dates, persistence, flat files, databases, REST APIs, Python or TypeScript fixtures, MongoDB or SQLite seeds, LLM context, deterministic calculators, dynamic behavior, test scenarios, or data-quality requirements.
---

# Plan Horizon Bank Synthetic Data

Define the smallest coherent dataset that proves the target experience. Inspect first; ask only for product decisions that the project cannot answer.

## Required workflow

1. Inspect the target repository, schemas, types, fixtures, routes, prompts, database setup, and tests. Identify every consumer of customer data.
2. Read [discovery-questionnaire.md](references/discovery-questionnaire.md) and resolve discoverable facts without asking.
3. Read [archetypes-and-overlays.md](references/archetypes-and-overlays.md) to select customer archetypes and named events without tying financial outcomes to protected traits.
4. Read the sibling generator’s [canonical model](../generate-horizon-bank-synthetic-data/references/canonical-model.md), [configuration schema](../generate-horizon-bank-synthetic-data/assets/config.schema.json), and [adapter and LLM-context guidance](../generate-horizon-bank-synthetic-data/references/adapters-and-delivery.md). Any runnable config must be valid JSON matching that schema.
5. Ask unresolved questions one at a time. Cover journey, audience, data contract, integration, time behavior, state, scale, optional LLM use, edge cases, and acceptance queries.
6. Prefer a canonical Horizon model plus a thin target adapter when it reduces duplication. The canonical model is an optional starting point rather than a required application contract; use the target schema directly when it better fits the experience and the required safety and financial invariants remain testable.
7. Choose deterministic generation for IDs, dates, money, relationships, balances, rates, and calculations. Allow model-written text only for whitelisted narrative fields.
8. Produce a decision-complete brief and a generator config. Include:
   - target consumers and exact field mapping;
   - scenario date and fixed or rolling time;
   - archetypes, modules, overlays, and scale;
   - required outputs and persistence behavior;
   - compact LLM context boundaries, if applicable;
   - invariants, privacy rules, tests, and acceptance queries.
9. Hand the approved config to `$generate-horizon-bank-synthetic-data`. Require `$validate-horizon-bank-synthetic-data` before delivery.

## Planning rules

- Keep customer type separate from channel. A youth persona may power web, voice, or wearable experiences.
- Model households, businesses, guardians, accounts, and events explicitly when the experience depends on those relationships.
- Anchor relative dates to one recorded scenario date. Never mix a current date with stale statements, bills, or prompt examples.
- For mutable experiences, define the mutation contract in the consuming project. Keep the bundled fixture server read-only.
- For LLM experiences, send only the task-relevant customer slice and stable entity IDs. Do not paste a full banking relationship into every prompt.
- Never plan to copy production records or generate passwords, PINs, SSNs, routing numbers, full account numbers, or valid full card numbers.

## Completion gate

Finish only when another developer can generate and integrate the data without choosing a schema, date policy, scale, archetype, output format, state model, or validation standard.
