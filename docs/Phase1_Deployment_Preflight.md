# Phase 1 Deployment Preflight Checklist — turonsf.com v1.3.0

**Document role:** Pre-deploy verification gate for the **deployment itself** — distinct from `Phase1_Preflight_Checklist.md` (which covers the build artifact's correctness). This document covers GitHub repo posture, Cloudflare account isolation, DNS, certs, the first-deploy smoke test, and post-deploy verification.
**Walk this AFTER the build preflight passes.** Build preflight = "the bundle is correct." Deployment preflight = "the bundle reaches the live domain correctly, on isolated infra, observable from day one."
**Pairs with:** `Phase1_Deployment_Red_JEC_Audit.md`, `Phase1_Deployment_Run_Guide.md`.

This checklist assumes Run Guide steps 1–6 have been executed (fresh GitHub org, fresh Cloudflare account, repo created, Pages project created, custom domain attached, first preview build succeeded).

---

## Section 1 — Infrastructure isolation (FPPC entanglement defense)

| # | Check | Result |
|---|---|---|
| 1.1 | GitHub org for this repo is **NOT** `CAREInstitute`. Recommended: `MichaelTuronForSFUSD` or equivalent campaign-scoped org. **BLOCKING.** | |
| 1.2 | Cloudflare account hosting the Pages project is **NOT** the same Cloudflare account that hosts careinstitute.ai. **BLOCKING.** | |
| 1.3 | Cloudflare account billing email is a campaign-scoped address (e.g., `cloudflare@turonsf.com`), not a CAREInstitute or personal-only address. **BLOCKING.** | |
| 1.4 | Domain registrar billing for turonsf.com is paid by the campaign committee bank account. **BLOCKING.** Lauren Turon confirms. | |
| 1.5 | Cloudflare API tokens scoped to this account only; no token has cross-account access to careinstitute.ai infrastructure. **BLOCKING.** | |
| 1.6 | Umami Cloud account hosting turonsf.com analytics is **NOT** the same account that hosts careinstitute.ai analytics. **BLOCKING.** | |
| 1.7 | Email forwarding (`info@turonsf.com`) is configured on Cloudflare Email Routing on the campaign Cloudflare account, OR documented as billed-to-campaign on an equivalent service. **BLOCKING.** | |
| 1.8 | Hugo theme `turon-civic` lives inside this repo (not as a cross-org submodule or external dependency). **BLOCKING.** Confirm: `ls themes/turon-civic/` shows the theme files in this repo. | |
| 1.9 | No careinstitute.ai or 501(c)(3)-attributable resources (S3 buckets, CDN origins, SSO providers) are referenced from any file in the deployed bundle. **BLOCKING.** | |

## Section 2 — GitHub repo posture

| # | Check | Result |
|---|---|---|
| 2.1 | Repo visibility is **public** (transparency aligns with FPPC posture). Or, if private, document the rationale. **WARN.** | |
| 2.2 | Branch protection on `main`: PR required, status checks required, no direct push for non-admins. **BLOCKING.** | |
| 2.3 | GitHub Pages explicitly DISABLED (Settings → Pages → Source = None). Audit F19. **BLOCKING.** | |
| 2.4 | Secret scanning ENABLED (Settings → Code security → Secret scanning). **WARN.** | |
| 2.5 | Dependabot alerts ENABLED. **WARN.** | |
| 2.6 | No secrets / tokens / API keys present in any committed file. `git log --all -p \| grep -iE "(api_key\|secret\|token=\|password)"` returns nothing campaign-relevant. **BLOCKING.** | |
| 2.7 | `.gitignore` excludes `*.draft.md`, `notes/`, `private/`, `.env*`, etc. (audit F18). **BLOCKING.** | |
| 2.8 | CI workflow `.github/workflows/build-and-check.yml` is present and runs on PR. **BLOCKING.** | |
| 2.9 | A PR exercising the CI workflow has run and passed (test it before the first real deploy). **BLOCKING.** | |
| 2.10 | License file present (or explicit "no license / all rights reserved" notice). **WARN.** | |

## Section 3 — DNS + domain

| # | Check | Result |
|---|---|---|
| 3.1 | turonsf.com nameservers point to Cloudflare (`*.ns.cloudflare.com`). **BLOCKING.** Verify with `dig NS turonsf.com`. | |
| 3.2 | DNS A / CNAME record for `turonsf.com` resolves to Cloudflare Pages (the Pages project's `*.pages.dev` host). **BLOCKING.** | |
| 3.3 | DNS CNAME for `www.turonsf.com` exists and points to apex (or to Cloudflare Pages directly with a redirect rule). **BLOCKING.** | |
| 3.4 | CAA record exists on turonsf.com authorizing only the Cloudflare cert provider (`pki.goog` + `letsencrypt.org`). Audit F13. **WARN** (not strictly required but recommended). | |
| 3.5 | DNS propagation verified: `dig turonsf.com` from at least 2 geographic locations returns Cloudflare. **BLOCKING.** | |
| 3.6 | SSL/TLS mode in Cloudflare = **Full (Strict)**. Audit F14. **BLOCKING.** | |
| 3.7 | "Always Use HTTPS" = ON. **BLOCKING.** | |
| 3.8 | "Automatic HTTPS Rewrites" = ON. **BLOCKING.** | |
| 3.9 | HTTPS cert is valid and trusted: `curl -sIv https://turonsf.com/ 2>&1 \| grep -i "subject:"` shows a valid cert chain. **BLOCKING.** | |
| 3.10 | HSTS preload: **deferred to Phase 2** (do NOT enable at v1.3.0 first deploy — hard to revert). | n/a |

## Section 4 — Cloudflare Pages configuration

| # | Check | Result |
|---|---|---|
| 4.1 | Pages project name: `turonsf-com` (or operator-chosen equivalent). **BLOCKING.** | |
| 4.2 | Build command: `hugo --minify --gc`. **BLOCKING.** | |
| 4.3 | Build output directory: `public`. **BLOCKING.** | |
| 4.4 | Environment variable `HUGO_VERSION` set to `0.125.7` (matches v1.2.0 baseline). **BLOCKING.** | |
| 4.5 | Environment variable `NODE_VERSION` set to `20` (latest LTS at audit date) or unset (Pages picks default). **WARN.** | |
| 4.6 | Production branch: `main`. **BLOCKING.** | |
| 4.7 | Preview deployments enabled for all non-main branches. **WARN.** | |
| 4.8 | Preview deployments have `X-Robots-Tag: noindex` applied. Audit F9. **BLOCKING.** | |
| 4.9 | Cloudflare Web Analytics DISABLED for this project (Umami is canonical). Audit F17. **WARN.** | |
| 4.10 | Custom domain `turonsf.com` attached and verified in Pages → Custom domains. **BLOCKING.** | |
| 4.11 | Redirect rule: `https://www.turonsf.com/*` → `https://turonsf.com/$1` (301). Audit F15. **BLOCKING.** | |
| 4.12 | `_headers` file applied (security headers visible in `curl -sI https://turonsf.com/`). Audit F21. **BLOCKING.** | |
| 4.13 | `_redirects` file applied (`/give/` → `/donate/` returns 301). **BLOCKING.** | |

## Section 5 — Analytics + community channel

| # | Check | Result |
|---|---|---|
| 5.1 | Umami site_id for turonsf.com matches the value in `hugo.toml` `[params.umami]`. **BLOCKING.** | |
| 5.2 | Umami script tag is rendered in the base template `<head>` (verify via View Source on live site). **BLOCKING.** | |
| 5.3 | `analytics.js` shim loads on every page (verify View Source for `<script defer src=".../analytics...js">`). **BLOCKING.** | |
| 5.4 | First Umami event recorded in dashboard within 5 minutes of first deploy (`page_view`). **BLOCKING.** | |
| 5.5 | `donate_cta_click` event fires when hero donate link is clicked (test on live site, verify in Umami live view). **BLOCKING.** | |
| 5.6 | `newsletter_cta_click` event fires when hero newsletter CTA is clicked. **BLOCKING.** | |
| 5.7 | `hero_cta_primary_view` impression event fires when hero scrolls into view. **BLOCKING.** | |
| 5.8 | `scroll_depth_75` and `scroll_depth_100` fire when scrolling to bottom. **WARN.** | |
| 5.9 | Three Umami custom dashboards configured: Phase 1 conversion funnel, Translation demand priority, Pillar attention. Audit + Analytics Spec §7. **WARN.** | |
| 5.10 | info@turonsf.com receives mail: send test message from external account, confirm receipt within 5 minutes. **BLOCKING.** | |
| 5.11 | mailto:info@turonsf.com link clicks fire `email_contact_click` event with `source` dimension. **WARN.** | |

## Section 6 — Backend integration verification

| # | Check | Result |
|---|---|---|
| 6.1 | ActBlue donate page exists at the URL configured in `hugo.toml [params.cta_destinations].donate`. Test by clicking from hero. **BLOCKING.** | |
| 6.2 | ActBlue page loads with UTM parameters intact in URL. **BLOCKING.** | |
| 6.3 | ActBlue Spanish-language form parameter verified for Spanish CTA clicks. Audit F23. **BLOCKING for Spanish go-live.** | |
| 6.4 | Action Network volunteer form URL works and accepts test submission. **BLOCKING.** | |
| 6.5 | Brevo newsletter signup form embeds correctly OR redirects to Brevo-hosted form. **BLOCKING.** | |
| 6.6 | Brevo `sib_form_success` callback fires `newsletter_signup_submit` event in Umami. **BLOCKING.** | |
| 6.7 | Cloudflare Turnstile renders on any campaign-controlled forms. **WARN.** | |

## Section 7 — First-deploy smoke test (live domain walkthrough)

Walk each item on `https://turonsf.com` AND on `https://turonsf.com/es/`, `/zh-Hant/`, `/zh-Hans/`, `/tl/`, `/vi/`, `/ar/`. iPhone-narrow viewport AND desktop 1440px viewport.

| # | Check | Result |
|---|---|---|
| 7.1 | `https://turonsf.com/` returns 200 with rendered home page. **BLOCKING.** | |
| 7.2 | Every non-English language path returns 200 (or 404 only for unconditionally-deferred pages). **BLOCKING.** | |
| 7.3 | Every page carries the utility bar with election date + FPPC ID 1482971. **BLOCKING.** | |
| 7.4 | Every page carries the §84305 footer with "Michael Turon for SFUSD Board of Education 2026" + FPPC ID 1482971 + Treasurer Lauren Turon. **BLOCKING.** | |
| 7.5 | Every non-English page renders the AI translation disclosure banner OR the pending notice (not both, not neither). **BLOCKING.** | |
| 7.6 | Arabic page (`/ar/`) renders RTL layout (mirrored nav, mirrored chevrons, language switcher opens to inline-start). **BLOCKING.** | |
| 7.7 | Trust strip dollar figures render LTR inside RTL Arabic flow (bidi isolation working). **BLOCKING.** | |
| 7.8 | Language switcher functions: clicking each option lands on the correct language path. **BLOCKING.** | |
| 7.9 | Hero primary CTA "Get campaign updates" clicks through to Brevo with UTMs. **BLOCKING.** | |
| 7.10 | Hero donate link clicks through to ActBlue with UTMs. **BLOCKING.** | |
| 7.11 | Hero tertiary "or read the full platform" link goes to `/platform/`. **BLOCKING.** | |
| 7.12 | Nav donate button works. **BLOCKING.** | |
| 7.13 | Footer newsletter / volunteer / donate / info@ links all work. **BLOCKING.** | |
| 7.14 | No console errors on any page in Safari + Chrome. **BLOCKING.** | |
| 7.15 | No mixed-content warnings (everything HTTPS). **BLOCKING.** | |
| 7.16 | Lighthouse score: Performance ≥ 90, Accessibility ≥ 95, Best Practices ≥ 95, SEO ≥ 95 (mobile). **WARN.** | |
| 7.17 | Page weight on mobile ≤ 100KB transferred (gzipped) per Architecture Decision 6. **WARN.** | |
| 7.18 | Time to First Byte (TTFB) ≤ 200ms from SF region. **WARN.** | |

## Section 8 — Search-engine discovery

| # | Check | Result |
|---|---|---|
| 8.1 | `https://turonsf.com/sitemap.xml` returns valid XML with all English pages. **BLOCKING.** | |
| 8.2 | `https://turonsf.com/robots.txt` returns the v1.3.0 file with 11-bot AI allowlist intact. **BLOCKING.** | |
| 8.3 | `https://turonsf.com/llms.en.txt` returns the English llms file. **WARN.** | |
| 8.4 | All 7 `llms.{lang}.txt` files accessible at their canonical URLs. **WARN.** | |
| 8.5 | Submit sitemap to Google Search Console for the verified turonsf.com property. **WARN.** | |
| 8.6 | Verify domain ownership in Google Search Console (TXT record on the domain). **WARN.** | |
| 8.7 | Bing Webmaster Tools — same. **WARN.** | |

## Section 9 — Rollback readiness

| # | Check | Result |
|---|---|---|
| 9.1 | Cloudflare Pages → Deployments tab shows the previous v1.2.x deploy as available for rollback. **BLOCKING.** | |
| 9.2 | Operator has verified ability to click "Rollback to this deployment" on the v1.2.x deploy in Cloudflare. **BLOCKING.** | |
| 9.3 | Git tag `v1.2.x-last` exists on the v1.2.x commit for emergency revert. **WARN.** | |
| 9.4 | Documented rollback procedure exists in Run Guide §11. **BLOCKING.** | |

## Section 10 — Sign-off block

Deploy proceeds only after every BLOCKING item is ✅ and the following sign-offs are recorded.

| Role | Name | Scope | Date | Signature |
|---|---|---|---|---|
| Operator | Michael Turon | Full deployment preflight | | |
| Counsel | Sam Ray | Sections 1 (entanglement), 2 (repo posture) | | |
| Treasurer | Lauren Turon | Sections 1.4 (billing), 5.10 (mail receipt), 6.1-6.3 (ActBlue) | | |

After sign-offs, deploy proceeds per Run Guide §8 (push to main; Cloudflare Pages auto-builds; preflight Section 7 + 8 walked on live domain within 30 minutes of deploy).

— end of `Phase1_Deployment_Preflight.md`
