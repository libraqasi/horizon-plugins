# Agentic commerce surfaces

## Surface separation

Use three distinct roles:

1. A neutral shopping assistant plans, searches, explains, and requests approval.
2. The Horizon Trusted Surface handles customer consent, policy, exact approval, bounded authorization, activity, and revocation.
3. Horizon Backstage controls scenarios and exposes deterministic policy, events, protocol evidence, rail behavior, and failures.

Do not visually co-brand a general-purpose assistant with Horizon. The assistant may link to Horizon as an external approval and authorization service.

## Authorization boundary

- The model plans; it never authorizes.
- The Trusted Surface is deterministic and non-agentic.
- The shopping assistant never submits approval decisions.
- Show deterministic policy results separately from model rationale.
- Bind exact approval to the displayed checkout.
- Display bounded future authorization as a separate task-and-constraints experience.
- Keep agent, consent, key, and Agent Account revocation independent.

## Evidence and observability

- Animate only from immutable events; do not infer financial state from UI timers.
- Preserve event order, actor, trust boundary, input/output, state transition, verification result, and trace identifiers.
- Redact secrets before logs or UI.
- Label protocol versions and verification results at their boundary.
- Show failed checks honestly and provide a recovery path.
- Use payment adapters behind one common purchase flow; do not present two unrelated journeys before rail selection.

## Environment language

Normal customer and operator copy should speak directly about Horizon Bank and its products. Use one restrained environment indicator per primary surface. Add precise qualifiers only to simulated merchants, payment credentials, network/processor results, external connectivity, and protocol conformance evidence.

## Layout guidance

- Keep approval actions sticky on narrow phones without obscuring content.
- Keep Backstage swimlanes and event tables dense, exact, and inspectable.
- Show plain-language narrative first, then progressive technical disclosure.
- Preserve at least 70 percent of a presentation stage for the trace when the inspector is open.
