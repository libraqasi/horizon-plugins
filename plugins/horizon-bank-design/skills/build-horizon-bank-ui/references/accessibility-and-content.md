# Accessibility and content

## Baseline

Target WCAG 2.2 AA for new work.

- Use one clear page title and a logical heading hierarchy.
- Prefer native buttons, links, inputs, lists, tables, dialogs, and landmarks.
- Give every control an accessible name that describes its outcome.
- Align DOM, visual, reading, and focus order.
- Keep every task operable by keyboard.
- Provide visible focus with at least 3:1 contrast against adjacent colors.
- Meet 4.5:1 for normal text, 3:1 for large text, and 3:1 for meaningful UI boundaries.
- Give informative images alt text and decorative images an empty alt.
- Honor reduced motion, orientation, text resizing, dynamic type, and zoom.
- Do not disable pinch zoom or depend on hover.

## Financial and authorization safety

- Make the requester, account, merchant, amount, timing, fees, scope, expiration, and consequences visible before commitment.
- Distinguish “save,” “review,” “approve,” “schedule,” and “complete.”
- Keep cancellation and correction available until an action is genuinely irreversible.
- Use neutral, factual warnings. Never shame, rush, or surprise the customer.
- Do not place secrets, full account numbers, credentials, authentication codes, or real customer data in examples.
- Keep agent-generated plans as proposals. Only deterministic bank controls and authenticated customer decisions may authorize.

## Voice

Use direct, respectful, plain language in sentence case.

Prefer:

- “Review your purchase”
- “Approve once”
- “We couldn’t authorize this payment”
- “Available balance”
- “Freeze account”
- “Try again or choose another account”

Avoid all caps, “Oops!”, “Invalid input,” “Click here,” vague CTA labels, and marketing claims inside error recovery.

Explain:

1. What happened.
2. What it affects.
3. What the customer can do next.

## Product truth

Treat Horizon Bank as the bank identity without repetitive prototype qualifiers. Add a restrained environment label only where necessary. Label simulated or emulated behavior precisely at merchant, credential, payment, network, protocol, and evidence boundaries. Do not imply live connectivity or certification.

## State coverage

Define loading, empty, partial, delayed, validation error, system error, offline/interrupted, durable success, expired session, and safe re-entry. Test long names, large amounts, localization, and screen-reader-only labels.
