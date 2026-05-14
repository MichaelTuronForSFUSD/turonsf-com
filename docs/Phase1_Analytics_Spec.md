# Phase 1 Analytics Spec — turonsf.com v1.3.0

**Document role:** Canonical specification for every Umami event the v1.3.0 site fires, the UTM scheme on every outbound CTA, and the Hugo shortcode pattern that wires events into templates without per-template duplication.
**Pairs with:** `Phase1_Design_Red_JEC_Audit.md` (finding F9, F10, F22), `turonsf_v1.3.0_mockup_r2.html` (telemetry HUD demonstrates every event in this spec).
**Ownership:** Operator wires events. Sam Ray reviews any event that records personal identifiers (none of them do; this is a deliberate design choice).

---

## 1. Event taxonomy

Every event is dimensioned by `language` (the active page language) and `viewport` (`desktop` or `mobile`), which the analytics shim attaches automatically. Per-event dimensions below are in addition to those two.

### 1.1 Conversion events (Phase 1 priority — list-building first, donation second)

| Event | Fires when | Per-event dimensions | Notes |
|---|---|---|---|
| `newsletter_cta_click` | User clicks any newsletter-signup CTA | `source` (hero / footer / pillar-1 / pillar-2 / pillar-3 / ai_disclosure) | Click event, **not** the conversion event. Pairs with `newsletter_signup_submit`. |
| `newsletter_signup_submit` | Brevo form submission succeeds (Brevo success callback) | `source` (same set as above), `list_id` (Brevo list segment) | **The conversion event.** Drives Phase 1 KPI: cold-visitor-to-list rate. |
| `donate_cta_click` | User clicks any donate link | `source` (nav / hero / footer / pillar / utility) | Click event. ActBlue confirmation lives on ActBlue, not on turonsf; conversion attribution flows via UTM. |
| `volunteer_cta_click` | User clicks any volunteer CTA | `source` (hero / footer / pillar) | Conversion event lives on Action Network. |
| `email_contact_click` | User clicks any `mailto:info@turonsf.com` link | `source` (ai_disclosure / pending_notice / footer / contact_page) | Low-volume but high-quality leads. |

### 1.2 Engagement events (signal for content + message optimization)

| Event | Fires when | Per-event dimensions | Notes |
|---|---|---|---|
| `pillar_click` | User clicks any pillar deep-link from home | `pillar` (1 / 2 / 3) | Per-pillar interest signal. Surfaces whether locked pillar order matches voter attention. |
| `platform_link_click` | User clicks the tertiary "read the full platform" link in hero | `source` (hero_tertiary) | Measures depth interest separate from pillar-specific clicks. |
| `hero_cta_primary_view` | Hero primary CTA enters viewport ≥ 50% visibility (IntersectionObserver, first time per session) | — | **Impression event.** Without this, you have clicks but not CTR. CTR = `newsletter_cta_click(source=hero)` / `hero_cta_primary_view`. |
| `trust_strip_view` | Trust strip enters viewport ≥ 50% visibility (first time per session) | — | Measures whether visitors absorb the trust strip before bouncing. |
| `scroll_depth_75` | User scrolls to 75% page depth | `page` (URL path) | Built-in Umami. |
| `scroll_depth_100` | User scrolls to 98% page depth | `page` | Built-in Umami. Note: threshold 0.98 not 1.0 because footer always renders below 1.0. |

### 1.3 Multilingual events (translation-priority demand signal)

| Event | Fires when | Per-event dimensions | Notes |
|---|---|---|---|
| `language_switcher_open` | User opens the language switcher dropdown | `from_language` | Consideration signal. |
| `language_switcher_select` | User picks a language from the switcher | `from_language`, `to_language` | Action signal. `from → to` reveals demand routes. |
| `language_pending_notice_view` | Pending notice enters viewport ≥ 30% visibility on a placeholder page | `page` | **Translation-priority demand signal.** N views per language per week = where to translate next. |
| `language_pending_to_english_click` | User clicks "Read in English" link from pending notice OR from switcher's read-in-english promo | `from_language`, `source` (pending_notice / switcher) | Fallback engagement signal. |

### 1.4 Navigation events (used for funnel attribution; low signal alone)

| Event | Fires when | Per-event dimensions | Notes |
|---|---|---|---|
| `nav_click` | User clicks any primary nav link | `source` (platform / endorsements / volunteer / contact) | Useful for path analysis; not a conversion. |

