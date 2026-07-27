# Horizon photography and iconography

## Canonical sources

Use the assets in the sibling build skill as the source of truth:

- [Seven editorial photographs](../../build-horizon-bank-ui/assets/stock/)
- [Sixty banking and utility icons](../../build-horizon-bank-ui/assets/icons/)

Do not copy these libraries into this skill. Inspect them in place and pass only the most relevant files to an image model.

## Photography reference map

| File | Useful alignment cues |
|---|---|
| `entrepreneurship.jpg` | Two people collaborating over plans and materials in a real workspace; warm daylight, tactile surfaces, calm concentration, broad environmental context |
| `family-travel.jpg` | Multigenerational group planning together at a table; natural interaction, practical travel objects, warm domestic setting |
| `financial-resilience.jpg` | Two people reviewing paperwork at home; supportive tone, uncluttered right-side copy space, soft natural light |
| `home-renovation.jpg` | Two adults reviewing plans and samples in a bright kitchen; believable decision-making, pale neutral environment, usable open space |
| `receipt-capture.jpg` | Overhead close-up of hands using a phone with a receipt; clear task focus, warm wood, simple composition |
| `retirement-planning.jpg` | Two older adults reviewing notes and a device outdoors; relaxed collaboration, natural greenery, quiet optimism |
| `vehicle-planning.jpg` | People reviewing information beside a vehicle in a bright dealership; credible purchase context, neutral styling, no celebratory excess |

## Shared photographic direction

- Show a real action connected to planning, paying, saving, working, traveling, purchasing, or managing money.
- Favor candid editorial framing over people posing or looking at the camera.
- Use inclusive casting across a series without turning identity into the story. Show different ages, races, genders, abilities, households, and work contexts naturally.
- Use soft daylight or believable practical light, warm neutrals, restrained wardrobe, natural skin texture, real material grain, and moderate depth of field.
- Keep the mood calm, capable, supportive, and optimistic without implying effortless wealth.
- Include enough environment to make the financial moment legible. Use close or overhead framing only when the task itself is the story.
- Reserve clean copy space only when the destination needs it. Keep faces, hands, and the key action away from likely crop boundaries.
- Let red and yellow enter through the interface around the image. Do not costume the scene in brand colors.

## Photographic avoid list

- Posed handshakes, staged cheering, piggy banks, floating currency, piles of cash, keys held toward camera, luxury signaling, or generic corporate boardrooms
- Visible third-party marks, fake Horizon marks, legible card or account data, generated phone UI, signage, captions, watermarks, or gibberish text
- Despair stereotypes, shame, coercion, exaggerated urgency, or a community shown only through financial hardship
- Plastic skin, over-retouching, HDR polish, extreme color grading, synthetic studio perfection, or excessive shallow focus
- Malformed hands, duplicated people or objects, warped devices, impossible reflections, inconsistent eyelines, or implausible physical interactions

## Hero composition

- Inspect the consuming layout before choosing subject placement.
- Reserve a copy-safe region with low detail and stable tonal contrast; do not bake a text overlay into the image.
- Keep the scene meaningful after responsive center, left, and right crops.
- Prefer one clear financial moment over a montage.
- Verify that any interface gradient or scrim preserves faces and useful details while meeting text contrast requirements.

## Icon system

The existing icons are transparent, single-color banking and utility symbols. Most use `#171617` compound-path artwork with simple outline-like forms, rounded relationships, generous internal negative space, and a complete-object metaphor.

Match these characteristics:

- One recognizable concept at a glance
- Near-black `#171617` artwork on a transparent canvas
- Balanced silhouette and padding with no permanent background tile
- Similar apparent weight to the nearest existing icons
- Minimal detail that survives at 32px and 36px
- No text, initials, logo fragments, decorative colors, gradients, shadows, perspective scenes, or embedded images

Search before drawing. Useful comparison families include money, cards and payments, buildings, devices, support, travel and mobility, planning, data, and agent or automation concepts.

For a bounded tile, create the surface in the consuming component. Use the original dark artwork on light surfaces and an inverse-white presentation on red or dark surfaces.
