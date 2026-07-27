# Horizon Bank UI review checklist

## 1. Authorization, safety, and trust

- Agent planning and deterministic authorization are visibly separate.
- Only an authenticated Horizon surface can record a customer approval decision.
- Consequential actions show requester, account, merchant, amount, timing, fees, scope, expiration, and consequences.
- Exact approval is bound to the exact checkout; bounded authorization uses distinct language and layout.
- Sensitive values are masked and absent from logs, examples, analytics attributes, and screenshots.
- Success is durable, not toast-only.
- Live connectivity and protocol certification are never implied without evidence.

## 2. Task and responsive behavior

- The primary journey works end to end.
- Navigation names the current location and adapts intentionally on mobile.
- Layout reflows without scrolling, clipping, overlap, or hidden essential content.
- Loading, empty, partial, interrupted, expired, error, and success states exist.
- Long labels, large balances, localization, 200% text scaling, and 400% reflow remain usable.

## 3. Accessibility

- WCAG 2.2 AA is the target.
- One clear page title and logical headings are present.
- Native semantic controls and landmarks are used.
- Labels persist; errors are associated and recoverable.
- Keyboard order matches visual order; focus is visible and not trapped.
- Text, meaningful boundaries, and focus indicators meet contrast targets.
- Color is never the only signal.
- Images, icons, charts, and dynamic status have accessible equivalents.
- Reduced motion, zoom/reflow, orientation, and dynamic type are supported.

## 4. Horizon identity

- The standalone wordmark is used when the bank name should be explicit; the independent HB icon is used only where compact identity is useful.
- No single-H identity or automatically combined icon-and-wordmark lockup appears.
- Only Horizon Bank names, initials, logos, and token prefixes are present.
- Horizon Sans, Horizon Sans Display, the slab-serif wordmark treatment, and IBM Plex Mono roles are consistent.
- White and warm neutral surfaces dominate; red and yellow are purposeful.
- Indigo behaves as a link color, and green status is paired with text or icon.
- Photography is relevant, inclusive, correctly cropped, and accessible.

## 5. Components and data

- Buttons have clear hierarchy and complete interaction states.
- Forms have labels, help, errors, suitable autocomplete/input modes, and preserved values.
- Cards create meaningful groups instead of generic visual clutter.
- Amounts align and distinguish pending, posted, scheduled, failed, reversed, and refunded states.
- Tables, ledgers, timelines, and swimlanes preserve their exact structure.
- Icons reinforce meaning and remain recognizable.

## 6. Engineering quality

- Semantic tokens replace scattered hex values.
- Reusable components share geometry and states.
- SVGs have safe sizing and do not inherit accidental fills.
- Focus, hover, active, disabled, forced-colors, and reduced-motion behavior are testable.
- No raw credential reaches UI, logs, fixtures, or model context.

## Evidence to record

- Screens and breakpoints inspected.
- Source files and line numbers.
- Automated audit results.
- Keyboard path and accessibility checks.
- Contrast calculations.
- Tests not run and evidence not available.