**Total: 14 events.** None record PII. None require user consent under FPPC or California privacy law because no personal identifiers leave the user's browser via this taxonomy (Umami is cookieless by design, and the email + ID identifiers exist only on backend forms, not in the event stream).

---

## 2. UTM scheme on outbound CTAs

Every link that leaves turonsf.com for a campaign backend carries the four UTM parameters below. Source attribution flows back: ActBlue dashboards, Brevo segments reports all surface the `utm_*` values.

### 2.1 Parameter spec

| Parameter | Value | Notes |
|---|---|---|
| `utm_source` | `turonsf` | Always the literal `turonsf`. Identifies our site to the destination platform's reports. |
| `utm_medium` | `web` | Always `web` for the canonical site. Email campaigns would use `email`; social would use `social-{platform}`. |
| `utm_campaign` | `phase1` | Phase identifier. Bumps to `phase2` when Phase 2 starts. |
| `utm_content` | `{cta_location}-{language}` | The specific CTA. Examples: `hero-en`, `hero-es`, `pillar1-zh-Hant`, `footer-ar`, `nav-en`, `utility-ar`. |

### 2.2 Per-CTA reference table

| Surface | `utm_content` value | Destination |
|---|---|---|
| Hero primary newsletter | `hero-{lang}` | Brevo signup form |
| Hero secondary donate link | `hero-donate-{lang}` | ActBlue |
| Hero tertiary platform link | `hero-platform-{lang}` | Internal (no UTM needed for internal links, but track it anyway for funnel analysis) |
| Nav donate button | `nav-donate-{lang}` | ActBlue |
| Footer newsletter link | `footer-newsletter-{lang}` | Brevo |
| Footer volunteer link | `footer-volunteer-{lang}` | Action Network |
| Footer donate link | `footer-donate-{lang}` | ActBlue |
| AI disclosure email link | `ai-disclosure-{lang}` | mailto (UTM survives in subject if mail client preserves it; primarily for backend log search) |
| Pending notice email link | `pending-notice-{lang}` | mailto |
| Pillar N CTA (when pillar pages add newsletter/donate CTAs in v1.3.1) | `pillar{N}-{lang}` | Brevo / ActBlue |

### 2.3 Worked example

A Spanish-speaking visitor clicks the hero donate link on the homepage. The URL they hit:

```
https://secure.actblue.com/donate/turonsf?utm_source=turonsf&utm_medium=web&utm_campaign=phase1&utm_content=hero-donate-es
```

ActBlue records the donation against `utm_content=hero-donate-es`. The campaign dashboard shows: "this $50 donation came from a Spanish hero donate click on the homepage." Phase 1 optimization decisions get the right signal.

---

## 3. Hugo implementation pattern

To avoid scattering UTM logic across templates, the campaign theme adds one shortcode that wraps every outbound CTA. Templates call the shortcode; the shortcode appends UTM + fires the Umami event.

### 3.1 Shortcode: `themes/turon-civic/layouts/shortcodes/cta.html`

