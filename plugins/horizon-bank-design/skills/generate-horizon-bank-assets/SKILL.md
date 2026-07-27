---
name: generate-horizon-bank-assets
description: Generate, edit, and deliver Horizon Bank visual assets that align with the bundled editorial photography and monochrome SVG icon system. Use for Horizon lifestyle or hero photography, campaign and article imagery, image edits, supporting raster assets, transparent cutouts, new banking or utility icons, and requests to make imagery or iconography feel consistent with Horizon Bank. Work from bundled references by default; requester-provided examples are optional. Do not use to redesign Horizon logos, wordmarks, payment-card identity, or complete UI screens.
---

# Generate Horizon Bank Assets

Create useful, credible visual assets without inventing a second Horizon visual language. Treat the existing photographs and icons as the canonical alignment set.

## Required workflow

1. Inspect the intended placement, surrounding layout, dimensions, crop, subject, audience, output format, and whether the result is exploratory or project-bound.
2. Read [photography-and-iconography.md](references/photography-and-iconography.md) for every task.
3. Read [prompt-recipes-and-qa.md](references/prompt-recipes-and-qa.md) before generating, editing, or validating an asset.
4. Read the sibling build skill's [brand foundations](../build-horizon-bank-ui/references/brand-foundations.md), [asset catalog](../build-horizon-bank-ui/references/asset-catalog.md), and [source boundaries](../build-horizon-bank-ui/references/source-boundaries.md) for every task.
5. Optionally invite the requester to attach examples when they have a particular composition, subject, or style in mind. State that examples are optional and never require them for ordinary Horizon work; the bundled references are sufficient.
6. Search the existing [stock photography](../build-horizon-bank-ui/assets/stock/) and [icon library](../build-horizon-bank-ui/assets/icons/) before creating anything. Reuse an existing asset when it already fits.
7. Select only the most relevant two to four references. Label every input as a style reference, composition reference, edit target, or supporting input.
8. Choose the photography, image-edit, icon, or supporting-raster lane below.
9. Generate or author the smallest requested set. Inspect every result and iterate with one targeted change at a time.
10. Save project-bound assets non-destructively in the consuming project. Report the final paths, prompt, references, generation or authoring method, transformations, and recommended alt treatment.

## Photography and raster assets

- Use the built-in image generation tool by default for new photography, illustrations grounded by supplied references, and substantive raster edits.
- Treat local images as visible inputs only after inspecting them. Distinguish a reference image from an edit target.
- Use `photorealistic-natural` for Horizon lifestyle and hero photography.
- Derive the subject placement and copy-safe area from the actual layout. Do not assume left or right placement without layout evidence.
- Keep headlines, disclosures, rates, product UI, account details, and brand marks out of generated pixels. Add accurate text and approved identity in the consuming layout.
- Preserve explicit edit invariants. Save edits beside the source with a descriptive versioned filename unless replacement is explicitly requested.
- Follow the installed image-generation workflow for transparent raster output, including its built-in-first chroma-key process and validation. Do not silently switch models or API paths.
- Ask for a style reference before introducing illustration, 3D, collage, or another visual family that the Horizon examples do not establish. If none is available, offer an established photography or icon direction instead.

## Production icons

1. Search filenames and inspect the closest three existing SVGs before designing a new icon.
2. Prefer a familiar single metaphor over a compound scene. Avoid duplicating an existing concept under a new name.
3. Use image generation only for optional concept exploration. Do not ship generated raster linework as the production vector.
4. Recreate or author the selected direction as deterministic SVG with a transparent canvas, balanced padding, near-black `#171617` artwork, and no embedded raster.
5. Keep the geometry simple, calm, and legible. Use rounded line relationships and visual weight consistent with the closest references; do not add a background plate, label, logo, gradient, shadow, or decorative brand color.
6. Deliver the SVG plus a transparent 512×512 PNG preview by default. Preserve the intended aspect ratio within the square PNG rather than stretching the artwork.
7. Inspect the icon at 32px and 36px. Verify direct use on white and warm-neutral surfaces and an inverse-white treatment on red or dark surfaces with at least 3:1 contrast.

## Boundaries

- Preserve the supplied Horizon Bank wordmarks and HB mark exactly. Never prompt a model to redraw, reinterpret, or decorate them.
- Do not generate payment-card designs, legal disclosures, rates, financial claims, real customer data, credentials, account numbers, or identifiable personal records.
- Do not copy another bank's identity, imagery, customer data, screenshots, or product claims.
- Do not imply that a pictured person is a real Horizon customer.
- Do not force red and yellow into clothing or scenery. Brand alignment comes from composition, tone, and the consuming interface.
- Keep generated visuals separate from full UI mockups; use the Horizon UI-building guidance for complete screens and flows.

## Completion gate

Finish only when the asset matches its intended placement, aligns with the selected Horizon references, contains no unwanted text or marks, avoids anatomy and device artifacts, remains usable at the target crop or size, has an accessibility recommendation, and includes provenance. For icons, also verify SVG integrity, transparency, small-size recognition, and the PNG preview.
