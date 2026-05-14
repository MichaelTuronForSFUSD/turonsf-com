# Deliverable 8: AI Translation Transparency Disclosure — English Source

**Version:** v1.3.5d
**Last updated:** 2026-05-14
**Status:** CLOSED — Sam Ray sign-off recorded below.

**Sam Ray sign-off:** Sam Ray, Colla & Ray LLP (SBN 308921)
**Date:** 2026-05-14
**Scope:** Disclosure strings (all 6 languages), email routing (help@),
removal of "English is official version" clause, slim bar design (Option A).
Confirms: clear-and-conspicuous standard satisfied.

**Lauren Turon notice-of-review:** Lauren Turon (CFRO)
**Date:** 2026-05-14
*(Lauren is not the primary reviewer for D8 — only D9 — but is notified that
the disclosure language exists alongside the FPPC footer and that the
ai-translation-disclosure.html partial renders both correctly.)*

**Related decision record:** DR-V1.3.5-001 (2026-05-14) — supersedes OIL
Decision 2 disclosure design provisions.

---

## 8.1 Current live strings (v1.3.5d — JEC-converged 2026-05-14)

The disclosure is a single-line slim bar (`class="disclosure-slim"`)
positioned between the language eyebrow and site header. It renders on all
non-English pages where `translation_status` is `live` or `ai_translated`.

Strings are split across three i18n keys per language:

- `ai_translation_disclosure_body` — disclosure statement
- `ai_translation_disclosure_link_text` — CTA / feedback invitation
- `disclosure_copied` — desktop clipboard toast confirmation

### English (parity only — EN pages never show disclosure)

```toml
[ai_translation_disclosure_body]
other = "This page was translated by AI so your family can read it in their language."

[ai_translation_disclosure_link_text]
other = "Help us improve it for more families."

[disclosure_copied]
other = "Copied! Email us at help@turonsf.com"
```

### Español (ES) — JEC panel 9.5/10

```toml
[ai_translation_disclosure_body]
other = "Queremos que tu familia pueda leer esto en español, como otras familias. Lo hicimos con ayuda de IA."

[ai_translation_disclosure_link_text]
other = "¿Nos ayudas a mejorarlo?"

[disclosure_copied]
other = "¡Copiado! Escríbenos a help@turonsf.com"
```

### 繁體 Traditional Chinese (zh-Hant) — JEC panel 9.5/10

```toml
[ai_translation_disclosure_body]
other = "為讓您的家人能用中文閱讀 · 我們借助AI進行了翻譯。"

[ai_translation_disclosure_link_text]
other = "您的寶貴意見能讓更多家庭受益"

[disclosure_copied]
other = "已複製 · 歡迎來信：help@turonsf.com"
```

### 简体 Simplified Chinese (zh-Hans) — JEC panel 9.5/10

```toml
[ai_translation_disclosure_body]
other = "为让您的家人能用中文阅读，我们真诚地借助AI进行了翻译。"

[ai_translation_disclosure_link_text]
other = "您的意见能让更多家庭受益"

[disclosure_copied]
other = "已复制 · 欢迎来信：help@turonsf.com"
```

### Filipino/Tagalog (tl) — JEC panel 9.33/10

```toml
[ai_translation_disclosure_body]
other = "Ginawa namin itong pahina sa Filipino para sa inyong pamilya. AI ang ginamit."

[ai_translation_disclosure_link_text]
other = "Tulungan kami na mapabuti para sa lahat"

[disclosure_copied]
other = "Nakopya! Mag-email sa amin: help@turonsf.com"
```

*Note: 9.33 due to Lorna (62, Tagalog-dominant) at irreducible 9.0 on AI
terminology. Jose and Maria both 9.5. Panel consensus: "AI" is the
correct term; "makina" (machine) less accurate.*

### Tiếng Việt (vi) — JEC panel 9.5/10

```toml
[ai_translation_disclosure_body]
other = "Chúng tôi muốn gia đình bạn được đọc trang này bằng tiếng Việt. AI đã dịch."

[ai_translation_disclosure_link_text]
other = "Góp ý giúp thêm nhiều gia đình"

[disclosure_copied]
other = "Đã sao chép! Viết thư cho chúng tôi: help@turonsf.com"
```

### عربي Arabic (ar) — JEC panel 9.5/10

```toml
[ai_translation_disclosure_body]
other = "حتى تقرأ عائلتك هذه الصفحة بالعربية، استعنّا بالذكاء الاصطناعي للترجمة."

[ai_translation_disclosure_link_text]
other = "شاركنا رأيك لتستفيد عائلات أخرى"

[disclosure_copied]
other = "نُسخ بنجاح · راسلنا: help@turonsf.com"
```

---

## 8.2 Design (v1.3.5d)

**Visual form:** Single-line slim bar (`class="disclosure-slim"`).
Background: `rgba(7,26,47,0.055)`. Border-bottom: `1px solid rgba(7,26,47,0.10)`.
Padding: `0.4rem 1rem`. Font: `0.78rem`. Height: ~32px (vs. ~80–100px box in v1.3.0).

**Placement:** Between `<nav class="lang-eyebrow">` and `<header class="site-header">`
in `baseof.html`. Renders before any page content.

