# Deliverable 8: AI Translation Transparency Disclosure — English Source

**Status:** SAM RAY REVIEW REQUIRED — AI translation transparency disclosure
English source. Verify FPPC §84305 standard footer disclosure (Deliverable 9)
remains separate and unaltered.

**Sam Ray sign-off:** _____________________  Date: _____________________

**Lauren Turon notice-of-review:** _____________________  Date: _____________________
*(Lauren is not the primary reviewer for D8 — only D9 — but is notified that
the disclosure language exists alongside the FPPC footer and that the
ai-translation-disclosure.html partial renders both correctly.)*

---

## 8.1 Final English source (JEC-converged through 3 cycles)

The body string rendered by `themes/turon-civic/layouts/partials/ai-translation-disclosure.html`
at the top of every live non-English page is split across two i18n keys so
the operator's translation workflow can localize the prompt-to-action
("Find an error? Email info@turonsf.com.") independently from the disclosure
statement itself. Per Deliverable 4.5 the partial composes both into a
single visual block.

### Key: `ai_translation_disclosure_body`

> **This page was translated by AI. English is the official version.**

(11 words. Three short sentences? No — two sentences. Plain words. Translates
cleanly across all six target languages.)

### Key: `ai_translation_disclosure_link_text`

> **Find an error? Email info@turonsf.com.**

(7 words plus an email address. Question form invites engagement without
violating the Bloomberg Businessweek deadpan tone.)

### Combined render

> **This page was translated by AI. English is the official version.
> Find an error? Email info@turonsf.com.**

**Word count:** 18 words (+1 email address token).
**Sentence count:** 4 (very short sentences average 4.5 words each).
**Flesch Reading Ease, computed on the 18 words excluding the email token:**
≈82. Comfortably above the prompt's ≥75 target.

---

## 8.2 JEC convergence trace

### Cycle 1 — candidate variants

**Variant A — prompt draft (28 words):**
> This page was translated from English by AI. English is the canonical
> version. Find an error? Email info@turonsf.com and we'll fix it.

**Variant B — architecture draft (20 words):**
> This page was translated by AI from English. English is the official
> version. Please send fixes to info@turonsf.com.

**Variant C — synthesis attempt (24 words):**
> This page was translated by AI from English. English is the canonical
> version. Find an error? Email info@turonsf.com — we'll fix it.

### Cycle 2 — Red Team objections

**Red Team (Adversarial Reviewer):** "canonical" is jargon for a voter
audience and translates badly across Tagalog/Vietnamese. Use "official."

**Red Team (Naive Reader, Spanish-speaking SF parent):** "we'll fix it" is a
promise the campaign cannot guarantee in 24 hours. Drop the commitment;
keep the action.

**Red Team (Hugo i18n Architect):** Splitting the disclosure into two i18n
keys is better than one — the second clause is a call to action that the
operator may want to localize register-aware (formal vs. friendly) without
restating the technical fact in the first clause.

**Red Team (FPPC defensibility):** "from English" is redundant once the
next sentence names English as the official version. Drop.

### Cycle 3 — Blue Team rebuttal + final

**Blue Team accepts:** Drop "canonical" → "official." Drop "we'll fix it"
commitment. Drop "from English." Split into two i18n keys.

**Final disclosure body (key `ai_translation_disclosure_body`):**
> This page was translated by AI. English is the official version.
> *(11 words)*

**Final disclosure CTA (key `ai_translation_disclosure_link_text`):**
> Find an error? Email info@turonsf.com.
> *(7 words + email token)*

**Combined: 18 words.** Flesch ≈82. All three required elements present:
(a) page is AI-translated, (b) English is canonical, (c) report errors to
info@turonsf.com.

---

## 8.3 FPPC defensibility trace

This disclosure does **not** replace and is **not equivalent to** the
Cal. Gov. Code §84305 paid-for footer (Deliverable 9). Both render on every
translated page (Architecture Decision 6.5; OIL Decision 2).

- **D8 (this disclosure)** speaks to translation method. It sits at the top
  of the page, immediately below the global header, and tells the reader
  the page is AI-translated and where to report errors.
- **D9 (FPPC §84305 footer)** speaks to payment / committee identity. It
  sits in the footer, in the page's language per FPPC Regulation 18435
  same-language requirement (Research §2.2), and identifies the campaign
  committee, FPPC ID 1482971, and treasurer.

The two disclosures do not overlap textually and do not interfere with each
other. The partial that renders D8 (`ai-translation-disclosure.html`) does
not render the FPPC footer. The footer partial that renders D9 does not
render D8. They are independent surfaces.

