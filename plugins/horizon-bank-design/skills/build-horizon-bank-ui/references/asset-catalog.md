# Asset catalog

## Logos

`assets/logos/` contains:

- `horizon-bank-icon.svg`: compact red HB monogram with yellow rule.
- `horizon-bank-wordmark-black.svg`: primary standalone black wordmark with the approved reinforced regular weight for light surfaces.
- `horizon-bank-wordmark-white.svg`: matching standalone white wordmark for red or dark surfaces.
- `horizon-bank-logo-horizontal.svg`: compatibility alias for the standalone black wordmark.
- `horizon-bank-logo-horizontal-white.svg`: compatibility alias for the standalone white wordmark.

The wordmark and icon are independent. Use the wordmark when the bank name should be explicit and the icon only when a compact mark is useful. Do not automatically combine them into a lockup. Preserve geometry and safe space. Never replace HB with H.

## Fonts

`assets/fonts/web/` contains:

- `HorizonSans-Regular.woff2`
- `HorizonSans-SemiBold.woff2`
- `HorizonSans-Italic.woff2`
- `HorizonSans-Display.woff2`

Use the `@font-face` declarations and family aliases in `assets/starter/horizon-tokens.css`. Use Horizon Sans Display only at regular weight for concise headings and Horizon Sans for interface copy. The formal logo is path-based and does not require a font file.

## Icons

`assets/icons/` contains 60 SVG banking, money, device, support, planning, mobility, and utility symbols. Filenames describe the concept. Every icon has a transparent canvas; no icon file includes a white background plate.

Use icons to reinforce visible labels. The bundled artwork is monochrome dark ink and works directly on white, warm, yellow, and other sufficiently light surfaces. The files intentionally have different intrinsic proportions, so size an `<img>` on one axis with the other set to `auto`; for a bounded icon area, combine `max-width`, `max-height`, and `object-fit: contain`. Never assign the same fixed width and height to every icon. When an icon is embedded with `<img>` on red or dark surfaces, use the starter’s `.horizon-icon-inverse` filter class to render it white, and verify at least 3:1 icon contrast. When inlining an SVG, changing the single artwork fill is safe because the icons are monochrome, but preserve their geometry and transparent canvas. Do not add a permanent white rectangle inside the SVG; if a bounded icon tile is required, create that surface in the surrounding component so its color and contrast remain contextual.

## Stock photography

`assets/stock/` contains seven supplied 1586×992 JPEGs:

- `entrepreneurship.jpg`
- `family-travel.jpg`
- `financial-resilience.jpg`
- `home-renovation.jpg`
- `receipt-capture.jpg`
- `retirement-planning.jpg`
- `vehicle-planning.jpg`

Use photography only when it clarifies or humanizes the product story. Add useful alt text when informative, use empty alt when decorative, preserve aspect ratio, set an intentional crop with `object-fit`, and verify text contrast if copy overlays an image.

## Tokens and starter

- `assets/tokens/horizon-tokens.json` is a portable custom token map.
- `assets/starter/horizon-tokens.css` provides semantic tokens, the brand frame, controls, cards, statuses, forms, finance rows, and accessibility adaptations.
- `assets/starter/horizon-starter-preview.html` is a component gallery and markup starting point, not a product screen.

Copy only what the product needs and keep semantic names in application code.
