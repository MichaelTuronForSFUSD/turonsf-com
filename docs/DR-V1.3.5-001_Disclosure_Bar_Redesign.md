# DR-V1.3.5-001 — Disclosure Bar Redesign + JEC Language Optimization

**Decision record ID:** DR-V1.3.5-001
**Date:** 2026-05-14
**Status:** ACCEPTED — CLOSED
**Author:** Michael Turon (operator)
**Affected versions:** v1.3.5 → v1.3.5d
**Supersedes:** OIL Decision 2 (disclosure design and language, ratified 2026-05-12)
**Related:** Deliverable 8 (AI Translation Transparency Disclosure)

---

## Decision

Replace the heavy-bordered `.translation-notice` box with a single-line
persistent slim bar (`.disclosure-slim`, Option A). Optimize disclosure
language across all six non-English languages via full JEC panel convergence.
Route translation feedback to `help@turonsf.com` (dedicated) rather than
`info@turonsf.com` (general). Remove "English is the official version" clause
from the bar. Sam Ray confirms these changes satisfy clear-and-conspicuous
standard.

---

## Background

The v1.3.0 disclosure rendered as a full-width bordered box (~80–100px height
on mobile) positioned inside `<main>` before hero content. JEC UX/CRO analysis
(2026-05-14) identified three failure modes:

1. **Above-fold real estate cost** — box consumed 80–100px before any hero
   or CTA content on mobile, estimated to increase bounce rate.
2. **Error priming** — CTA "Find an error? Email info@turonsf.com" anchored
   readers in defect-detection mode before engaging with content.
3. **Hierarchy signal** — "English is the official version" read as "this
   version doesn't count" across all six language communities.

Full-panel JEC evaluation (5 panelists ES/繁體/简体, 3 each TL/VI/AR)
confirmed all three failure modes and converged on the Option A slim bar
at 9.5/10 across all panels.

---

## Decisions Made

### D1 — Visual design: Option A slim bar

**Decision:** Replace `.translation-notice` box with `.disclosure-slim`
single-line persistent bar positioned between the lang-eyebrow and site-header.

**Rationale:** JEC panel (6 languages, 21 panelists) voted unanimously for
Option A. Option B (dismissible with ×) rejected — × button confuses
lower-literacy users (Rosa ES 9.0, Mrs. Lam 繁體 7.5, Lorna TL 7.0 on B).
Persistent bar satisfies OIL Decision 2 non-dismissibility contract.

**CSS:** `.disclosure-slim` in `themes/turon-civic/static/css/site.css`.
**Partial:** `themes/turon-civic/layouts/partials/ai-translation-disclosure.html`.
**Placement:** `themes/turon-civic/layouts/_default/baseof.html` between
`<nav class="lang-eyebrow">` and `<header class="site-header">`.

### D2 — Disclosure language: JEC-converged strings

**Decision:** Replace original two-key disclosure strings with JEC-optimized
community-native strings across all 6 languages. Five design rules locked:

1. **Purpose leads** — WHY (family can read this) before HOW (AI)
2. **AI as tool** — "with AI's help / AI-assisted" not "AI translated"
3. **Family frame** — authentic for SFUSD parent candidate
4. **Collective-benefit CTA** — help more families, not report errors
5. **Zero error priming** — feedback/opinion/share, never error/mistake/report

**Converged strings (all panels at 9.5/10):**

| Lang | `ai_translation_disclosure_body` | `ai_translation_disclosure_link_text` |
|---|---|---|
| EN | This page was translated by AI so your family can read it in their language. | Help us improve it for more families. |
| ES | Queremos que tu familia pueda leer esto en español, como otras familias. Lo hicimos con ayuda de IA. | ¿Nos ayudas a mejorarlo? |
| 繁體 | 為讓您的家人能用中文閱讀 · 我們借助AI進行了翻譯。 | 您的寶貴意見能讓更多家庭受益 |
| 简体 | 为让您的家人能用中文阅读，我们真诚地借助AI进行了翻译。 | 您的意见能让更多家庭受益 |
| TL | Ginawa namin itong pahina sa Filipino para sa inyong pamilya. AI ang ginamit. | Tulungan kami na mapabuti para sa lahat |
| VI | Chúng tôi muốn gia đình bạn được đọc trang này bằng tiếng Việt. AI đã dịch. | Góp ý giúp thêm nhiều gia đình |
| AR | حتى تقرأ عائلتك هذه الصفحة بالعربية، استعنّا بالذكاء الاصطناعي للترجمة. | شاركنا رأيك لتستفيد عائلات أخرى |

**JEC panel scores:** ES 9.5 · 繁體 9.5 · 简体 9.5 · TL 9.33* · VI 9.5 · AR 9.5
*TL 9.33: Lorna (62, Tagalog-dominant) at irreducible 9.0 on AI terminology.
Jose and Maria both 9.5.

### D3 — Email routing: help@turonsf.com (dedicated)

**Decision:** Translation feedback routed to `help@turonsf.com` (dedicated
triage address), not `info@turonsf.com` (general). Desktop copy-to-clipboard
handler in `analytics.js` copies `help@turonsf.com`. Mobile `mailto:` opens
native mail to `help@turonsf.com`.