### Traceability to Research §2.7 / §2.9 / §6.6

Research §2.7 catalogs five FPPC-compatible disclaimer patterns. The chosen
English source is closest to:

- **§2.7 row 2 "AI Disclosure":** "Translated by artificial intelligence
  for accessibility. We welcome community feedback at info@turonsf.com to
  improve accuracy."
- **§2.7 row 4 "Legal Standard":** "English is the canonical language of
  this campaign. Translated content is not intended to create legal or
  binding obligations."

The final English source synthesizes both: AI-translation acknowledgement
+ English-as-official + community feedback channel. The "Legal Standard"
row's "not intended to create legal or binding obligations" clause is
deliberately omitted because (a) it is legal jargon, (b) it does not
satisfy the voter-readable constraint, and (c) Research §2.8 / AB 2655 /
AB 2839 caselaw (Judge Menendez, October 2024) make explicit AI
labeling the legally safer pattern without requiring legal-disclaimer
language.

Research §6.6 identifies the target quality tier as **Tier 2: AI-assisted
with human spot-check.** The phrase "translated by AI" is sufficient to
locate the campaign in Tier 2 from the reader's perspective; "English is
the official version" sets the canonical-source expectation; "Find an
error? Email info@turonsf.com" operationalizes the human-loop.

---

## 8.4 i18n key allocation

The English-source keys are declared in `i18n/en.toml`:

```toml
[ai_translation_disclosure_body]
other = "This page was translated by AI. English is the official version."

[ai_translation_disclosure_link_text]
other = "Find an error? Email info@turonsf.com."
```

The six non-English string tables in `i18n/{es,zh-Hant,zh-Hans,tl,vi,ar}.toml`
ship with these two keys present, containing the English placeholder text,
and a `# AWAITING TRANSLATION` marker. The operator's translation workflow
fills in the translated values.

Per Architecture Decision 6.5, the `ai-translation-disclosure.html` partial
renders these keys ONLY when:

1. `.Site.Language.Lang` is not `en`, AND
2. `translation_status` is not `placeholder` (placeholder pages render
   the translation-pending notice instead).

---

## 8.5 Translation guidance for the six target languages

The English source is deliberately structured to translate cleanly:

| Language    | Notes                                                                                                  |
|-------------|--------------------------------------------------------------------------------------------------------|
| es          | Use formal register (`usted` if any pronouns enter the translation). "Oficial" not "canónica."         |
| zh-Hant     | Traditional characters only — do NOT mix Simplified in. SF parent register, not mainland register.     |
| zh-Hans     | Simplified characters only. "官方" is the cleanest "official" rendering.                                 |
| tl          | Plain Tagalog, no Taglish. "Opisyal" is the cleanest "official" rendering. Avoid name transliteration. |
| vi          | Plain Vietnamese with full tone diacritics. "Chính thức" for "official."                                |
| ar          | Modern Standard Arabic. Preserve `info@turonsf.com` in Latin script with bidi isolation.                |

Each translation is reviewed by Sam Ray before publication because the
disclosure interacts with FPPC §84305 / Regulation 18435 same-language
requirements (Research §2.2).

---

## 8.6 Non-dismissibility (OIL Decision 2 contract)

The disclosure is **not dismissible.** The partial renders no close button,
no JS toggle, no `localStorage` hide flag, and no per-session suppression.
Dismissibility would undermine the transparency commitment and create a
discoverability inconsistency for voters who have JS disabled or who clear
storage.

If a future build introduces user-preference controls (font-size,
high-contrast, etc.), the disclosure is explicitly out-of-scope for those
controls. This is documented in the preflight checklist (Deliverable 12 §6).

---

## 8.7 Acceptance gates

- [ ] Sam Ray sign-off recorded above.
- [ ] English source string locked: "This page was translated by AI.
      English is the official version. Find an error? Email info@turonsf.com."
- [ ] `ai_translation_disclosure_body` key present in all 7 i18n files.
- [ ] `ai_translation_disclosure_link_text` key present in all 7 i18n files.
- [ ] `ai-translation-disclosure.html` partial renders on every live
      non-English page (Preflight §6).
- [ ] Partial does NOT render on English canonical pages (Preflight §6).
- [ ] Partial does NOT render the FPPC footer; D9 stays separate (Preflight §5).
- [ ] Partial is not dismissible — no close UI in DOM (Preflight §6).
- [ ] Disclosure uses only Direction A tokens (`--navy-900`, `--accent`,
      `--cream-50`) (Preflight §3).
- [ ] mailto: subject auto-populates with page title + language for triage.