**Link UX:**
- Mobile (<768px): `<a href="mailto:help@turonsf.com?subject=...">` — native mail app
- Desktop (≥768px): JS intercepts click, `e.preventDefault()`, copies
  `help@turonsf.com` to clipboard, shows language-native toast for 2.5s

**mailto subject:** Auto-populates "Translation feedback - [Page Title] ([Language])"
for operator inbox triage. Implemented via Hugo `printf` in the partial.

**Non-dismissible:** No close button, no JS toggle, no localStorage flag.
OIL Decision 2 contract preserved.

**Partial path:** `themes/turon-civic/layouts/partials/ai-translation-disclosure.html`

---

## 8.3 Email routing (v1.3.5d)

| Address | Purpose |
|---|---|
| `help@turonsf.com` | Translation feedback only — disclosure bar mailto + clipboard copy |
| `info@turonsf.com` | General campaign contact — all other site uses unchanged |

`help@turonsf.com` is a dedicated triage address. Sam Ray confirmed this
routing satisfies clear-and-conspicuous standard (2026-05-14). Inbox setup
and auto-tagging recommended before May 20 in-home event.

---

## 8.4 FPPC defensibility (unchanged from v1.3.0)

This disclosure does **not** replace and is **not equivalent to** the
Cal. Gov. Code §84305 paid-for footer (Deliverable 9). Both render on
every translated page (Architecture Decision 6.5; OIL Decision 2).

**D8 (this disclosure)** speaks to translation method and community
access. It sits between the eyebrow and site header.

**D9 (FPPC §84305 footer)** speaks to payment / committee identity. It
sits in the footer with FPPC ID 1482971, committee name, and treasurer.

The removal of "English is the official version" from the bar does not
affect FPPC defensibility because: (a) English canonicality is implicit
in the site architecture (EN pages have no disclosure), (b) this clause
is not required by FPPC §84305 or Regulation 18435, and (c) Sam Ray
confirmed the omission satisfies clear-and-conspicuous standard.

Traceability to Research §2.7 / §2.9 / §6.6 remains valid. The v1.3.5d
strings satisfy the same AI-labeling + community-feedback-channel pattern
identified in Research §6.6 Tier 2. The "English is official" clause
was never a FPPC requirement — it was an internal conservatism that
Sam Ray confirmed is no longer needed in the bar.

---

## 8.5 JEC convergence trace (v1.3.5 — 2026-05-14)

### Five design rules locked (DR-V1.3.5-001)

1. **Purpose leads** — WHY (family can read this) before HOW (AI)
2. **AI as tool** — "with AI's help / AI-assisted" not "AI translated"
3. **Family frame** — authentic for SFUSD parent candidate
4. **Collective-benefit CTA** — help more families, not report errors
5. **Zero error priming** — feedback/opinion/share, never error/mistake

### Panel composition

- ES: 5 panelists (Valentina, Marcos, Isabel, Roberto, Carmen)
- 繁體: 5 panelists (Mrs. Lam, Kevin, Alice, Mr. Wong, Linda)
- 简体: 5 panelists (Wei, Helen, Jason, Mei, Lily)
- TL: 3 panelists (Maria, Jose, Lorna)
- VI: 3 panelists (Linh, Thanh, Bà Nguyễn)
- AR: 3 panelists (Fatima, Kareem, Nadia)

### Convergence summary

4 cycles run. Cycles 1–3 tested body/link text; Cycle 4 tested toast copy
and `help@` vs `info@`. `help@` outperformed `info@` by 1.0–2.0 points
across all 6 languages unanimously. All panels reached 9.5 by Cycle 4
(TL 9.33 due to Lorna AI-term floor).

Full JEC trace documented in session log 2026-05-14.

---

## 8.6 Version history

| Version | Date | Change |
|---|---|---|
| v1.3.0 | 2026-05-12 | Initial — heavy box, "Find an error?", info@, "English is official" |
| v1.3.5 | 2026-05-14 | Slim bar, JEC body/link strings, help@ routing |
| v1.3.5b | 2026-05-14 | Data path fix (partial render bug) |
| v1.3.5c | 2026-05-14 | Desktop clipboard handler, JEC toast strings |
| v1.3.5d | 2026-05-14 | Single-element link, JS desktop intercept |

---

## 8.7 Acceptance gates (v1.3.5d state)

- [x] Sam Ray sign-off recorded above — 2026-05-14
- [x] `ai_translation_disclosure_body` key present in all 7 i18n files
- [x] `ai_translation_disclosure_link_text` key present in all 7 i18n files
- [x] `disclosure_copied` key present in all 7 i18n files
- [x] `ai-translation-disclosure.html` partial renders on every live non-English page
- [x] Partial does NOT render on English canonical pages
- [x] Partial does NOT render the FPPC footer; D9 stays separate
- [x] Partial is not dismissible — no close UI in DOM
- [x] mailto: subject auto-populates page title + language for triage
- [x] help@turonsf.com in mailto and clipboard copy; info@ unchanged elsewhere
- [x] Desktop: clipboard copy + toast on ≥768px
- [x] Mobile: native mailto: on <768px
- [x] 6/6 CI gates passing at v1.3.5d (build, i18n parity, FPPC, UTM, no-JD, translation-status)
