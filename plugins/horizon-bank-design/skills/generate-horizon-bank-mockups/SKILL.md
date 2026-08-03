---
name: generate-horizon-bank-mockups
description: Create and iterate visual Horizon Bank web UI/UX mockups, concept screens, wireframes, responsive-web screen sets, journey storyboards, and design explorations at low or high fidelity. Use when an agent needs to turn a banking idea, product flow, feature brief, rough sketch, or existing screen into Horizon-aligned prototype images or other visual artifacts before implementation, including with image-generation, image-editing, HTML/SVG rendering, design, or multimodal tools. Native concepts are exploratory and must follow their target platform's conventions.
---

# Generate Horizon Bank Mockups

Create visual artifacts for learning and decision-making before implementation. Ground every result in the bundled Horizon identity, design tokens, patterns, and rendered references.

The bundled task plates, token CSS, starter HTML, and deterministic component examples are web and responsive-web references. They may inform an exploratory native or cross-platform concept, but do not present them as authoritative native navigation, controls, typography, or accessibility patterns. Identify the target platform in the brief and disclose any platform-specific fidelity gaps.

## Required workflow

1. Define the concept: user, primary job, entry point, critical decision, success state, target device, fidelity, and output format.
2. Infer safe defaults when details are missing. Unless the request implies otherwise, produce a high-fidelity primary screen at the requested device size plus one consequential or recovery state.
3. Read [visual-direction.md](references/visual-direction.md) and [reference-pack.md](references/reference-pack.md) for every task.
4. Read [generation-recipes.md](references/generation-recipes.md) before using image generation, image editing, or a prompt-only workflow.
5. Choose the rendering route:
   - Use image generation or editing for rapid visual exploration, alternative directions, editorial concepts, and early product frames.
   - Use HTML/CSS or SVG rendering when exact copy, financial values, the formal wordmark, component geometry, or responsive behavior must be trustworthy.
   - Produce a ready-to-run visual brief and prompt only when no rendering tool is available or the user asks for a prompt.
6. Select the smallest relevant set of bundled visual references. Supply them to the rendering model when the tool accepts image inputs.
7. Create the smallest coherent screen set that can validate the idea. Include the state before an important action, the decision itself, and durable feedback when the concept involves money, authorization, privacy, or access.
8. Inspect the rendered output against [quality-gate.md](references/quality-gate.md). Iterate on specific failures rather than regenerating without direction.
9. Deliver the visual artifact, state the assumptions that materially shaped it, and name any unresolved text, logo, accessibility, or product-truth limitations.

## Choose fidelity deliberately

### Low fidelity

- Focus on information architecture, task order, content hierarchy, and component placement.
- Use grayscale, white, and warm neutral blocks with restrained Horizon red annotations or primary-action emphasis.
- Use real interface labels and plausible synthetic data; do not use lorem ipsum.
- Keep decoration, photography, shadow, and micro-polish out of the frame.
- Prefer HTML/SVG wireframes when legibility matters. Image generation is acceptable for fast layout exploration.

### High fidelity

- Attach `assets/visual-references/identity.png`, `foundations.png`, and one or two task-specific reference plates to an image-capable tool.
- Use exact Horizon tokens, bundled fonts, supplied logos, icons, and stock imagery.
- Show a credible responsive frame rather than a generic floating card collection.
- Composite the supplied SVG wordmark after generation when the image model distorts it. Never accept a redrawn or misspelled Horizon Bank mark.
- Preserve exact labels, amounts, dates, masked identifiers, and action outcomes. Render with HTML/SVG when the image model cannot.
- Do not let a model fill open space with invented policy, legal, fee, timing, cancellation, network, partner, or eligibility copy.

## Use visual tools

When an image-generation or image-editing tool is available and the user requested a visual, call it. Do not stop at a prose prompt unless the user asked only for instructions.

Treat generated raster UI as an exploration medium, not automatically as exact UI evidence. Use a deterministic render or post-generation compositing for:

- the Horizon Bank wordmark or HB icon;
- dense tables and transaction histories;
- precise money, dates, identifiers, disclosures, or authorization scope;
- multiple screens that must retain identical navigation and component geometry;
- accessibility claims that depend on measurable contrast, size, or focus order.

For a multi-screen journey, preserve a single design seed or reference set, canvas ratio, content model, navigation frame, and token recipe across every generation. Change only the state or task content.

## Preserve Horizon identity

- Use the standalone Horizon Bank wordmark when the bank name should be explicit and the independent HB icon only when compact identity is useful.
- Never create a permanent icon-plus-wordmark lockup, substitute a single `H`, or redraw, recolor, crop, outline, or decorate the supplied marks.
- Keep the recognizable red masthead or primary frame, thin yellow rule, warm neutral field, dark ink, indigo links, and restrained green status treatment.
- Use Horizon Sans Display for concise headings and Horizon Sans for interface copy.
- Prefer borders and surface contrast before shadow. Avoid ornamental gradients, glass effects, neon treatments, excessive rounding, and decorative dashboards.
- Use plain sentence-case language, left-aligned task content, visible labels, and outcome-specific actions.
- Keep independent agents, merchants, and third parties visually separate from Horizon Bank.

## Protect product truth

- Use synthetic people, accounts, merchants, dates, and amounts. Never place real customer data, full account numbers, credentials, or authentication codes in a mockup.
- Treat Horizon Bank as the product identity in ordinary UI copy without repeating “mock,” “fake,” or “demo.”
- Add one restrained environment label only where it changes user understanding.
- Never imply live funds movement, live issuer or network connectivity, protocol certification, guaranteed rates, or approved legal/compliance language without evidence.
- Show requester, source, destination, amount, fees, timing, scope, expiration, consequence, and reversal path before consequential authorization.

## Iterate with evidence

After each render:

1. Compare the artifact to the exact reference plates and tokens.
2. Check the primary task at a glance, then inspect every label and financial value.
3. Remove any unrequested copy or product behavior, especially policy and disclosure language.
4. Identify the three highest-impact mismatches.
5. Edit or regenerate only those mismatches while preserving what already works.
6. Recheck at target size and as a thumbnail.

Do not present several nearly identical outputs as meaningful alternatives. Vary information architecture, interaction model, or emphasis, and explain what each direction is meant to test.

## Bundled resources

- `assets/visual-references/`: rendered identity, foundation, desktop-web, and responsive-web mobile grounding images for multimodal tools.
- `assets/logos/`: formal standalone wordmarks and independent HB icon for exact placement or compositing.
- `assets/fonts/web/`: Horizon Sans digital font family.
- `assets/icons/`: reusable banking and utility SVGs.
- `assets/stock/`: curated editorial photography for relevant product stories.
- `assets/tokens/horizon-tokens.json`: machine-readable, web-oriented design-token reference; translate web units and interaction states for other platforms.
- `assets/starter/horizon-tokens.css`: deterministic web styling and components.
- `assets/starter/horizon-starter-preview.html`: complete rendered component reference and HTML starting point.

If the concept becomes an implemented interactive product, continue with `$build-horizon-bank-ui` when available. Use `$audit-horizon-bank-ui` for a review-only request.