```go-html-template
{{/*
  cta.html — wraps every campaign CTA with UTM tagging + Umami event firing.

  Usage in templates / content:
    {{< cta
      kind="newsletter"           {{/* newsletter | donate | volunteer | platform | email */}}
      source="hero"               {{/* hero | footer | nav | pillar-N | utility | ai_disclosure */}}
      label_key="newsletter_cta"  {{/* i18n key for the visible label */}}
      style="primary"             {{/* primary | secondary | tertiary | text */}}
    >}}

  The shortcode resolves the destination URL from site config, appends UTMs,
  adds data-event + data-source attributes for the Umami shim, and renders the
  label via i18n. Operator never hand-codes UTM strings or event names.
*/}}
{{ $kind := .Get "kind" }}
{{ $source := .Get "source" }}
{{ $labelKey := .Get "label_key" }}
{{ $style := .Get "style" | default "primary" }}
{{ $lang := .Page.Lang }}

{{/* Resolve destination URL from site config (set in hugo.toml) */}}
{{ $destinations := .Site.Params.cta_destinations }}
{{ $baseURL := index $destinations $kind }}

{{/* Append UTM parameters */}}
{{ $utmContent := printf "%s-%s" $source $lang }}
{{ $separator := "?" }}
{{ if (in $baseURL "?") }}{{ $separator = "&" }}{{ end }}
{{ $fullURL := printf "%s%sutm_source=turonsf&utm_medium=web&utm_campaign=phase1&utm_content=%s" $baseURL $separator $utmContent }}

{{/* Event name conventions */}}
{{ $eventName := "" }}
{{ if eq $kind "newsletter" }}{{ $eventName = "newsletter_cta_click" }}
{{ else if eq $kind "donate" }}{{ $eventName = "donate_cta_click" }}
{{ else if eq $kind "volunteer" }}{{ $eventName = "volunteer_cta_click" }}
{{ else if eq $kind "email" }}{{ $eventName = "email_contact_click" }}
{{ else if eq $kind "platform" }}{{ $eventName = "platform_link_click" }}
{{ end }}

<a href="{{ $fullURL }}"
   class="cta cta--{{ $style }} cta--{{ $kind }}"
   data-event="{{ $eventName }}"
   data-source="{{ $source }}">
  {{ i18n $labelKey }}
  {{ if or (eq $style "primary") (eq $style "secondary") }}
    <span class="cta__arrow" aria-hidden="true">→</span>
  {{ end }}
</a>
```

### 3.2 Site config additions to `hugo.toml`

```toml
[params.cta_destinations]
  newsletter = "https://sibforms.com/serve/MUIFAA..."          # Brevo embed URL — operator confirms before deploy
  donate     = "https://secure.actblue.com/donate/turonsf"      # ActBlue donate page
  volunteer  = ""  # Action Network form
  email      = "mailto:info@turonsf.com"
  platform   = "/platform/"
```

Operator updates one place; every CTA in every template + every page in every language picks up the new destination + UTM scheme automatically.

### 3.3 Example template usage

In `themes/turon-civic/layouts/index.html` (home template):

```go-html-template
<div class="hero__ctas">
  {{< cta
    kind="newsletter"
    source="hero"
    label_key="newsletter_cta_primary"
    style="primary"
  >}}
  {{< cta
    kind="donate"
    source="hero"
    label_key="donate_link_secondary"
    style="text"
  >}}
</div>
```

Three lines per CTA. No UTM strings hand-coded. No event names typed twice.

---

## 4. Umami shim — production code

The shim is one JavaScript file shipped to every page. The mockup demonstrates the exact pattern; production swaps the `console.log` for the live Umami call.

### 4.1 `themes/turon-civic/assets/js/analytics.js`

```javascript
/* analytics.js — Umami event shim for turonsf.com v1.3.0+ */

(function(){
  const seen = new Set();

  function track(eventName, dims = {}) {
    const lang = document.documentElement.getAttribute('lang') || 'en';
    const viewport = window.innerWidth < 768 ? 'mobile' : 'desktop';
    const fullDims = { language: lang, viewport: viewport, ...dims };

    if (window.umami && typeof window.umami.track === 'function') {
      window.umami.track(eventName, fullDims);
    } else if (typeof console !== 'undefined' && console.log) {
      console.log('[umami:noop]', eventName, fullDims);
    }
  }

  /* Click events on any [data-event] element */
  document.addEventListener('click', (e) => {
    const el = e.target.closest('[data-event]');
    if (!el) return;
    const dims = {};
    if (el.dataset.source) dims.source = el.dataset.source;
    if (el.dataset.pillar) dims.pillar = el.dataset.pillar;
    if (el.dataset.to) dims.to_language = el.dataset.to;
    track(el.dataset.event, dims);
  });

  /* Impression events via IntersectionObserver */
  function observeImpression(selector, eventName, threshold = 0.5) {
    const el = document.querySelector(selector);
    if (!el) return;
    const io = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting && entry.intersectionRatio >= threshold && !seen.has(eventName)) {
          seen.add(eventName);
          track(eventName, {});
        }
      });
    }, { threshold });
    io.observe(el);
  }

  observeImpression('[data-cta-primary]', 'hero_cta_primary_view', 0.5);
  observeImpression('[data-trust-strip]', 'trust_strip_view', 0.5);
  observeImpression('[data-pending-notice]:not([style*="display: none"])', 'language_pending_notice_view', 0.3);

  /* Scroll depth */
  let d75 = false, d100 = false;
  window.addEventListener('scroll', () => {
    const pct = (window.scrollY + window.innerHeight) / document.documentElement.scrollHeight;
    if (!d75 && pct >= 0.75) { d75 = true; track('scroll_depth_75', { page: location.pathname }); }
    if (!d100 && pct >= 0.98) { d100 = true; track('scroll_depth_100', { page: location.pathname }); }
  }, { passive: true });

})();
```

