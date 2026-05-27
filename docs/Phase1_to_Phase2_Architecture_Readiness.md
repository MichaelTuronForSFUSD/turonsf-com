# Phase 1 → Phase 2 Architecture Readiness — turonsf.com v1.3.0

**Document role:** Pre-lock assessment. Answers two questions: (1) are post-launch adjustments easy with the current architecture? (2) is Phase 2 transition clean, or does the v1.3.0 architecture need rework first?
**Audience:** Michael Turon (operator), with sign-off scope for Sam Ray and Lauren Turon on counsel- and compliance-affecting changes.
**Pairs with:** `Phase1_Design_Red_JEC_Audit.md`, `Phase1_Analytics_Spec.md`, `Phase1_Preflight_Checklist.md`, `MANIFEST.md`.

---

## 1. Current architecture inventory

The v1.3.0 architecture rests on six load-bearing decisions. Each is documented; each enables or constrains specific Phase 2 moves.

| # | Decision | What it enables | What it locks |
|---|---|---|---|
| 1 | **Hugo + Cloudflare Pages static** | Zero-cost hosting, sub-100ms global LCP, atomic deploys via git push | Anything dynamic (forms, A/B, user state) must run on Cloudflare Workers or external services; no server-side rendering |
| 2 | **`translationByFileName` i18n mode** | Translations live next to source (`page.es.md` next to `page.md`); operator edits one folder | Switching to dir-based or multi-host i18n later requires moving every scaffold |
| 3 | **`data/translation_status.yaml` as single source of truth** | Four surfaces (hreflang, switcher, sitemap, AI disclosure) read one file; one YAML edit promotes a translation | A new surface that needs translation state must also read this file or stay in sync |
| 4 | **Direction A design tokens (LOCKED)** | Cohesive visual language across every page and language; consistent BW deadpan aesthetic | Cannot change `--navy-900`, `--accent`, `--cream-50`, or font choices without violating the Decisions Register |
| 5 | **i18n string tables (`themes/turon-civic/i18n/*.toml`)** | All visible text is a key; copy edits don't touch templates | Adding a string requires adding the key to all 7 language files (parity check needed) |
| 6 | **Umami + UTM analytics taxonomy (`Phase1_Analytics_Spec.md`)** | Funnel observable from day one; new CTAs auto-instrument via the `cta` shortcode | Any analytics platform swap (e.g., to Plausible or PostHog) requires re-implementing the shim and dashboards |

Backend integrations: Brevo (newsletter), ActBlue (donations), Action Network (volunteers), Cloudflare Turnstile (anti-bot). All four are HTTP-form-based; the architecture is integration-agnostic — if any backend is replaced, the change is one config line in `hugo.toml` `[params.cta_destinations]`.

---

## 2. Adjustability triage matrix

Every adjustment a campaign typically wants falls into one of four buckets.

### 2.1 One-edit changes (≤ 5 minutes, single file)

| Change | File | Why it's easy |
|---|---|---|
| CTA label text | `themes/turon-civic/i18n/{lang}.toml` for each language | One i18n key per CTA; all surfaces using the key update together |
| Hero subhead copy | Same as above | i18n-driven |
| Pillar body text | `content/platform/pillar-{N}.md` (English) + 6 scaffold variants | Markdown + frontmatter |
| ActBlue / Brevo / Action Network destination URL | `hugo.toml` `[params.cta_destinations]` | Single config map; shortcode reads it; every CTA picks it up |
| Election date countdown | i18n key in utility bar | Will need a Hugo template helper for live countdown when desired; ship-state is a static date |
| FPPC ID, treasurer name | i18n key in footer disclosure | Glossary contract preserves the literal across all 7 languages |
| Promote a translation from `placeholder` → `reviewed` | `data/translation_status.yaml` (one line) | Four surfaces re-render on next build |
| Activate Endorsements page | `content/endorsements.md` frontmatter: `is_active: true` + populate `data/endorsements.yaml` | One frontmatter flip + data rows |
| Activate UESF questionnaire | `content/platform/uesf-questionnaire.md` frontmatter | Same |
| Add a new endorser | `data/endorsements.yaml` append | YAML row |

### 2.2 Multi-file mechanical changes (5-30 minutes, scriptable)

