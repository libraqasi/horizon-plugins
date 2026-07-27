# Brand foundations

## Identity

Horizon Bank is the customer-facing bank identity. Use `Horizon Bank`, `Horizon`, `HB`, and product names such as `Horizon Agent Account` without qualification in ordinary interface copy.

Use the standalone Horizon Bank wordmark when the bank name should be explicit. Use the independent HB mark for compact identity, and never shorten it to a single H. Neither asset requires the other.

Keep an independent shopping assistant visually separate from Horizon. The bank may appear as a named connected service, approval destination, or deterministic authorization boundary without co-branding the assistant shell.

## Color roles

Use semantic roles instead of raw palette names in product code.

| Role | Token | Value | Guidance |
|---|---|---:|---|
| Brand primary | `brand.primary` | `#D71E28` | Masthead, primary action, selection, limited emphasis |
| Brand primary hover | `brand.primaryHover` | `#B01B24` | Interactive red state |
| Brand rule | `brand.rule` | `#FFCD41` | Thin rule and sparing punctuation |
| Page | `surface.page` | `#FFFFFF` | Primary canvas |
| Warm canvas | `surface.warm` | `#F4F0ED` | Page and section background |
| Quiet surface | `surface.quiet` | `#F9F7F6` | Cards and inset regions |
| Text | `text.primary` | `#141414` | Default text and icon color |
| Muted text | `text.muted` | `#675F5F` | Supporting copy; verify size and contrast |
| Subtle border | `border.subtle` | `#E2DEDE` | Grouping and dividers |
| Control border | `border.control` | `#787070` | Inputs and meaningful boundaries |
| Link | `action.link` | `#5A469B` | Conventional inline links |
| Positive | `status.positive` | `#178757` | Positive state paired with text/icon |
| Warning | `status.warning` | `#A93E00` | Warning state paired with text/icon |
| Fault | `status.fault` | `#87190A` | Fault state paired with text/icon |

Use white plus black as the default focus treatment across mixed surfaces. Do not use color as the only signal.

Secondary orange, coral, pink, purple, violet, and indigo families support charts and illustration. Avoid rainbow screens.

## Typography

- Use the bundled Horizon Sans family for digital UI.
- Use Horizon Sans Display at regular weight for brief page titles, section headings, hero statements, and large account summaries.
- Use Regular for body, labels, descriptions, navigation, and values.
- Use SemiBold for buttons, tabs, active navigation, compact headings, and emphasis.
- Do not synthesize bold or italic. Use only the supplied Regular, SemiBold, Italic, and Display faces.
- Use IBM Plex Mono only for identifiers, protocol payloads, hashes, and developer evidence.
- Use sentence case. Avoid all caps for ordinary controls and prose.
- Use tabular numerals for aligned financial values when supported.

Recommended ramp:

| Token | Size | Line height | Typical use |
|---|---:|---:|---|
| Display XL | `clamp(2.25rem, 4vw, 3.5rem)` | 1.08 | Marketing hero |
| Display L | `clamp(2rem, 3vw, 2.75rem)` | 1.12 | Page title |
| Display M | `clamp(1.75rem, 2.4vw, 2.125rem)` | 1.2 | Section title |
| Heading S | `1.5rem` | 1.25 | Flow or card heading |
| Body L | `1.125rem` | 1.5 | Introductory copy |
| Body | `1rem` | 1.5 | Default UI |
| Body S | `0.875rem` | 1.45 | Supporting copy |
| Legal | `0.75rem` | 1.5 | Required disclosure |

## Composition

- Use a confident red brand frame and generous neutral field.
- Use the thin yellow rule as punctuation, not decoration.
- Keep task content left aligned.
- Prefer borders and surface contrast before shadow.
- Use moderate card radii and pill-shaped compact actions consistently.
- Use authentic, inclusive photography only when it supports the content.
- Avoid ornamental gradients, glass effects, decorative dashboards, and generic card grids that obscure information structure.

## Logo

The primary Horizon Bank identity is a standalone, uppercase slab-serif wordmark with a subtly reinforced regular weight. Its stroke density should visually align with the supplied reference identity without becoming a bold display face. The black and white SVGs use vector paths, so their formal appearance does not depend on an installed font. Preserve their geometry, aspect ratio, clear space, and fill color.

Treat the HB tile as a separate compact icon. It does not include the bank name and does not need to sit beside the wordmark. Use it for app icons, avatars, favicons, small navigation surfaces, or other constrained placements where the bank name is already clear.

When a layout needs editable text instead of the formal SVG, typeset `Horizon Bank` with the `--horizon-font-wordmark` stack at regular weight and the starter’s subtle same-color reinforcement. Use the bundled Horizon Sans family for all ordinary interface copy.

Do not build a permanent lockup by automatically placing the HB icon beside the wordmark. Do not recolor, distort, crop, outline, animate, or decorate either asset. Provide a meaningful text alternative unless adjacent text already names the bank.