**Rationale:** Full panel confirmed `help@` outperforms `info@` by 1.0–2.0
points across all 6 languages. Unanimous finding: dedicated address signals
purposeful routing ("someone set this up for my community's feedback").
`info@turonsf.com` remains the canonical general campaign contact unchanged.

**Panel quote (Helen, 简体, community organizer):**
"help@ 说明这封邮件有人专门负责。info@ 进去之后谁知道谁看？"
(help@ means someone is specifically responsible. With info@ who knows who reads it?)

### D4 — Remove "English is the official version" clause from bar

**Decision:** "English is the official version" removed from the disclosure
bar body. Sam Ray confirmed this satisfies clear-and-conspicuous standard.

**Rationale:** Three independent failure modes identified across all panels:
(a) Positions non-English versions as second-class. (b) Reads as legal
protection for the campaign rather than service to the community. (c) Not
needed in the bar — English canonicality is implicit (EN pages have no
disclosure) and the FPPC footer is unchanged.

**What remains:** English canonicality is still documentable via this DR
and D8 for audit purposes. The FPPC §84305 footer (Deliverable 9) is
unchanged. D9 is the legal instrument; D8 is the accessibility instrument.

### D5 — Link UX: single element, JS desktop intercept

**Decision:** Single `<a href="mailto:help@..." data-copy-email>` element.
Desktop (≥768px): JS intercepts click, `e.preventDefault()`, copies email,
shows i18n toast. Mobile (<768px): click falls through to native `mailto:`.

**Rationale:** Original `<a> + <button>` CSS show/hide approach caused both
elements to render visually. Single-element JS-gated approach eliminates
duplicate, is more robust, degrades gracefully without JS.

**Toast strings — JEC-converged (all panels at 9.5/10):**

| Lang | `disclosure_copied` |
|---|---|
| EN | Copied! Email us at help@turonsf.com |
| ES | ¡Copiado! Escríbenos a help@turonsf.com |
| 繁體 | 已複製 · 歡迎來信：help@turonsf.com |
| 简体 | 已复制 · 欢迎来信：help@turonsf.com |
| TL | Nakopya! Mag-email sa amin: help@turonsf.com |
| VI | Đã sao chép! Viết thư cho chúng tôi: help@turonsf.com |
| AR | نُسخ بنجاح · راسلنا: help@turonsf.com |

---

## Consequences

- Disclosure bar height reduced from ~80–100px to ~32px on mobile
- Zero error priming in any language
- `help@turonsf.com` receives all translation feedback (requires inbox setup)
- `info@turonsf.com` unchanged as general campaign contact
- OIL Decision 2 non-dismissibility contract preserved — no close button
- FPPC §84305 footer (Deliverable 9) unchanged
- D8 updated to reflect new strings, design, email, and Sam Ray sign-off
- Three new i18n keys added: `disclosure_copied` (all 7 TOMLs)
- `analytics.js` carries copy handler + toast renderer inside existing IIFE

## Files Changed (v1.3.4 → v1.3.5d)

| File | Change |
|---|---|
| `themes/turon-civic/layouts/_default/baseof.html` | Eyebrow nav (v1.3.4) + disclosure partial relocation (v1.3.5) |
| `themes/turon-civic/layouts/partials/ai-translation-disclosure.html` | Full rewrite: slim bar, help@, single-link structure |
| `themes/turon-civic/static/css/site.css` | `.lang-eyebrow*` (v1.3.4) + `.disclosure-slim*` + `.disclosure-toast*` |
| `themes/turon-civic/assets/js/analytics.js` | `_discShowToast`, `_discFallbackCopy`, click handler inside IIFE |
| `themes/turon-civic/i18n/*.toml` (all 7) | Updated body + link text; added `disclosure_copied` key |
| `themes/turon-civic/layouts/partials/site-nav.html` | Removed `language-switcher.html` include (v1.3.4) |

## Git tags

| Tag | Commit | Description |
|---|---|---|
| v1.3.4 | 3691ae7 | Eyebrow language switcher, nav dropdown removed |
| v1.3.5 | 99217ef | JEC slim bar + 6-language disclosure strings |
| v1.3.5b | (see git log) | Data path fix — disclosure renders on non-EN pages |
| v1.3.5c | bc57a67 | help@ routing, JEC toast strings, clipboard handler |
| v1.3.5d | 8c8fd05 | Single-element link, JS desktop intercept |

---

## Sam Ray sign-off — DR-V1.3.5-001 CLOSED

**Confirmed 2026-05-14:**
- `help@turonsf.com` dedicated address satisfies clear-and-conspicuous
  standard for AI translation disclosure feedback routing
- Removal of "English is the official version" clause from bar satisfies
  clear-and-conspicuous standard; English canonicality remains implicit
  and documented in D8 for audit trail
- FPPC §84305 footer (Deliverable 9) unchanged and sufficient

| Role | Name | Date | Scope |
|---|---|---|---|
| Counsel | Sam Ray, Colla & Ray LLP (SBN 308921) | 2026-05-14 | All decisions in this DR |
| Operator | Michael Turon | 2026-05-14 | All decisions in this DR |