| Change | Files touched | Why it's medium |
|---|---|---|
| Add a new page (e.g., `/press/`) | New `content/press.md` + 6 scaffold `.{lang}.md` files + 6 rows in `translation_status.yaml` | Same scaffold-generation script that built v1.3.0 (`/home/claude/gen_scaffolds.py` in the build env) can run again on a new page |
| Add a new nav link | `themes/turon-civic/i18n/*.toml` × 7 (label) + `hugo.toml` menu config + nav partial | Three places, all string-driven |
| Add a new Umami event | `Phase1_Analytics_Spec.md` (canonical spec) + `analytics.js` if it's a new pattern + partial that fires it | Spec doc keeps events from drifting across templates |
| Add a new CTA destination (e.g., a new lead-magnet form) | `hugo.toml` `[params.cta_destinations]` + i18n keys + shortcode usage | Shortcode handles UTM + event firing automatically |
| Re-add deferred letter + talk pages | Restore the 14 files + 12 `translation_status.yaml` entries + un-comment the i18n keys | Documented in `MANIFEST.md` §5 OIL Decision 4 + per-i18n-file deferral comments |
| Re-translate one page in one language with a new tool | The page's `.{lang}.md` body + frontmatter `translation_tool_primary` field; `translation_status.yaml` row promotes from `placeholder` → `ai_translated` → `reviewed` | Per the Translation Workflow doc |
| Bulk update copy across multiple pillars | i18n keys + per-pillar `.md` body | Scriptable with sed if needed |

### 2.3 Architectural changes (hours to days, design + counsel involvement)

| Change | What it requires | When to do it |
|---|---|---|
| Add a new language (e.g., Russian) | New entry in `hugo.toml` `[languages]`, new i18n TOML, new `llms.ru.txt`, 13+ new scaffold files, 13+ new `translation_status.yaml` rows, language switcher partial new option, font-stack consideration if non-Latin | Phase 2 only if SFUSD demographics shift or operator commits to expanded reach |
| Switch analytics platform | Re-implement shim against new platform's SDK; re-set up dashboards; preserve UTM scheme | Only if Umami fails on cost or feature; Plausible / PostHog are nearest peers |
| Restructure i18n mode (e.g., translationByFileName → translationByMultiHost) | Move every scaffold; rewrite `hugo.toml` `[languages]`; rewrite head-hreflang partial; sitemap regen | **Don't.** translationByFileName is the right choice for this scale; switching is gratuitous churn |
| Change Direction A tokens | Tokens.css.diff + every partial using them + visual QA + counsel sign-off on FPPC-surface changes | Locked per Decisions Register; would require a formal token-revision JEC cycle |
| Reorder the three pillars | `content/platform/pillar-{N}.md` filename + numbering + i18n + home template + every internal reference | Locked per Decisions Register; the order is a values statement |
| Add server-side dynamic features (e.g., real-time event RSVP) | Cloudflare Workers code + Workers KV / Durable Objects + new analytics for the Worker | Phase 3 candidate; Phase 2 stays static |

### 2.4 Locked decisions (require a formal Decisions Register update before touching)

These are not "hard to change" — they're "shouldn't change without explicit operator + counsel sign-off":

- Direction A design tokens (`--navy-900`, `--accent`, `--cream-50`, font choices)
- Trust strip Sequence F Option β ($72M cost savings at Royal Caribbean → Two kids / SFUSD parent through 2040 → HelloFresh → Cambridge order + financial figures)
- Three-pillar order (Special Ed → Budget Discipline → Teacher Retention)
- Hero copy structure (operator-credential anchored headline + three-pillar reference subhead + dual CTA)
- Role tag "Data Scientist, SFUSD Parent" — never JD/attorney/lawyer/Juris Doctor in any language
- FPPC §84305 footer string (Sam Ray batched review per language)
- AI translation disclosure text (D8 source — Sam Ray reviewed)
- info@turonsf.com canonical email
- FPPC ID 1482971 literal in every footer
- "No CMS, no translation widget" — markdown + git only
- Non-dismissible AI translation disclosure (no close button, no JS hide, no cookie hide)

---

## 3. Phase 2 likely scope — informational sketch

Phase 2 is not formally defined in any committed document. Based on the campaign timeline (Phase 1 ships May 2026, election November 3 2026), the operator's documented platform priorities, and the deferred surfaces noted in v1.3.0, Phase 2 candidates land roughly in this order:

