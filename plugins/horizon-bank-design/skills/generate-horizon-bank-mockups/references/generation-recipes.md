# Generation recipes

## Contents

1. Build the prompt contract
2. Choose an artifact form
3. Generate low-fidelity wireframes
4. Generate high-fidelity product screens
5. Generate a responsive screen set
6. Edit an existing concept
7. Create alternatives
8. Use a deterministic render
9. Repair common failures

## Build the prompt contract

Give the rendering model a complete visual contract in this order:

1. **Artifact**: UI mockup, wireframe, storyboard, responsive comparison, or design board.
2. **Frame**: device, orientation, dimensions or aspect ratio, and whether the UI is isolated or shown in context.
3. **Primary job**: the one task or decision the screen must make obvious.
4. **Information architecture**: regions and their relative priority.
5. **Exact content**: labels, values, dates, states, and synthetic data that must appear.
6. **Horizon treatment**: identity, palette, typography, spacing, components, and relevant reference plates.
7. **State**: loading, empty, error, review, success, interrupted, or another consequential state.
8. **Exclusions**: visual cliches, unsafe data, false product claims, and elements the model must not add.
9. **Output requirement**: isolated orthographic UI, readable text, no device perspective or surrounding scene unless requested.

Do not rely on adjectives such as “modern,” “premium,” or “clean” without specifying the information structure and exact Horizon treatment.
Tell the model not to add policy, legal, fee, rate, timing, cancellation, eligibility, partner, network, or disclosure copy that was not supplied. Empty space is safer than invented product behavior.

## Choose an artifact form

| Need | Preferred form |
|---|---|
| Explore layout quickly | Low-fidelity HTML/SVG wireframe or raster concept |
| Validate visual direction | High-fidelity raster image with reference plates |
| Validate exact copy and financial data | HTML/CSS or SVG render |
| Compare desktop and mobile | Two isolated frames or one clearly separated comparison board |
| Explain a journey | Three-to-five frame storyboard with stable shell |
| Present an idea to stakeholders | Annotated concept board with one primary screen and focused callouts |
| Iterate an existing screen | Image edit using the current screen plus Horizon references |

## Generate low-fidelity wireframes

Use this structure:

```text
Create a low-fidelity [device] wireframe for Horizon Bank.

Concept: [one-sentence idea]
Customer job: [task]
Frame: [dimensions or aspect ratio], isolated flat UI, no device mockup
Structure:
- [region 1 and purpose]
- [region 2 and purpose]
- [primary action]
- [supporting/recovery action]
Exact labels and synthetic data:
- [copy]
State to show: [state]

Visual treatment:
- warm-white canvas, grayscale blocks and 1 px neutral strokes
- restrained Horizon red only for the primary action or annotations
- 8 px spacing rhythm, left-aligned content, real labels, no lorem ipsum
- intentionally unfinished; no photography, gradients, glass, shadow, or decorative icons

Make task order and hierarchy obvious at thumbnail size. Keep every label legible.
```

When testing several structures, vary navigation, sequencing, or information grouping. Do not merely change colors.

## Generate high-fidelity product screens

Attach `identity.png`, `foundations.png`, and the closest task-specific plate, then use:

```text
Create a high-fidelity Horizon Bank [device] UI mockup for [concept].

Primary customer job: [task]
Frame: [dimensions or aspect ratio], isolated orthographic UI screenshot, no hands,
device hardware, browser chrome, perspective, or presentation background.

Information hierarchy:
1. [highest-value information or decision]
2. [supporting detail]
3. [primary action]
4. [secondary/recovery action]

Exact copy and synthetic values:
- [heading]
- [labels, amounts, dates, masked identifiers, statuses]
- [button labels]

Use the provided Horizon references as visual ground truth:
- standalone Horizon Bank wordmark when the bank name must be explicit
- red #D71E28 brand frame or primary action with a thin #FFCD41 rule
- white and #F4F0ED fields, #141414 ink, #5A469B links
- Horizon Sans Display-style concise headings and Horizon Sans-style UI copy
- subtle borders, 6.4 px controls, 12 px cards, restrained elevation, 8 px rhythm
- outcome-specific actions and visible status labels

Do not invent another logo, combine the HB icon with the wordmark, use gradients or
glass effects, turn every region into a card, fabricate live product claims, or include
real customer information. Do not add explanatory, policy, legal, fee, timing,
cancellation, eligibility, partner, network, or disclosure copy not supplied above.
Leave space empty rather than inventing product behavior. Render all text and currency
once, correctly, and legibly.
```

After generation, overlay the exact SVG wordmark or rerender deterministically if the mark, labels, or amounts are wrong.

## Generate a responsive screen set

Create desktop and mobile as separate frames or a clearly separated board. Use a desktop/mobile reference pair.

Keep constant:

- product and account data;
- page title and primary task;
- component visual language;
- action wording and status semantics;
- identity treatment.

Change intentionally:

- desktop side-by-side summaries become stacked mobile regions;
- tables become labeled rows or progressive disclosure;
- navigation collapses while preserving current location;
- primary actions may become full-width or sticky without covering content;
- secondary information moves below the task rather than shrinking.

Do not create a miniature desktop screen inside a phone.

## Edit an existing concept

Provide the current artifact as the first reference and Horizon identity/foundations after it.

State:

1. what must remain unchanged;
2. the exact regions to restyle or restructure;
3. the Horizon tokens and pattern to apply;
4. the text, amounts, and logo geometry that must remain exact;
5. the failure to remove.

Prefer localized edits over full regeneration when the structure already works.

## Create alternatives

Generate two or three directions only when each tests a distinct hypothesis:

- **Task-first**: lead with the next safe action.
- **Balance-first**: lead with financial position and trends.
- **Guided**: use progressive disclosure and explanatory review.
- **Evidence-first**: lead with authorization scope, event trace, or comparison.

Label the hypothesis outside the UI or in delivery notes, not as interface copy. Keep the Horizon identity stable so the comparison is about product structure.

## Use a deterministic render

Use `assets/starter/horizon-tokens.css` and bundled assets when exactness outweighs rapid image exploration.

1. Copy only the needed token, font, logo, icon, and stock assets.
2. Build semantic HTML or SVG at the target canvas size.
3. Reuse classes or visual treatments from `horizon-starter-preview.html`.
4. Populate exact synthetic data and required states.
5. Render at target desktop and mobile dimensions.
6. Inspect the screenshots and revise before delivery.

Use this route for dense content, a handoff-ready mockup, or a screen set that must remain visually consistent.

## Repair common failures

| Failure | Repair |
|---|---|
| Misspelled or redrawn wordmark | Remove it and composite the supplied SVG |
| Garbled text or currency | Local edit if supported; otherwise use HTML/SVG |
| Generic fintech look | Reattach identity and foundations; specify red frame, yellow rule, warm field, indigo links, and prohibited effects |
| Too many cards | Restore task-specific regions, table, ledger, timeline, or review summary |
| Mobile looks shrunken | Request reflow, stacking, full-width actions, and simplified navigation |
| Status depends on color | Add a visible label and icon or shape |
| Consequential action lacks context | Add requester, source, destination, amount, fees, timing, scope, expiration, and edit/cancel path |
| Different screens drift | Reuse the same references, seed, content model, frame, and unchanged shell |
| UI appears inside a glossy device scene | Request an isolated orthographic interface frame |
| Prototype implies live behavior | Add one precise environment label and remove unsupported connectivity or certification claims |
| Model invents policy or disclosure copy | Remove it through a targeted edit; never treat plausible generated prose as approved product behavior |
