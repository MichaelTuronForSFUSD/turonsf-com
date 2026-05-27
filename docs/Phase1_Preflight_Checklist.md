# Phase 1 Preflight Checklist — turonsf.com v1.3.0

**Document role:** Pre-deploy verification gate. Every item must pass before merging `phase1-7lang-build` → `main`. Items marked **BLOCKING** halt the deploy; items marked **WARN** allow deploy with a logged exception.
**Operator:** Michael Turon. Reviewers: Sam Ray (counsel), Lauren Turon (treasurer).
**Pairs with:** `Phase1_Translation_Workflow.md`, `Phase1_JEC_Scorecard.md`.

This checklist assumes:
- v1.3.0 diffs applied to a clean checkout of the v1.2.0 main.
- All 66 scaffold files in `content/` (60 unconditional + 6 conditional for `/platform/uesf-questionnaire/`).
- All 7 i18n string tables in `themes/turon-civic/i18n/` (with `[letters]` and `[talk]` keys annotated as deferred from v1.3.0 but retained for future re-enable).
- Three new partials in `themes/turon-civic/layouts/partials/`.
- New `layouts/sitemap.xml`.
- Updated `static/robots.txt`, 7 new `static/llms.{lang}.txt`.
- `data/translation_status.yaml` with all 66 entries at `placeholder`.
- `data/endorsements.yaml` empty.
- Letter (`/letters/uesf-2026-05-12/`) and talk (`/talk/`) pages **deferred from v1.3.0 scope** (May 12 OIL decision). Pages are not in this bundle; their scaffolds are not in this bundle; their `translation_status.yaml` entries are not in this bundle. Re-add in v1.3.1+.

Walk top to bottom. Note the result in column 3 (✅ / ❌ / ⚠️).

---

## Section 1 — Build integrity

| # | Check | Result |
|---|---|---|
| 1.1 | `hugo --minify --logLevel warn` exits 0 with zero warnings. **BLOCKING.** | |
| 1.2 | Build produces seven language outputs in `public/` — English at root, `es/`, `zh-Hant/`, `zh-Hans/`, `tl/`, `vi/`, `ar/`. **BLOCKING.** | |
| 1.3 | `public/sitemap.xml` validates against `https://www.sitemaps.org/schemas/sitemap/0.9` via `xmllint --noout --schema sitemap.xsd public/sitemap.xml`. **BLOCKING.** | |
| 1.4 | `public/sitemap.xml` lists every English page; lists no non-English pages on first deploy (all at `placeholder`). **BLOCKING.** | |
| 1.5 | `public/robots.txt` preserves the eleven-bot AI allowlist from v1.2.0 unchanged. **BLOCKING.** | |
| 1.6 | Seven `public/llms.{lang}.txt` files present and well-formed. **BLOCKING.** | |
| 1.7 | No `[TODO]`, `XXX`, or `FIXME` markers survive into rendered `public/` HTML. `grep -rEn "TODO\|XXX\|FIXME" public/` returns no results. **BLOCKING.** | |
| 1.8 | Build wall time on Mac Studio M4 Max is within 2× v1.2.0 baseline. **WARN.** | |
| 1.9 | No new external CDN dependency introduced; all assets local. **BLOCKING.** | |

## Section 2 — Content integrity (English source)

