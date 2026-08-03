# Reference pack

Use the smallest relevant reference set. Too many unrelated images dilute style and content grounding.

## Always available

| Resource | Use |
|---|---|
| `assets/visual-references/identity.png` | Exact relationship between standalone wordmarks, HB icon, and surfaces |
| `assets/visual-references/foundations.png` | Palette, typography, spacing, shape, elevation, and icon treatment |
| `assets/tokens/horizon-tokens.json` | Machine-readable color, type, spacing, radius, shadow, and motion tokens |
| `assets/starter/horizon-tokens.css` | Deterministic CSS tokens and component treatments |
| `assets/starter/horizon-starter-preview.html` | Complete component gallery and renderable reference |

For every high-fidelity image generation, provide `identity.png` and `foundations.png` when the tool accepts image inputs.

## Task-specific visual references

| Visual reference | Attach for |
|---|---|
| `account-overview-desktop.png` | Account dashboard, overview, balance, or quick actions |
| `account-overview-mobile.png` | Responsive-web account overview or narrow-screen balance hierarchy |
| `transfer-review-desktop.png` | Transfer, bill pay, or consequential review at desktop size |
| `transfer-review-mobile.png` | Responsive-web transfer or payment review |
| `agent-approval-desktop.png` | Delegated spending, merchant approval, agentic commerce, or authorization limits |
| `agent-approval-mobile.png` | Responsive-web delegated-spending approval |
| `data-visualization-desktop.png` | Cash flow, spending analysis, category comparison, or forecast |
| `operational-states-desktop.png` | Loading, empty, interruption, and durable success concepts |
| `imagery.png` | Marketing, editorial, planning, goal, or life-event concepts using photography |

Use the desktop and mobile pair when a responsive-web relationship is the question. Otherwise select only the target device plate. These mobile plates are not iOS or Android component specifications. For an exploratory native concept, retain the Horizon identity and financial-safety hierarchy while following the named platform's navigation, controls, typography, and accessibility conventions.

## Exact identity assets

Use files from `assets/logos/` for deterministic layout or post-generation compositing:

- `horizon-bank-wordmark-black.svg`
- `horizon-bank-wordmark-white.svg`
- `horizon-bank-icon.svg`

The `horizon-bank-logo-horizontal*.svg` files are compatibility aliases for the standalone wordmarks. They are not icon-plus-wordmark lockups.

Use `assets/horizon-bank-icon.svg` only for the skill's own UI metadata when needed.

## Production assets

- `assets/fonts/web/` contains Regular, SemiBold, Italic, and Display web fonts.
- `assets/icons/` contains the full reusable banking and utility SVG set. Search filenames by concept before choosing an icon.
- `assets/stock/` contains seven editorial photographs. Use them only when the image adds meaning, not as filler.

Preserve source filenames and aspect ratios. When rendering an SVG icon with HTML/CSS, constrain one axis and leave the other `auto`, or use `max-width`, `max-height`, and `object-fit: contain` inside a bounded area. Do not trace or redraw identity assets from a screenshot when the original SVG is bundled.

## Reference priority

When references conflict, use this order:

1. supplied SVG identity geometry;
2. exact token JSON and CSS values;
3. rendered identity and foundation plates;
4. rendered task-specific plates;
5. written composition guidance;
6. model defaults.

The rendered plates are examples, not immutable page templates. Reuse their visual grammar without copying their information architecture when the new task requires a different structure.

## Tool portability

- For multimodal image tools, attach the relevant PNG plates and exact SVG mark if supported.
- For text-only image tools, translate the plates into the prompt recipe from `generation-recipes.md`.
- For web code-capable agents, render from the token CSS, web font files, SVG assets, and starter HTML.
- For design tools, import the SVG marks and token values directly, then use the plates as a visual calibration layer.
- For agents with no visual output, deliver the completed generation brief, exact copy deck, screen inventory, and ready-to-run prompt.