| Tier | Phase 2 candidate | Architecture impact |
|---|---|---|
| **High-confidence Phase 2** | Re-add `/letters/uesf-2026-05-12/` once content is locked | Mechanical — 14 files restored, 12 yaml entries, un-comment i18n |
| | Re-add `/talk/` (Google Calendar booking) once content is locked | Mechanical — same pattern |
| | Activate `/endorsements/` as endorsements roll in | Frontmatter flip + data YAML rows |
| | Activate `/platform/uesf-questionnaire/` post Schmaus permission | Frontmatter flip + paste verbatim content |
| | Promote first language (Spanish) from placeholder → reviewed | Translation pipeline output; `translation_status.yaml` rows flip |
| | Pillar deep pages get pillar-specific newsletter CTAs (audit F-pillar-cta) | Hugo shortcode + i18n keys per pillar |
| | "Platform brief" PDF as lead magnet if F19 option (b) is chosen | Operator authors brief; Brevo automation sends on signup |
| **Likely Phase 2** | Press kit page with downloadable assets | New page + content type |
| | Event calendar (forums, candidate nights, voter Q&A) | New content type + date-aware templates |
| | Coalition partner page with logos and quotes | New page + data YAML |
| | News / blog page (campaign updates, public correction log rollups) | New content type + RSS feed |
| | Mature Umami dashboards (per-language conversion, per-pillar attention, translation-priority queue) | Configuration work in Umami, not in repo |
| **Possible Phase 2** | Embedded Brevo signup forms inline (vs. outbound link) | New embed partial; cookieless verification with Turnstile |
| | Donation amount presets on hero CTA ("Donate $25 · $50 · $100") | ActBlue preset URLs + hero variant template |
| | Endorsement quote carousel | New partial + content type |
| **Phase 3 candidates** | A/B testing on CTA copy | Cloudflare Workers edge logic |
| | Real-time event RSVP forms | Cloudflare Workers + KV |
| | Interactive budget simulator | JS widget; potentially React/Svelte if reactive |

**Key finding:** every High-confidence and Likely Phase 2 item lands inside the existing architecture without re-architecting. The architecture pays for itself across the next two quarters.

---

## 4. Pre-lock action items — gaps to close BEFORE going live

Three pieces of work close the remaining gaps. Each is independently shippable; none blocks the others.

### 4.1 Pre-lock action A — wire the analytics shortcode + shim

**Status:** `Phase1_Analytics_Spec.md` ships in v1.3.0. The `cta` shortcode + `analytics.js` shim are specified but not yet in the theme.
**Estimated effort:** 1-2 hours.
**Action:** Add `themes/turon-civic/layouts/shortcodes/cta.html` and `themes/turon-civic/assets/js/analytics.js` per the spec. Convert every CTA in `layouts/index.html` to use the shortcode. Add the `defer` script tag to the base template.
**Why pre-lock:** Without this, every CTA in the launch site lacks UTM parameters and event firing. Day 1 of launch produces zero observable funnel data. The audit's F9 + F10 + F22 are not closed in code, only in spec.
**Owner:** Operator.

### 4.2 Pre-lock action B — verify Spanish backend URL parameters

**Status:** audit finding F23 — ActBlue, Action Network, and Brevo all support Spanish-language form configurations, but the exact URL parameter format must be verified against current backend docs.
**Estimated effort:** 30 minutes (read three docs, test three URLs on preview).
**Action:** Confirm parameter format with each backend's current documentation. Update `hugo.toml` `[params.cta_destinations]` to thread the correct parameter when `Page.Lang == "es"`. Update `Phase1_Analytics_Spec.md` §6 with the verified parameter values.
**Why pre-lock:** Spanish-speaking visitors who hit donate / volunteer / newsletter CTAs from a Spanish page should land on a Spanish backend form. Without this, conversion rate drops for the largest non-English audience (SFUSD demographics: 64.76% EL is Spanish).
**Owner:** Operator + lightweight Lauren review for ActBlue (treasurer surface).

### 4.3 Pre-lock action C — decide F19 lead-magnet question

**Status:** carried forward from audit. Current mockup r2 ships option (a) soft CTA "Get campaign updates from Michael" because that's safe-by-default.
**Estimated effort:** Decision = zero. Option (b) execution = 2-3 hours operator drafting + Sam Ray review.
**Action:** Operator decides:
- (a) Ship the soft CTA as-is. Lower conversion. Zero additional work.
- (b) Commit to producing a one-page Phase 1 platform brief. Upgrade the CTA copy to "Get Michael's platform brief in your inbox." Configure Brevo to send the brief on signup confirmation. 2-3× conversion lift per civic-campaign benchmarks.
**Why pre-lock:** Once the brief is live, you can't quietly retract the promise. The decision belongs before lock so the visitor experience is consistent from day one.
**Owner:** Michael Turon. Sam Ray reviews the brief content if option (b) chosen.

### 4.4 Pre-lock action D — Sam Ray batched review

