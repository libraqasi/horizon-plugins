---
name: audit-horizon-bank-ui
description: Audit Horizon Bank web and responsive-web interfaces, screenshots, prototypes, frontend code, and web design systems for standalone wordmark and optional HB icon use, Horizon typography, semantic tokens, responsive behavior, financial UX safety, agentic-commerce boundaries, content quality, and accessibility. Use for web design critiques, implementation reviews, pre-handoff QA, regression checks, or requests asking whether a web experience follows Horizon Bank design guidance. Native source auditing is not included.
---

# Audit Horizon Bank UI

Produce an evidence-backed review with prioritized, actionable findings. Do not silently modify an artifact during a review-only request.

## Supported audit scope

The automated audit and source checklist support web and responsive-web experiences. A non-web screenshot or rendered artifact may still receive a limited review of Horizon identity, content, financial safety, state clarity, and broadly applicable accessibility outcomes. Do not claim source-level iOS, Android, desktop-native, wearable, or other platform validation; name the unsupported target and recommend its platform-native engineering and accessibility checks.

## Audit workflow

1. Identify the artifact, product surface, framework, target devices, and primary journey.
2. Read [review-checklist.md](references/review-checklist.md) completely.
3. Read [evidence-boundaries.md](references/evidence-boundaries.md) before labeling a preference as a requirement.
4. Inspect the rendered UI when available. Review code and screenshots together.
5. For eligible web source, run `python3 scripts/audit_horizon_ui.py <source-path> --strict`. Confirm at least one eligible web file was scanned and review false positives. If the result reports zero files, record that no web audit was performed.
6. Exercise desktop and responsive-web navigation, zoom, keyboard focus, loading, empty, error, interrupted, success, long labels, and realistic finance data.
7. Report findings by severity:
   - `P0`: exposes sensitive data, bypasses authorization, or enables a materially harmful financial action.
   - `P1`: major accessibility, trust, navigation, or task-completion failure.
   - `P2`: visible identity, responsive, component, or content inconsistency.
   - `P3`: polish or maintainability improvement.
8. Tie each finding to a screen, element, file, or line. Explain impact and the smallest credible remediation.
9. Separate confirmed findings, questions, and optional improvements.

## Review priorities

Audit in this order:

1. Authorization boundaries, privacy, fraud resistance, and irreversible action.
2. Task completion, state clarity, recovery, and responsive navigation.
3. Accessibility semantics, keyboard behavior, contrast, zoom, motion, and touch.
4. Standalone wordmark and optional HB icon use, typography, palette, iconography, imagery, and content voice.
5. Token consistency, component reuse, performance, and visual polish.

## Required output

Lead with the highest-severity findings. For each finding include severity, evidence, user impact, and remediation. Then summarize what already works, unresolved evidence gaps, supported scope, and validation performed. If there are no actionable findings, say so directly and name residual risks or tests not performed. Never present a zero-file scan or a non-web visual review as a completed web source audit.