| # | Check | Result |
|---|---|---|
| 2.1 | All v1.2.0 page URLs resolve unchanged (home, /about/, /platform/, /platform/pillar-1/, /platform/pillar-2/, /platform/pillar-3/, /endorsements/, /volunteer/, /donate/, /contact/). **BLOCKING.** | |
| 2.2 | Hero copy structure unchanged from v1.2.0 (operator-credential anchored headline; three-pillar reference subheadline; dual CTA). **BLOCKING.** | |
| 2.3 | Three-pillar order preserved: Special Education → Budget Discipline → Teacher Retention. **BLOCKING.** | |
| 2.4 | Trust strip Sequence F Option β intact: $72M cost savings at Royal Caribbean → Two kids / SFUSD parent through 2040 → HelloFresh −$33M→+$9M → Cambridge. DOM order unchanged. **BLOCKING.** | |
| 2.5 | All four trust-strip financial figures render with the exact v1.2.0 strings (no recomputation, no rephrasing). **BLOCKING.** | |
| 2.6 | `/endorsements/` renders dormant copy + two signup forms because `is_active: false` and `data/endorsements.yaml` empty. **BLOCKING.** | |
| 2.7 | `/platform/uesf-questionnaire/` returns 404 because `is_active: false`. Not in nav. Not in sitemap. **BLOCKING.** | |
| 2.8 | Email canonical `info@turonsf.com` in every page footer. **BLOCKING.** | |
| 2.9 | FPPC ID `1482971` literal string in every page footer. **BLOCKING.** | |
| 2.10 | Role tag `"Data Scientist, SFUSD Parent"` — never JD, attorney, lawyer, or Juris Doctor anywhere in English source. `grep -rEi "juris doctor\|attorney\|lawyer\|\bJD\b" content/ themes/` returns no matches inside renderable content. **BLOCKING.** | |
| 2.11 | All English page Flesch Reading Ease ≥ 75 (run `vale` with the readability rule or equivalent). **WARN.** | |

## Section 3 — Visual integrity

Walk each page on (a) iPhone 14 viewport, (b) desktop 1440px viewport, in Safari and Chrome.

| # | Check | Result |
|---|---|---|
| 3.1 | No horizontal scroll on any page on iPhone 14 viewport. **BLOCKING.** | |
| 3.2 | Direction A tokens unchanged: `--navy-900`, `--accent`, `--cream-50`, font choices. `git diff main themes/turon-civic/static/css/tokens.css \| grep -E "^-.*(--navy-900\|--accent\|--cream-50)"` returns no deletions of these values. **BLOCKING.** | |
| 3.3 | Layout pattern unchanged on every existing v1.2.0 page (visual diff vs production). **BLOCKING.** | |
| 3.4 | Language switcher visible on every page on mobile and desktop. **BLOCKING.** | |
| 3.5 | Language switcher tap targets ≥ 44×44 px on mobile. **BLOCKING.** | |
| 3.6 | Language switcher renders each language name in its own script (Español / 繁體中文 / 简体中文 / Tagalog / Tiếng Việt / العربية / English). **BLOCKING.** | |
| 3.7 | AI translation disclosure does NOT render on English pages. **BLOCKING.** | |
| 3.8 | Trust-strip dollar figures render as Latin-script digits on every page in every language. **BLOCKING.** | |
| 3.9 | No FOUC (flash of unstyled content) on initial paint on any page. **WARN.** | |
| 3.10 | Page weight on mobile ≤ 100 KB transferred per page (gzipped). **WARN.** | |

## Section 4 — SEO + internationalization correctness

| # | Check | Result |
|---|---|---|
| 4.1 | English canonical URL has no `hreflang` siblings emitted for non-English pages (because all are `placeholder` at first deploy). **BLOCKING.** | |
| 4.2 | English pages emit `<link rel="alternate" hreflang="en" href="…" />` self-reference and `<link rel="alternate" hreflang="x-default" href="…" />`. **BLOCKING.** | |
| 4.3 | Every non-English page emits `<meta name="robots" content="noindex, follow" />` because all are `placeholder`. **BLOCKING.** | |
| 4.4 | Every non-English page emits `<link rel="canonical" href="…english source…" />` pointing to the English canonical of THAT page (not site home). **BLOCKING.** | |
| 4.5 | Sitemap contains only English entries on first deploy. **BLOCKING.** | |
| 4.6 | When `data/translation_status.yaml` flips a page-language to `reviewed`, the next build adds that page to the sitemap and emits hreflang. Test with one canary entry (e.g., `/about/::es` → `reviewed`) and verify before reverting. **BLOCKING.** | |
| 4.7 | `lang` attribute on `<html>` matches the page language for every rendered page. **BLOCKING.** | |
| 4.8 | `dir="rtl"` on `<html>` for every `/ar/` page. **BLOCKING.** | |
| 4.9 | `lang` and `dir` attributes correct on every option inside the language switcher. **BLOCKING.** | |
| 4.10 | `/give/` 301-redirects to `/donate/` (Cloudflare Pages redirect rule). `/give/` not in sitemap. **BLOCKING.** | |
| 4.11 | Schema.org JSON-LD validates clean on every English page (`https://validator.schema.org/`). **BLOCKING.** | |

