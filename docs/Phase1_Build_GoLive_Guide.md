# Phase 1 Build + Go-Live Guide — turonsf.com v1.3.1

**Document role:** operator runbook to build, preview, approve, and make live the Phase 1 site.
**Deploy target:** Hugo + Cloudflare Pages static site.
**Primary gate:** `docs/Phase1_Preflight_Checklist.md`.

This guide assumes the v1.3.1 overlay has been copied into a clean v1.2.0 checkout. It is written as a deploy sequence, not as a design rationale document.

---

## 1. What this overlay changes

The v1.3.1 overlay adds or revises these production-critical pieces:

| Area | Files |
|---|---|
| Multilingual scaffolds | `content/*.{es,zh-Hant,zh-Hans,tl,vi,ar}.md`, `data/translation_status.yaml` |
| Multilingual rendering | `layouts/sitemap.xml`, `partials/head-hreflang.html`, `partials/language-switcher.html`, `partials/ai-translation-disclosure.html` |
| Analytics + CTA wiring | `partials/cta-link.html`, `shortcodes/cta.html`, `assets/js/analytics.js`, `partials/analytics-script.html` |
| Performance | `partials/head-preconnects.html`, `static/css/tokens.css.diff` |
| Docs and gates | canonical Phase 1 docs, revised preflight, this guide, `bin/preflight-check.sh` |

Important implementation note: Hugo shortcodes are content-file tools. Layout templates should call `partials/cta-link.html` directly. Markdown content may use the `cta.html` shortcode. Both paths share the same renderer, so UTM and event logic does not drift.

---

## 2. Local prerequisites

Install or confirm:

```bash
git --version
hugo version
python3 --version
```

Use the same Hugo version locally and on Cloudflare Pages. Record it:

```bash
hugo version > .hugo-version.local.txt
```

Cloudflare Pages production and preview environments should set `HUGO_VERSION` to this tested version.

---

## 3. Create the feature branch

From the site checkout root:

```bash
git checkout main
git pull --ff-only
git status --short
```

The status output must be empty.

```bash
git checkout -b phase1-v1.3.1-preflight
```

---

## 4. Copy the overlay

From the site checkout root, where `/path/to/turonsf_v1.3.1_phase1_overlay` is this overlay folder:

```bash
OVERLAY=/path/to/turonsf_v1.3.1_phase1_overlay

cp -rv "$OVERLAY/content/." ./content/
cp -rv "$OVERLAY/data/." ./data/
cp -rv "$OVERLAY/docs/." ./docs/
cp -rv "$OVERLAY/static/." ./static/
cp -rv "$OVERLAY/themes/." ./themes/
cp -rv "$OVERLAY/bin/." ./bin/
cp "$OVERLAY/layouts/sitemap.xml" ./layouts/sitemap.xml
```

Apply diffs:

```bash
git apply "$OVERLAY/hugo.toml.diff"
git apply -p0 "$OVERLAY/themes/turon-civic/static/css/tokens.css.diff"
```

If either diff fails because v1.2.0 has changed, manually reconcile the additions. Do not overwrite existing locked token values.

---

## 5. Configure live backend destinations

Open `hugo.toml` and replace placeholder destinations:

```toml
[params.cta_destinations]
  newsletter = "https://sibforms.com/serve/<live-brevo-form>"
  donate     = "https://secure.actblue.com/donate/turonsf"
  volunteer  = "https://actionnetwork.org/forms/<live-volunteer-form>"
  email      = "mailto:info@turonsf.com"
  platform   = "/platform/"
```

Do not guess Spanish URL parameters. Use language-specific override maps only after testing the backend-rendered form:

```toml
[params.cta_destinations_es]
  newsletter = "https://sibforms.com/serve/<tested-spanish-brevo-form>"
  donate     = "https://secure.actblue.com/donate/<tested-spanish-actblue-form>"
  volunteer  = "https://actionnetwork.org/forms/<tested-spanish-action-network-form>"
```

If Spanish pages are still `placeholder` and do not expose Spanish CTAs, the override map can remain absent.