**Status:** four items queued for Sam:
- D8 AI translation disclosure source (final 18-word English)
- D9 FPPC footer per-language reference translations (6 languages)
- Pillar 2 "most expensive board-oversight miss" claim phrasing
- Pillar 3 strike-fund disclosure phrasing

**Estimated effort:** Sam ~2 hours; operator ~30 minutes integrating Sam's notes.
**Action:** Send Sam the four items as a single batched review request. Expected 48-72 hour turnaround. Apply Sam's notes; re-review.
**Why pre-lock:** None of these are recoverable without re-deploy if Sam later flags. Front-load the counsel review now.
**Owner:** Michael + Sam.

### 4.5 Pre-lock action E — Lauren treasurer review

**Status:** trust strip credentials + FPPC footer treasurer name + financial figures.
**Estimated effort:** Lauren ~30 minutes.
**Action:** Walk Lauren through the rendered Cloudflare Pages preview. Confirm: trust strip figures unchanged, FPPC ID 1482971 in every footer in every language, treasurer name "Lauren Turon" preserved Latin-script in every language, info@turonsf.com routing tested.
**Why pre-lock:** Treasurer is FPPC-required attestation; her sign-off goes on the Phase1_Preflight_Checklist §10 block.
**Owner:** Michael + Lauren.

---

## 5. Phase 2 readiness verdict

**Architecture passes Phase 2 readiness.** Of the Phase 2 candidate items in §3:

- **Zero** require architectural rework.
- **All** Phase 2 candidates land inside the existing template + i18n + data + analytics structures.
- **Two** Phase 3 candidates (A/B testing, server-side dynamic) would require Cloudflare Workers; deferred to Phase 3 explicitly and not blocking Phase 2.

The five pre-lock action items in §4 are NOT architectural blockers — they're operational completion items that should land before going live for funnel observability (A), multilingual conversion quality (B), CTA truthfulness (C), counsel defensibility (D), and treasurer attestation (E).

**Lock recommendation: green light, conditional on completing actions A, B, D, E pre-deploy. Action C can ship at option (a) and upgrade to option (b) in Phase 1.5 without architectural change.**

---

## 6. Adjustment cookbook — common edits with file paths

For each common adjustment scenario, the file(s) to touch and a one-line rationale.

### Recipe 1 — Change a CTA label (e.g., "Get updates" → "Subscribe")
```
themes/turon-civic/i18n/en.toml      → newsletter_cta_primary = "Subscribe"
themes/turon-civic/i18n/es.toml      → newsletter_cta_primary = "Suscríbete"
themes/turon-civic/i18n/zh-Hant.toml → newsletter_cta_primary = "訂閱"
themes/turon-civic/i18n/zh-Hans.toml → newsletter_cta_primary = "订阅"
themes/turon-civic/i18n/tl.toml      → newsletter_cta_primary = "Mag-subscribe"
themes/turon-civic/i18n/vi.toml      → newsletter_cta_primary = "Đăng ký"
themes/turon-civic/i18n/ar.toml      → newsletter_cta_primary = "اشترك"
```
Build, preview, deploy. ~3 minutes including all 7 language updates.

### Recipe 2 — Activate Endorsements (when endorsements land)
```
content/endorsements.md             → frontmatter: is_active: true
data/endorsements.yaml              → append endorser rows
```
Build, preview, deploy. The dormant signup form converts to the endorsement-list view; conditional rendering in the layout template handles the switch.

### Recipe 3 — Promote Spanish home page from placeholder → reviewed
```
data/translation_status.yaml        → "/::es": "reviewed"
content/_index.es.md                → translation_status: "reviewed" in frontmatter
                                       review_log entries appended for Sam Ray + Lauren
```
Build. Hreflang now emits Spanish; sitemap now lists Spanish home; AI translation disclosure renders (was pending notice); page is live in production.

### Recipe 4 — Add a new page (`/press/`)
```
content/press.md                    → new English source page
content/press.es.md                 → scaffold (use gen_scaffolds.py or copy pattern)
content/press.zh-Hant.md            → scaffold
content/press.zh-Hans.md            → scaffold
content/press.tl.md                 → scaffold
content/press.vi.md                 → scaffold
content/press.ar.md                 → scaffold
data/translation_status.yaml        → append 6 new rows: /press/::{lang}: "placeholder"
themes/turon-civic/i18n/*.toml × 7  → add nav label key "press" if linking from nav
hugo.toml                           → add to menu config if linking from nav
```
~10 minutes. Mechanical.

### Recipe 5 — Switch ActBlue donate URL (e.g., new donation page slug)
```
hugo.toml                           → [params.cta_destinations].donate = "<new URL>"
```
Every donate CTA on every page in every language picks up the new URL on next build. ~30 seconds.