## Section 5 — FPPC compliance

| # | Check | Result |
|---|---|---|
| 5.1 | English FPPC footer present on every English page: "Paid for by Michael Turon for SFUSD Board of Education 2026. FPPC ID 1482971." **BLOCKING.** | |
| 5.2 | Non-English scaffold files carry the English FPPC footer placeholder with the `# AWAITING TRANSLATION` marker and the "REQUIRES SAM RAY REVIEW BEFORE PUBLICATION" flag. **BLOCKING.** | |
| 5.3 | When a translation status flips to `reviewed`, the rendered FPPC footer in that language has been Sam-Ray-reviewed (review log entry present in frontmatter). **BLOCKING per language.** | |
| 5.4 | FPPC ID `1482971` literal preserved in every footer in every language. **BLOCKING.** | |
| 5.5 | Treasurer name "Lauren Turon" preserved in every footer in every language. **BLOCKING.** | |
| 5.6 | Campaign committee name "Michael Turon for SFUSD Board of Education 2026" preserved verbatim in English; localized name in other languages requires Sam Ray sign-off. **BLOCKING.** | |
| 5.7 | No trust-strip financial figure altered from v1.2.0 in any language. **BLOCKING.** | |
| 5.8 | LCFF / attendance recovery figures on Pillar-1 unchanged in any language. **BLOCKING.** | |
| 5.9 | No mention of Juris Doctor, attorney, or lawyer in any rendered page in any language. `grep -rEi "juris\|attorney\|lawyer\|abogad\|律师\|律師\|محامي\|luật sư" public/` returns no matches inside body content. **BLOCKING.** | |
| 5.10 | Two-track separation maintained: Deliverable 8 (AI translation disclosure) at top of page; Deliverable 9 (FPPC §84305 footer) in footer. Neither replaces the other. Both render on every translated page once that page is at `reviewed`. **BLOCKING.** | |

## Section 6 — AI translation disclosure (OIL Decision 2)

| # | Check | Result |
|---|---|---|
| 6.1 | `ai-translation-disclosure.html` partial renders ONLY when `.Site.Language.Lang != "en"`. **BLOCKING.** | |
| 6.2 | English source string locked: see `docs/Deliverable_8_AI_Translation_Disclosure_Source.md`. Sam Ray sign-off recorded. **BLOCKING.** | |
| 6.3 | Disclosure renders at top of content on every non-English page (above the page H1). **BLOCKING.** | |
| 6.4 | Disclosure is non-dismissible (no close button, no JS-driven hide, no cookie-driven hide). **BLOCKING.** | |
| 6.5 | Disclosure mailto link auto-populates subject with page title + language. Test: click on `/es/about/`, mail client opens with subject "Translation feedback - About (Spanish)" or equivalent. **BLOCKING.** | |
| 6.6 | Disclosure uses only Direction A design tokens. No new colors. No new fonts. **BLOCKING.** | |
| 6.7 | Disclosure not hidden by `display: none` or `visibility: hidden` in any breakpoint. **BLOCKING.** | |
| 6.8 | Disclosure has proper semantic markup (`<aside role="note">` or equivalent), not a div-with-aria. **WARN.** | |
| 6.9 | On `placeholder` pages, the translation-pending notice renders in place of the AI disclosure (Architecture Decision 6.5). **BLOCKING.** | |
| 6.10 | Disclosure does not block keyboard focus flow to page content (test with tab key from URL bar). **BLOCKING.** | |

## Section 7 — Accessibility