Hugo includes this via:

```go-html-template
{{ $analytics := resources.Get "js/analytics.js" | resources.Minify | resources.Fingerprint }}
<script defer src="{{ $analytics.RelPermalink }}" integrity="{{ $analytics.Data.Integrity }}"></script>
```

`defer` plus fingerprint = no render-blocking + cache-busting on every change.

---

## 5. Newsletter signup submit (the conversion event)

`newsletter_cta_click` fires on click; the actual conversion `newsletter_signup_submit` fires only after Brevo confirms the submission. Brevo supports a JavaScript success callback on its embed form. Wire it like:

```javascript
/* In analytics.js or in the partial that embeds the Brevo form */
window.addEventListener('sib_form_success', (e) => {
  const source = e.detail?.source || 'unknown';
  const listId = e.detail?.list_id || '';
  if (window.umami) {
    window.umami.track('newsletter_signup_submit', {
      source: source,
      list_id: listId,
      language: document.documentElement.lang,
      viewport: window.innerWidth < 768 ? 'mobile' : 'desktop'
    });
  }
});
```

The `source` dimension must be passed from the form embed (Brevo lets you add hidden fields). Hugo shortcode that embeds Brevo forms threads the `source` through to the hidden field automatically.

---

## 6. Pre-deploy validation

Before merging to main, the operator confirms:

| # | Check | Method |
|---|---|---|
| 1 | Every CTA renders with `data-event` and `data-source` attributes | `grep -E 'href=' public/index.html | grep -v 'data-event'` should return no campaign-CTA matches |
| 2 | Every outbound CTA URL contains all four UTM parameters | `grep -oE 'href="https://(secure.actblue|actionnetwork|sibforms)[^"]*"' public/index.html | grep -v 'utm_source=turonsf'` should be empty |
| 3 | `analytics.js` loads on every page | View source on any page; confirm `<script defer src="…analytics…js">` present |
| 4 | Umami `data-website-id` matches the live property | Confirm against Umami Cloud dashboard before deploy |
| 5 | Brevo success callback fires `newsletter_signup_submit` | Submit test form on preview build; confirm Umami event lands |
| 6 | ActBlue Spanish form URL parameter verified (F23) | Confirm with current ActBlue docs; document in this spec when verified |
| 7 | Action Network Spanish form URL parameter verified (F23) | Same |
| 8 | Brevo Spanish-language form configuration verified (F23) | Same |
| 9 | Scroll depth events fire (test on preview) | Scroll preview page; confirm `scroll_depth_75` + `scroll_depth_100` in Umami |
| 10 | IntersectionObserver impressions fire only once per session | Load page, scroll trust strip into view, scroll past, scroll back; only one `trust_strip_view` event |

The first two checks are scriptable. Add to CI as a build-time assertion: if a campaign-CTA URL ships without UTMs, the build fails. That guarantee outlasts operator memory.

---

## 7. Dashboards to set up before lock

Umami's default dashboard isn't optimized for conversion analysis. Set up three custom views in Umami:

1. **Phase 1 conversion funnel:** `newsletter_cta_click` impressions → `newsletter_cta_click` clicks → `newsletter_signup_submit`. Per language. Per source. CTR per source.
2. **Translation demand priority:** `language_pending_notice_view` count per language, weekly. Sorted descending. Drives translation completion order.
3. **Pillar attention:** `pillar_click` count per pillar, per language. Reveals message resonance.

The three dashboards take ~30 minutes to configure in Umami Cloud. Set them up before first deploy so the first week of data is observable from day one.

---

## 8. Document version

- **v1.0** — May 12, 2026. Ships with v1.3.0. Closes audit change-list items F9, F10, F22. Pairs with `Phase1_Design_Red_JEC_Audit.md`.
- **Next revision trigger:** when Brevo / ActBlue / Action Network language URL parameters are verified (F23), or when Phase 2 introduces new events.

— end of `Phase1_Analytics_Spec.md`
