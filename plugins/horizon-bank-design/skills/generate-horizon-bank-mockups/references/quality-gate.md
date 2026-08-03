# Mockup quality gate

Review the rendered artifact at full size and as a thumbnail. Iterate until no critical failure remains.

## Critical failures

Do not deliver with any of these:

- misspelled, distorted, recolored, or invented Horizon identity;
- another bank's name, logo, typography, customer data, rates, or disclosures;
- unreadable labels, nonsense currency, duplicated controls, or contradictory values;
- real customer data, full account numbers, secrets, credentials, or authentication codes;
- a consequential action without enough scope or consequence to understand it;
- false live-payment, issuer, merchant, network, protocol, compliance, or certification claims;
- unrequested policy, legal, fee, timing, cancellation, eligibility, partner, network, or disclosure claims;
- clipped primary content or unusable responsive reflow;
- an image that does not visibly contain the requested mockup.

## Visual checks

- The primary task or decision is obvious within three seconds.
- Horizon Bank is recognizable through correct identity, red/yellow brand punctuation, warm neutral field, typography, and restrained geometry.
- Red is concentrated on the brand frame, primary action, selection, or high-value emphasis.
- Indigo is used as a link or informative accent, not as a decorative gradient.
- Titles are concise, task content is left aligned, and labels stay close to their values.
- Cards communicate real groups; tables, timelines, ledgers, or summaries remain structured when needed.
- Buttons have a clear hierarchy and name outcomes.
- Icons reinforce visible labels and do not replace important text.
- Wide, square, and narrow icons retain their intrinsic proportions; no icon is stretched or squeezed to fill a fixed box.
- Photography, if present, supports the customer story and leaves clear room for UI copy.
- The artifact remains understandable at thumbnail size without becoming sparse at full size.

## Financial and trust checks

- Account names and identifiers are synthetic and masked.
- Money uses consistent currency, signs, decimals, and alignment.
- Available, current, pending, scheduled, and posted values are not conflated.
- Review screens expose source, destination, amount, fees, total, timing, and edit/cancel path.
- Delegated actions expose requester, merchant, scope, limit, expiration, and revocation.
- Agent planning remains visually separate from Horizon authorization.
- Loading, empty, interrupted, error, or success feedback explains what happened and the next step.
- Success is durable and not represented only by a transient toast.

## Responsive checks

- Mobile content reflows instead of shrinking.
- The primary task, identity, critical state, and safe action order survive.
- Navigation adapts intentionally and keeps current location clear.
- Tables become readable rows, progressive disclosure, or horizontal structures with an explicit affordance.
- Touch actions are visually large enough and are not crowded by nearby controls.
- Sticky actions do not cover content.

## Raster-generation checks

- Inspect every word, amount, date, icon, hand, and face at 100%.
- Compare the formal identity against `assets/visual-references/identity.png`.
- Compare palette, type character, spacing, radius, and icon treatment against `foundations.png`.
- Remove fake browser chrome, device hardware, perspective, and presentation backgrounds unless requested.
- Check for model artifacts: warped borders, inconsistent spacing, mixed typefaces, impossible shadows, random badges, and repeated elements.
- Composite exact assets or use deterministic rendering when local edits cannot make critical text trustworthy.

## Iteration note

Record the three highest-impact discrepancies after each pass. Preserve successful regions and target those discrepancies in the next edit. If two raster repair passes still fail on exact text or identity, switch to HTML/SVG rendering instead of repeatedly regenerating the full image.
