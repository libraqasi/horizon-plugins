---
name: build-horizon-bank-ui
description: Design, implement, or refactor modern Horizon Bank web interfaces and guide native mobile UI using the standalone Horizon wordmark, optional HB icon, bundled Horizon Sans fonts, semantic tokens, accessible financial patterns, reusable SVG icons, stock photography, and agentic-commerce trust boundaries. Use for Horizon dashboards, customer banking flows, public pages, prototypes, design systems, React/HTML/CSS work, mobile concepts, or requests to create future Horizon Bank elements.
---

# Build Horizon Bank UI

Create a credible bank experience that feels established, calm, and task-focused. Treat Horizon Bank as the product identity in ordinary UI copy.

## Required workflow

1. Inspect the existing framework, screen set, journey, and design tokens before changing code.
2. Read [brand-foundations.md](references/brand-foundations.md) for every task.
3. Read [components-and-patterns.md](references/components-and-patterns.md) when creating or changing UI components or flows.
4. Read [accessibility-and-content.md](references/accessibility-and-content.md) for every customer-facing experience.
5. Read [asset-catalog.md](references/asset-catalog.md) before selecting identity marks, icons, or photography.
6. Read [agentic-commerce-surfaces.md](references/agentic-commerce-surfaces.md) for delegated spending, approval, agent, protocol, or observability work.
7. Establish semantic tokens before styling components. For web work, start from `assets/starter/horizon-tokens.css` and inspect `assets/starter/horizon-starter-preview.html`.
8. Build the smallest coherent end-to-end flow, including loading, empty, error, interrupted, and durable success states.
9. Run `python3 scripts/audit_horizon_ui.py <source-path> --strict`. Review findings and confirm eligible files were scanned.
10. Inspect the rendered result at representative desktop and mobile sizes. Verify keyboard access, zoom/reflow, contrast, reduced motion, hierarchy, and clipping.

## Identity rules

- Treat the standalone Horizon Bank wordmark and the HB icon as independent assets. Use the wordmark when the bank name should be explicit and the HB icon when compact identity is useful. Never substitute a single `H` or require the icon beside the wordmark.
- Use only Horizon Bank names, initials, marks, filenames, selector prefixes, and code comments in generated work.
- Keep the red masthead, thin yellow rule, warm neutral field, indigo links, and restrained green status treatment recognizable without saturating every surface.
- Use the bundled Horizon Sans family for digital UI and Horizon Sans Display for brief page and section headings. Use IBM Plex Mono only for protocol payloads, identifiers, and developer evidence.
- Preserve the supplied logo geometry, aspect ratio, colors, and safe space. Do not redraw, recolor, distort, crop, outline, or animate it.
- Use the bundled SVG icons when they fit; use icons to reinforce a visible label rather than replace one by default. Their canvases are transparent and their artwork is dark monochrome: use them directly on light surfaces and apply the starter’s inverse treatment on red or dark surfaces.

## Product truth without repetitive disclaimers

- Write normal Horizon UI as a real bank product: “Horizon Bank,” “Horizon Agent Account,” “Approve once,” and “Freeze account.”
- Do not repeatedly call the bank, components, screens, accounts, or ordinary interactions fake, mock, synthetic, or demo.
- Preserve truth at the boundary where it changes user understanding: environment status, simulated merchant/payment/network data, emulated protocol behavior, test credentials, and unsupported compliance claims.
- Prefer one restrained environment disclosure per primary surface and precise labels in evidence views. Do not attach a disclaimer badge to every component.
- Never imply live funds movement, live issuer/network connectivity, or protocol certification when it is not present.

## Core design direction

- Lead with clarity, trust, task completion, and visible control.
- Use white and warm neutral surfaces as the field. Reserve red for mastheads, primary actions, selection, and high-value emphasis.
- Use the yellow rule sparingly as brand punctuation.
- Prefer sentence case, direct labels, left-aligned task content, restrained elevation, and consistent geometry.
- Keep financial data scannable: align money, show dates and status, distinguish pending from posted, and never use color alone.
- Keep consequential actions deterministic and reviewable. Show who requested the action, exact scope, amount, merchant, timing, expiration, and revocation path.
- Keep agent planning visually and functionally separate from bank authorization.

## Bundled resources

- `assets/logos/`: Horizon Bank SVG identity family.
- `assets/icons/`: reusable 60-file banking and utility SVG library.
- `assets/stock/`: seven supplied editorial photographs for relevant product storytelling.
- `assets/tokens/horizon-tokens.json`: portable Horizon token map.
- `assets/starter/horizon-tokens.css`: web starter with semantic tokens and common components.
- `assets/starter/horizon-starter-preview.html`: accessible component-gallery markup.
- `scripts/audit_horizon_ui.py`: palette, identity, and common accessibility preflight.

Copy only the assets the product needs. Keep source filenames where practical and record transformed asset provenance.

## Completion gate

Deliver only after the primary journey works, the HB identity is correct, responsive structure is intentional, native semantics are used, WCAG 2.2 AA is the target, keyboard and screen-reader names are meaningful, consequential states are durable, protocol/payment boundaries remain truthful, and the rendered UI has been visually reviewed.