### Recipe 6 — Add a new analytics event (e.g., `press_kit_download_click`)
```
docs/Phase1_Analytics_Spec.md       → document the event in §1
themes/turon-civic/layouts/.../partials/press-kit-link.html → add data-event="press_kit_download_click"
                                                              data-source="<source>" attributes
                                                              (analytics.js auto-wires on click)
```
No JS code change. The shim already handles any `[data-event]` element. ~5 minutes.

### Recipe 7 — Re-enable a deferred page (letter or talk in Phase 2)
```
content/letters/uesf-2026-05-12/index.md       → restore from git history (was deferred in v1.3.0)
content/letters/uesf-2026-05-12/index.*.md     → restore all 6 scaffolds
data/translation_status.yaml                    → un-comment / append the 6 entries
themes/turon-civic/i18n/*.toml                  → remove the "DEFERRED FROM v1.3.0" comment lines above [letters] key
```
~15 minutes if the source content is locked. Documented in MANIFEST §5 OIL Decision 4.

### Recipe 8 — Activate a new lead magnet (e.g., switch to F19 option b "platform brief")
```
themes/turon-civic/i18n/en.toml + es/zh-Hant/zh-Hans/tl/vi/ar    → newsletter_cta_primary key value change
brevo dashboard                                                   → configure auto-responder to send PDF on signup
docs/Phase1_Analytics_Spec.md                                     → document the lead magnet in §5 (newsletter_signup_submit dim list_id)
(no template change needed; CTA picks up new copy automatically)
```
~30 minutes including Brevo config.

### Recipe 9 — Update FPPC footer string (e.g., committee name change — unlikely but documented)
```
themes/turon-civic/i18n/en.toml      → fppc_footer = "<new English string>"
themes/turon-civic/i18n/es.toml      → fppc_footer = "<new Spanish per Sam Ray>"
                                       (same for all 7 languages, Sam Ray reviews each)
docs/Deliverable_9_FPPC_Footer_Disclosure.md → update the source doc + Sam Ray review notation
```
Sam-Ray-blocked. ~24-48 hours to land due to review.

### Recipe 10 — Add a new language (Phase 2 expansion candidate)
```
hugo.toml                                                  → [languages] new entry with weight + dir + languageName
themes/turon-civic/i18n/<lang>.toml                        → new TOML, copy structure from en.toml, mark "# AWAITING TRANSLATION"
static/llms.<lang>.txt                                     → new llms file
content/*.{lang}.md                                        → generate 11 unconditional scaffolds (use gen_scaffolds.py)
data/translation_status.yaml                               → append 11 rows: /*/::lang: "placeholder"
themes/turon-civic/layouts/partials/language-switcher.html → add new <option>
themes/turon-civic/static/css/tokens.css                   → font stack override if non-Latin
docs/Phase1_Translation_Workflow.md                        → update Section 2 + 4 with new language guidance
layouts/sitemap.xml                                        → no change (data-driven)
```
~2-3 hours including font-stack research. Mechanical.

---

## 7. What's NOT in scope of this readiness assessment

To bound expectations:

- **Phase 2 roadmap commitment:** §3 is informational only. The operator decides what actually lands in Phase 2 based on campaign needs in July-August 2026.
- **Brevo / ActBlue / Action Network feature comparisons:** the architecture is integration-agnostic; vendor swaps are possible but not the subject of this doc.
- **SEO strategy beyond hreflang correctness:** Phase 1 ships the technical SEO foundation; ranking optimization is content + outreach work.
- **Paid traffic strategy (Google Ads, Meta, etc.):** UTM scheme supports it but campaign decisions are operator scope.
- **Email list management beyond Brevo signup:** segmentation, drip campaigns, transactional emails are Brevo configuration work.

---

## 8. Sign-off

| Role | Name | Scope | Date | Signature |
|---|---|---|---|---|
| Operator | Michael Turon | Full readiness assessment, lock decision | 2026-05-12 | drafted |
| Counsel | Sam Ray | Pre-lock action D batched review items | _pending_ | _pending_ |
| Treasurer | Lauren Turon | Pre-lock action E preview walkthrough | _pending_ | _pending_ |

**Pre-lock readiness verdict:** GREEN LIGHT conditional on actions A, B, D, E completing pre-deploy. Action C ships option (a) by default; option (b) upgrade path available in Phase 1.5 without architectural change.

— end of `Phase1_to_Phase2_Architecture_Readiness.md`
