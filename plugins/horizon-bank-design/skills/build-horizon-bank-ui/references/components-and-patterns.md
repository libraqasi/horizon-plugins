# Components and patterns

## Global frame

- Use a red masthead with the standalone white Horizon Bank wordmark and a thin yellow bottom rule. Add the HB icon only when the surface independently needs a compact mark.
- Keep product or section identity in text beneath or beside the bank name.
- Put utility actions at the trailing edge.
- Collapse navigation intentionally on mobile; preserve the primary task and current location.
- Provide a skip link, landmarks, meaningful labels, and keyboard-complete menus.

## Buttons

- Primary: red fill, white SemiBold label, minimum practical height of 44 pixels.
- Secondary: white or warm surface, dark label, visible control border.
- Tertiary: text or icon-and-text with a clear hit area; use indigo for links.
- Name the outcome: “Approve once,” “Freeze account,” or “Pay $125.00.” Avoid “Submit” when a specific result is available.
- Keep hover, active, focus, disabled, loading, and destructive states explicit.
- Separate a card’s final action row from descriptive text, data rows, and dividers with at least 1.5rem of block space. Do not rely on the preceding element’s padding to create this boundary.
- In the web starter, group card actions with `.horizon-actions.horizon-card-actions`. The modifier owns a 1.5rem content-to-action gap. Inside `.horizon-stack`, its 0.5rem margin combines with the stack’s 1rem gap to preserve the same 1.5rem boundary without doubling it.

## Forms

- Keep persistent labels. Placeholder text never replaces a label.
- Group related information and preserve logical reading and tab order.
- Associate errors programmatically, explain recovery, and preserve entered values.
- Use appropriate input modes, autocomplete tokens, masking, and reveal-state labels.
- Implement a binary switch as a labeled checkbox with `role="switch"` so its checked state remains native and keyboard operable.
- Scope generic checkbox and radio sizing with `input:not(.horizon-switch)`. A broad selector such as `.horizon-check input` can override the switch track because it is more specific than `.horizon-switch`.
- Give the switch track an explicit width, matching `min-width`, height, zero padding, `flex: 0 0 auto`, and both `-webkit-appearance: none` and `appearance: none`. Verify its knob at the checked and unchecked positions instead of relying on the browser’s default checkbox rendering.
- Review consequential actions before commitment. Show the exact source, destination, amount, fees, timing, authority, and expiration.

## Cards and surfaces

- Use cards for meaningful grouping, not as the default wrapper for every sentence.
- Prefer white or quiet surfaces with subtle borders and restrained elevation.
- Align repeated cards to a shared grid.
- Keep repeated card actions aligned predictably, but let content determine card height on narrow screens. Action placement must not crowd the final data row or create a large unusable void.
- Treat a product caption and its primary amount as one summary cluster. In the web starter, wrap them in `.horizon-product-summary`; its tight internal gap preserves hierarchy and its 0.75rem trailing space keeps the amount from touching a progress bar or detail row.
- Leave at least 0.5rem between a progress bar and the next detail row. Amounts, supporting visualizations, dividers, and actions must never appear as one undifferentiated block.
- Make the whole card clickable only when it has one destination and clear semantics.
- Keep icon canvases transparent. Use the bundled dark monochrome icons directly on light surfaces and the starter’s `.horizon-icon-inverse` treatment when an `<img>` sits on red or dark surfaces. Make any backing tile part of the surrounding component rather than baking a white rectangle into the SVG.
- Preserve the intrinsic proportions of every icon. For `<img>` icons, set only width or height and leave the other dimension `auto`; when a shared visual area needs both bounds, use `max-width`, `max-height`, and `object-fit: contain`. Do not apply the same fixed width and height to non-square SVGs, because wider support, mobility, and payment artwork will be squeezed.

## Accounts, approvals, and transactions

- Show account name, masked identifier, balance label, amount, and status in an unambiguous hierarchy.
- Distinguish pending, posted, scheduled, failed, canceled, reversed, and refunded states.
- Right-align comparable amounts and use tabular numerals.
- Bind exact approval UI to the specific merchant, items, landed cost, delivery, expiration, and checkout identity.
- Keep exact-purchase approval visually distinct from bounded future authorization.
- Keep freeze, revoke agent, revoke consent, rotate key, and close account as independent controls.

## Alerts and feedback

- Use an icon, concise heading, explanatory text, and recovery action.
- Do not use red as generic decoration or green as the only success signal.
- Announce dynamic status without repeatedly interrupting assistive technology.
- Never use a transient toast as the only record of a financial action; provide durable confirmation.

## Data and protocol visualization

- Preserve tables, timelines, ledgers, and swimlanes when they carry exact structure. Do not turn them into generic card grids.
- Keep actor lanes, nodes, connectors, and trust boundaries in one coordinate system.
- Pair color with text, shape, icon, or line style.
- Provide exact values, accessible summaries, and redacted structured detail on demand.
- Never render raw credentials or secrets.

## Responsive behavior

- Reflow rather than shrink.
- Test at 320, 390, 768, 1024, and 1280+ CSS pixels unless the product defines other targets.
- Preserve the primary task, identity, critical status, and safe action order.
- Support 200% text scaling and browser reflow at 400% where applicable.
- Keep sticky approval actions visible without covering content.
- Keep dialogs within the viewport and return focus to the trigger.