---

## 6. Wire the base templates

These partial calls must be present in the v1.2.0 theme after the overlay is applied.

### 6.1 In `<head>`

```go-html-template
{{ partial "head-preconnects.html" . }}
{{ partial "head-hreflang.html" . }}
```

Keep the existing Umami tracker script with the live `data-website-id`. Do not replace the website ID during this work.

### 6.2 Near the top of `<main>`

Render the translation disclosure before the page H1/body on non-English pages:

```go-html-template
{{ partial "ai-translation-disclosure.html" . }}
```

### 6.3 Header, mobile drawer, and footer

Render the language switcher anywhere the design requires it:

```go-html-template
{{ partial "language-switcher.html" . }}
```

If the switcher appears multiple times on one page, the v1.3.1 script assigns unique menu IDs at runtime.

### 6.4 Before `</body>`

```go-html-template
{{ partial "analytics-script.html" . }}
```

This loads the local shim. It does not replace Umami. On preview pages without Umami, it logs safe no-op messages to the console.

---

## 7. Convert campaign CTAs

Template CTAs should call the partial:

```go-html-template
{{ partial "cta-link.html" (dict
  "Page" .
  "Site" .Site
  "kind" "newsletter"
  "source" "hero"
  "label_key" "newsletter_cta_primary"
  "style" "primary"
) }}
```

Use these `kind` values:

| kind | Event | Destination map key |
|---|---|---|
| `newsletter` | `newsletter_cta_click` | `newsletter` |
| `donate` | `donate_cta_click` | `donate` |
| `volunteer` | `volunteer_cta_click` | `volunteer` |
| `email` | `email_contact_click` | `email` |
| `platform` | `platform_link_click` | `platform` |

Add required impression hooks:

```html
<div data-cta-primary>...</div>
<section data-trust-strip>...</section>
```

Pillar deep-links must carry pillar dimensions unless a dedicated pillar partial is added:

```html
<a href="/platform/pillar-1/" data-event="pillar_click" data-pillar="1">
  How I'll fix Special Education staffing →
</a>
```

Markdown content may use the shortcode:

```go-html-template
{{< cta kind="donate" source="footer" label_key="donate_cta" style="text" >}}
```

---

## 8. Build locally

```bash
hugo --minify --logLevel warn
```

Then run the static guard script:

```bash
./bin/preflight-check.sh
```

Fix every failure. Warnings require a written exception in the checklist.

---

## 9. Manual preview QA

Serve locally:

```bash
hugo server --disableFastRender
```

Check these pages at minimum:

| URL | Expected |
|---|---|
| `/` | English homepage; newsletter primary CTA; no AI disclosure |
| `/about/` | English page; normal canonical |
| `/platform/` | English platform page |
| `/platform/pillar-1/` | English pillar page |
| `/platform/pillar-2/` | English pillar page |
| `/platform/pillar-3/` | English pillar page |
| `/endorsements/` | Dormant conversion surface, unless active endorsements are intentionally enabled |
| `/volunteer/` | Volunteer flow |
| `/donate/` | Donate flow |
| `/contact/` | Contact/email flow |
| `/es/` | Pending notice, noindex, English fallback link above fold |
| `/zh-Hant/` | Pending notice |
| `/zh-Hans/` | Pending notice |
| `/tl/` | Pending notice |
| `/vi/` | Pending notice |
| `/ar/` | Pending notice, RTL layout |
| `/platform/uesf-questionnaire/` | 404 while inactive |

Browser checks:

```text
- mobile 390px viewport
- desktop 1440px viewport
- keyboard-only tab order
- language switcher open/select keyboard controls
- no horizontal scroll
- console has no blocking JS errors
```

---

## 10. Analytics test on preview

On a Cloudflare preview deployment, test these events in Umami:

| Test | Expected event |
|---|---|
| Open language switcher | `language_switcher_open` |
| Select a language | `language_switcher_select` |
| View pending notice | `language_pending_notice_view` |
| Click pending notice English link | `language_pending_to_english_click` |
| View hero primary CTA | `hero_cta_primary_view` |
| Click newsletter CTA | `newsletter_cta_click` |
| Click donate CTA | `donate_cta_click` |
| Click volunteer CTA | `volunteer_cta_click` |
| Click pillar card | `pillar_click` |
| Scroll 75% / bottom | `scroll_depth_75`, `scroll_depth_100` |

Verify that every event includes `language` and `viewport`. For campaign CTAs, verify `source`. For language events, verify `from_language` and `to_language` where applicable.

---

## 11. Commit and push preview

```bash
git add -A
git diff --stat
git commit -m "feat(phase1): add multilingual preflight, CTA analytics, and deploy gates"
git push -u origin phase1-v1.3.1-preflight
```

Cloudflare Pages should create a preview deployment for the branch.

---

## 12. Cloudflare Pages settings

In Cloudflare Pages project settings:

```text
Framework preset: Hugo, or None with explicit command
Build command: hugo --minify --logLevel warn
Build output directory: public
Production branch: main
Preview deployments: enabled
Environment variable: HUGO_VERSION=<local tested version>
```

Add `HUGO_VERSION` to both production and preview environments.

---

## 13. Approval sequence

Do not merge until the checklist sign-off block is complete.

1. Operator runs local build, script preflight, and preview QA.
2. Sam Ray reviews FPPC footer source, AI translation disclosure source, Pillar 2 EmpowerSF claim, and Pillar 3 strike-fund disclosure.
3. Lauren reviews treasurer name, FPPC ID, trust-strip figures, donation route, and email forwarding.
4. Campaign manager confirms dormant endorsements route or active endorsements route.
5. Operator records exceptions, if any.

---

## 14. Merge and make live

After sign-off:

```bash
git checkout main
git pull --ff-only
git merge --no-ff phase1-v1.3.1-preflight
git push origin main
```

Cloudflare Pages deploys production from `main`.

Production smoke test:

```bash
curl -I https://turonsf.com/
curl -I https://turonsf.com/es/
curl -I https://turonsf.com/platform/uesf-questionnaire/
```

Expected:

```text
/                              200
/es/                           200 with noindex in HTML
/platform/uesf-questionnaire/  404 while inactive
```

Then open the site in a browser and repeat the critical CTA and language-switcher tests.

---

## 15. First-hour monitoring

In the first hour after production deploy:

| Surface | Check |
|---|---|
| Cloudflare Pages | production deployment green |
| Browser | no console errors on home + `/es/` + `/ar/` |
| Umami | pageviews arrive; manual CTA event arrives |
| ActBlue | donate click reaches correct committee URL with UTMs |
| Brevo | signup test succeeds and callback event fires |
| Action Network | volunteer link/form route opens with UTMs |
| Email | `info@turonsf.com` receives test email |
| Search posture | non-English placeholders are noindex |

---

## 16. Rollback

Preferred rollback:

```bash
git revert <merge_commit_sha>
git push origin main
```

Cloudflare redeploys the prior state.

Emergency rollback:

1. Open Cloudflare Pages → Deployments.
2. Select the last known-good production deployment.
3. Use rollback/redeploy controls.
4. Record the rollback reason in `docs/Phase1_Preflight_Checklist.md` or the campaign deployment log.

Rollback triggers:

```text
- Broken homepage rendering
- Incorrect FPPC footer or treasurer name
- Wrong ActBlue committee/donation route
- Placeholder non-English pages indexed or missing noindex
- Analytics script causing user-visible failure
- JS error blocks navigation or CTAs
```

---

## 17. Post-launch operating rhythm

Daily for first 7 days:

```text
- Review Umami conversion funnel
- Check pending-language notice views by language
- Review info@turonsf.com translation feedback
- Confirm backend UTM reports receive traffic
- Log any copy or route correction in git
```

Weekly during Phase 1:

```text
- Rank languages by pending-notice demand
- Pick next translation review target
- Re-run ./bin/preflight-check.sh after every content change
- Keep all claim/FPPC changes in Sam review queue before merge
```

— end of `Phase1_Build_GoLive_Guide.md`
