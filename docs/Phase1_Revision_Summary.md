# Phase 1 Revision Summary — v1.3.1 Overlay

**Date:** 2026-05-12
**Scope:** review of the uploaded v1.3.0 overlay against the Phase 1 Analytics Spec, Red JEC Audit, and Phase 1→2 Architecture Readiness assessment.

## Executive finding

The uploaded v1.3.0 package was a strong multilingual scaffold overlay, but it was not ready to make live because launch-critical analytics, CTA instrumentation, UTM enforcement, backend-preconnect, and deploy-runbook pieces were still specified in documents rather than implemented in the overlay.

The v1.3.1 overlay adds those missing launch pieces without changing the locked campaign decisions.

## What was revised

| Issue found | Risk | Revision made |
|---|---|---|
| Analytics spec existed but the theme lacked `cta.html` and `analytics.js`. | Day-one funnel data would be blind. | Added `partials/cta-link.html`, `shortcodes/cta.html`, `assets/js/analytics.js`, and `partials/analytics-script.html`. |
| Spec described shortcode use inside templates. | Hugo templates cannot use Markdown shortcode syntax directly. | Added a template partial and made the shortcode a wrapper around it. |
| Outbound CTA destination map was absent from `hugo.toml.diff`. | CTAs could ship with hand-coded URLs and no UTM consistency. | Added `[params.cta_destinations]` and optional language-specific destination maps. |
| Preconnects were an audit requirement but absent from overlay. | First-click latency to campaign backends would be worse. | Added `partials/head-preconnects.html`. |
| Language switcher lacked analytics hooks. | Translation-demand signal would be incomplete. | Added `language_switcher_open`, `language_switcher_select`, and data dimensions. |
| Placeholder pages lacked switcher-level English fallback. | Mobile users could miss the English fallback path. | Added top English fallback link when current page is `placeholder`. |
| Existing status lookups used `.RelPermalink`. | Non-English paths could probe `/es/about/::es` instead of `/about/::es`. | Revised status lookups to use `.Params.canonical_path` when present. |
| Pending notice lacked analytics hooks. | Translation-priority dashboard could miss demand. | Added `data-pending-notice`, `language_pending_notice_view`, and English-click events. |
| Preflight checklist did not cover the 14-event taxonomy or UTM scheme. | Build could pass while analytics remained incomplete. | Replaced preflight with a launch-specific blocking checklist. |
| No operator go-live guide existed. | Cloudflare build, preview, sign-off, and rollback path were under-specified. | Added `Phase1_Build_GoLive_Guide.md`. |
| No scriptable static check existed. | Repeated manual checks would drift. | Added `bin/preflight-check.sh`. |

## Items deliberately not marked complete

These remain blocking until the operator or reviewer completes them:

- live Brevo URL replacement;
- live Umami `data-website-id` confirmation;
- ActBlue, Action Network, and Brevo Spanish-route verification if Spanish CTAs are exposed;
- Sam Ray review of FPPC footer source, AI disclosure source, Pillar 2 claim, and Pillar 3 strike-fund wording;
- Lauren review of treasurer/FPPC/donation/email surfaces;
- conversion of existing v1.2.0 layout CTAs to the new CTA partial, because the uploaded bundle is an overlay and does not include the full v1.2.0 templates.

## Launch posture

The overlay is ready to apply to a clean checkout. It is not a substitute for the final rendered-preview review. Production deploy remains gated by `docs/Phase1_Preflight_Checklist.md`.

— end of `Phase1_Revision_Summary.md`
