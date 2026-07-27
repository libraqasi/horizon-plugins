# Horizon visual direction
Use this reference to translate an idea into a recognizable Horizon Bank visual without turning every frame into a brand poster.

## Brand signature

Horizon should feel established, calm, direct, and capable. Lead with the customer's money, decision, or next action. Use generous neutral space and a confident red frame. Let exact information carry the design.

The formal wordmark and compact HB icon are independent:

- Use `assets/logos/horizon-bank-wordmark-black.svg` on light surfaces.
- Use `assets/logos/horizon-bank-wordmark-white.svg` on red or dark surfaces.
- Use `assets/logos/horizon-bank-icon.svg` for constrained surfaces where the bank identity is already clear.
- Never pair the icon and wordmark by default, replace HB with H, or ask an image model to invent a new mark.

## Color roles

| Role | Value | Visual use |
|---|---:|---|
| Brand primary | `#D71E28` | Masthead, primary action, selected state, limited emphasis |
| Primary hover | `#B01B24` | Interactive red state |
| Brand rule | `#FFCD41` | Thin rule and sparing punctuation |
| Page | `#FFFFFF` | Primary canvas |
| Warm canvas | `#F4F0ED` | Page or section background |
| Quiet surface | `#F9F7F6` | Cards and inset regions |
| Primary ink | `#141414` | Text and monochrome icons |
| Muted text | `#675F5F` | Supporting content |
| Subtle border | `#E2DEDE` | Grouping and dividers |
| Control border | `#787070` | Inputs and meaningful boundaries |
| Link indigo | `#5A469B` | Conventional links and informative accents |
| Positive green | `#178757` | Positive state with visible label or icon |
| Warning | `#A93E00` | Warning state with visible label or icon |
| Fault | `#87190A` | Fault state with visible label or icon |

Do not let red cover every surface. Do not use green as the only success signal. Secondary chart colors may use the supplied orange, coral, pink, purple, violet, and indigo families, but avoid rainbow dashboards.

## Typography

- Use Horizon Sans Display at regular weight for brief page titles, section headings, hero statements, and large financial summaries.
- Use Horizon Sans Regular for body copy, navigation, labels, descriptions, and values.
- Use Horizon Sans SemiBold for controls, tabs, compact headings, and emphasis.
- Use sentence case. Avoid all caps except the supplied uppercase wordmark.
- Use tabular numerals for aligned finance data when supported.
- Use monospace only for identifiers, event traces, or developer evidence.

When a raster model cannot reproduce Horizon Sans, favor a humanist sans with similar open forms and repair the final artifact through deterministic rendering when type fidelity matters.

## Composition

- Start with the primary job or financial state, not a greeting or decorative chart.
- Keep task content left aligned and group labels closely with their values.
- Use white and warm neutral fields. Prefer subtle borders and surface changes before shadows.
- Use 6.4 px control radii, 12 px card radii, and pills only for compact controls or statuses.
- Follow an 8 px rhythm with common gaps of 8, 16, 24, and 32 px.
- Use cards only for meaningful grouping. Preserve tables, ledgers, timelines, comparisons, and review summaries when their structure matters.
- Keep one visually dominant primary action. Name the outcome, such as “Review transfer,” “Approve once,” or “Freeze account.”
- Use bundled line icons to reinforce visible labels. Do not use oversized decorative finance glyphs.

## Banking patterns

### Accounts and activity

Show the account name, masked identifier, balance label, amount, and status in a clear hierarchy. Distinguish current and available balance. Align comparable amounts and label pending, posted, scheduled, failed, canceled, reversed, and refunded states.

### Transfer or payment review

Show source, destination, amount, fee, total, timing, and ability to edit before commitment. Separate the action area from the summary. Provide durable confirmation after commitment.

### Approvals and delegated spending

Keep the agent's proposal visually separate from the bank's authorization boundary. Show requester, merchant, item or purpose, exact landed cost, delivery, limit, expiration, approval scope, and revocation path.

### Data visualization

Favor labeled bars, comparisons, tables, or forecasts with exact values. Pair color with text or shape. Do not use an unlabeled donut chart as the main explanation.

### Operational states

Design loading, empty, partial, validation error, system error, offline/interrupted, durable success, expired session, and safe re-entry as part of the concept.

## Low-fidelity treatment

Retain the Horizon information hierarchy while removing finish:

- warm-white canvas, gray strokes, and neutral placeholder blocks;
- one restrained red primary-action or annotation color;
- real labels and plausible synthetic data;
- no photography, shadow, detailed icons, or decorative backgrounds;
- annotations that explain the interaction or hypothesis being tested.

Low fidelity should look intentionally unfinished, not like a broken high-fidelity screen.

## Avoid

- another financial institution's identity, fonts, layouts, or customer data;
- generic fintech gradients, glassmorphism, neon purple, or floating 3D cards;
- a dashboard made entirely of equally weighted cards;
- fake phone photography, hands holding devices, browser chrome, or perspective views unless the user requests a presentation scene;
- decorative stock photography that displaces a financial task;
- illegible generated text, nonsense currency, duplicated controls, or contradictory status;
- urgency, shame, or celebration that obscures financial consequence.