| # | Check | Result |
|---|---|---|
| 7.1 | WCAG 2.1 AA color contrast preserved on every page (axe DevTools clean). **BLOCKING.** | |
| 7.2 | Language switcher keyboard-navigable (ArrowDown / ArrowUp / Home / End / Escape / Enter). **BLOCKING.** | |
| 7.3 | Language switcher has visible focus ring on keyboard navigation. **BLOCKING.** | |
| 7.4 | Language switcher has `aria-haspopup="listbox"` and `aria-expanded` toggled correctly. **BLOCKING.** | |
| 7.5 | Skip-to-content link still works on every page in every language. **BLOCKING.** | |
| 7.6 | CJK font rendering legible on every `/zh-Hant/` and `/zh-Hans/` page (system stack — PingFang TC/SC primary; Microsoft JhengHei/YaHei fallback; Noto CJK fallback). **WARN.** | |
| 7.7 | Arabic font rendering legible on every `/ar/` page (system stack — SF Arabic primary; Geeza Pro fallback; Noto Naskh Arabic fallback). **WARN.** | |
| 7.8 | RTL chevrons mirror correctly on `/ar/` pages. **BLOCKING.** | |
| 7.9 | RTL mobile drawer opens from inline-start (right side in Arabic). **BLOCKING.** | |
| 7.10 | Trust-strip dollar figures read LTR inside RTL Arabic flow (bidi isolation working). **BLOCKING.** | |

## Section 8 — Analytics + community channel

| # | Check | Result |
|---|---|---|
| 8.1 | Umami `data-website-id` unchanged from v1.2.0. **BLOCKING.** | |
| 8.2 | Umami events fire for: language switcher click (with target language), donate CTA click (per language), volunteer CTA click (per language), book-call CTA click (per language). **WARN.** | |
| 8.3 | info@turonsf.com mail forwarding active and tested (send test mail; confirm receipt). **BLOCKING.** | |
| 8.4 | Brevo newsletter signup form works on every language page (test submit). **WARN.** | |
| 8.5 | Action Network volunteer form works on every language page (test submit). **WARN.** | |
| 8.6 | ActBlue donate link routes correctly from every language page. **BLOCKING.** | |
| 8.7 | Cloudflare Turnstile loads on every form on every language page. **BLOCKING.** | |

## Section 9 — Translation handoff

| # | Check | Result |
|---|---|---|
| 9.1 | All 60 unconditional scaffold files present and well-formed. **BLOCKING.** | |
| 9.2 | All 6 conditional scaffold files (uesf-questionnaire) present and well-formed (build does not render them). **BLOCKING.** | |
| 9.3 | Every scaffold frontmatter has `inLanguage`, `translation_status: "placeholder"`, `translation_tool_primary: ""`, `translation_tool_backup: ""`. **BLOCKING.** | |
| 9.4 | Every scaffold body has the standardized comment block (glossary keep-English, glossary localize, FPPC-sensitive list, link to workflow doc). **BLOCKING.** | |
| 9.5 | `data/translation_status.yaml` has 66 entries (60 unconditional + 6 conditional), all at `placeholder`. **BLOCKING.** | |
| 9.6 | All 7 i18n TOML files have identical key sets (42 keys each, 294 total). **BLOCKING.** | |
| 9.7 | Non-English TOML files have English placeholder values with `# AWAITING TRANSLATION` markers. **BLOCKING.** | |
| 9.8 | Per-language `llms.{lang}.txt` present in `static/` and carries the localized three-pillar names + canonical-figure tokens. **WARN.** | |
| 9.9 | `Phase1_Translation_Workflow.md` present in `docs/` and references the Translation Pipeline v1 Run Guide. **BLOCKING.** | |
| 9.10 | `Phase1_JEC_Scorecard.md` present in `docs/`. **BLOCKING.** | |

## Section 10 — Sign-off block

The deploy proceeds only after every BLOCKING item above is ✅ and the following sign-offs are recorded.

| Role | Name | Scope of review | Date | Signature |
|---|---|---|---|---|
| Operator | Michael Turon | All sections | | |
| Counsel | Sam Ray | Sections 5 (FPPC), 6 (AI disclosure), 7 (a11y for FPPC visibility) | | |
| Treasurer | Lauren Turon | Sections 2.4–2.5 (trust strip), 5 (FPPC), 8.3 (committee email forwarding) | | |
| **Optional:** Native-language reviewer | per language | Section 3.6 (own-script names), Section 7.6–7.10 (script + RTL rendering) | | |

After all sign-offs, push merge to `main`. The first production deploy ships with every non-English page at `placeholder` status — public sees the English site plus a discoverable language switcher with pending-translation notices. As the operator's separate translation workflow progresses each page-language pair through `reviewed`, the next build promotes that pair to hreflang + sitemap automatically.

— end of `Phase1_Preflight_Checklist.md`
