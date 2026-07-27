# Prompt recipes and quality review

## Reference intake

The bundled Horizon examples are sufficient for normal work. Additional requester examples are optional.

If extra examples would improve a particular composition or subject, say:

> If you have a layout or image you want this to resemble, you can attach it, but you do not need to. I can work from the bundled Horizon references.

Never frame examples as a prerequisite. Do not pause when the request, project context, and bundled assets provide enough direction.

For every image input, state its role:

```text
Image 1: Horizon style and lighting reference
Image 2: Horizon composition reference
Image 3: requester-provided subject reference
Image 4: edit target
```

Use two to four references. More inputs can dilute the intended subject or cause unwanted details to transfer.

## Lifestyle or hero prompt

```text
Use case: photorealistic-natural
Asset type: <hero / editorial card / campaign image / article header>
Primary request: <the requested financial moment>
Input images: <two to four files with explicit roles>
Scene/backdrop: <credible home, work, travel, retail, or community environment>
Subject: <people and their concrete action>
Style/medium: photorealistic candid editorial photography; authentic skin, fabric, wood, paper, and device texture
Composition/framing: <wide / medium / close / overhead>; derive subject placement and copy-safe area from the consuming layout
Lighting/mood: soft believable daylight; warm neutral balance; calm, capable, supportive
Constraints: inclusive and natural casting; no text; no logos; no watermark; no account, card, or personal data; plausible hands, devices, reflections, and eye lines
Avoid: staged advertising poses; handshakes; piggy banks; floating money; luxury signaling; despair stereotypes; heavy retouching; synthetic HDR polish
```

Do not add people, props, or a side-specific composition that the request or layout does not support.

## Image-edit prompt

```text
Use case: <precise-object-edit / lighting-weather / identity-preserve / compositing>
Asset type: <destination>
Input images: Image 1: edit target; Image 2: optional Horizon style reference
Primary request: change only <requested change>
Constraints: preserve subject identity, geometry, camera angle, crop, lighting logic, and all unmentioned content; no new text, logos, marks, or people
Avoid: composition drift; face or hand changes; altered device content; extra objects
```

Repeat the invariants for every iteration. Save a new version instead of overwriting the source unless replacement is explicit.

## Supporting raster prompt

Use this only when the asset remains inside an established photographic direction or the requester supplied a clear style reference:

```text
Use case: <photorealistic-natural / stylized-concept>
Asset type: <background / cutout / section visual>
Primary request: <asset>
Input images: <reference roles>
Style/medium: match the supplied reference family without adding a new brand style
Composition/framing: fit the target dimensions with intentional open margins
Constraints: no text; no logos; no Horizon identity redraw; no watermark; no embedded claims or customer data
```

If the user requests an unestablished illustration, 3D, or collage style without a reference, explain that Horizon does not yet define that family and offer the established photography or icon direction.

## New icon brief

Search the library before using this brief. Treat image generation as optional concept exploration only.

```text
Asset type: Horizon utility icon concept
Primary request: one simple icon representing <concept>
Input images: Image 1..3: closest Horizon icon style references
Style/medium: clean monochrome line-icon concept suitable for deterministic SVG recreation
Composition/framing: one centered familiar metaphor with balanced padding and a strong silhouette
Color palette: near-black #171617 only on a plain removable background
Constraints: no text; no logo; no initials; no background tile; no gradient; no shadow; no 3D; no perspective scene; no decorative detail
```

Rebuild the chosen direction as SVG rather than tracing noisy raster pixels. Use a transparent canvas, explicit `viewBox`, `#171617` artwork, and no external references, scripts, filters, masks that hide raster content, or `<image>` elements.

Deliver:

- `<descriptive-name>.svg`
- `<descriptive-name>-preview.png`, transparent, 512×512
- A visual check at 32px and 36px on white, `#F4F0ED`, `#D71E28` with inverse white, and `#141414` with inverse white

## Photography review

- The financial action reads without explanatory text.
- Casting and environment feel specific, inclusive, and unstaged.
- Skin, hands, teeth, eyes, devices, paper, reflections, and repeated objects are plausible.
- The crop works at the destination aspect ratio and preserves the key action at responsive crops.
- Copy space is intentional when required and unnecessary emptiness is absent otherwise.
- No visible text, competitor mark, fake Horizon identity, card/account data, watermark, or unsupported product claim appears.
- Color, light, texture, and emotional tone align with the selected Horizon references.
- The result does not imply that pictured people are real customers.

## Icon review

- No existing icon already communicates the concept.
- The metaphor remains clear at 32px and 36px.
- Apparent weight, corner character, density, and padding match nearby Horizon icons.
- The SVG canvas is transparent and contains no text, logo, plate, raster image, script, gradient, shadow, or unintended color.
- Artwork is `#171617`; inverse presentation is white without changing geometry.
- Icon contrast is at least 3:1 against adjacent surfaces.
- The 512×512 PNG has alpha, preserves aspect ratio, and matches the SVG.

## Delivery record

Provide a compact record with:

```text
Asset:
Intended use and crop:
Final path(s):
Prompt or vector brief:
Reference files and roles:
Generation or authoring path:
Transformations:
Alt recommendation:
Review notes:
```

Use descriptive, Horizon-neutral filenames. Keep discarded validation variants outside the plugin unless the requester explicitly approves them as canonical references.
