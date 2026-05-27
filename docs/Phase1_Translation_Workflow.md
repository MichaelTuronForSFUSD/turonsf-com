# Phase 1 Translation Workflow — turonsf.com v1.3.0

**Document role:** Operator-facing guide for running AI translation against the v1.3.0 scaffold files.
**Audience:** Michael Turon (operator), with review gates for Sam Ray (counsel) and Lauren Turon (treasurer / FPPC CFRO).
**Pairs with:** `0_Translation_Pipeline_v1_Run_Guide.md` (engine spec — the `turon-translate` CLI). This document is the human-loop wrapper. It does **not** redesign the engine.
**Locked context (Decisions Register):** AI-translation-first methodology with English as canonical; community-review feedback channel via info@turonsf.com; no CMS / translation widgets (markdown + git only).

---

## 1. Scope and source-of-truth model

The v1.3.0 build produced **66 scaffold files** (60 unconditional + 6 conditional for `/platform/uesf-questionnaire/`) across six target languages: Spanish (`es`), Traditional Chinese (`zh-Hant`), Simplified Chinese (`zh-Hans`), Tagalog (`tl`), Vietnamese (`vi`), Arabic (`ar`). Each scaffold is the English source body with translation-target frontmatter, glossary discipline, and the standard FPPC footer placeholder. The `/letters/uesf-2026-05-12/` and `/talk/` pages — and their 12 scaffolds — were deferred from v1.3.0 (May 12 OIL decision) and will be re-added in v1.3.1+.

The build produces scaffolds. **This workflow runs AI translation against those scaffolds.** Nothing in this document changes the IA, the design tokens, or the locked decisions; this is purely the localization pass.

The single source of truth for translation state is `data/translation_status.yaml` at the project root. Every page/language pair has one status:

| Status | Meaning | Hreflang | Sitemap | Pending banner | Public visibility |
|---|---|---|---|---|---|
| `placeholder` | Scaffold only; no AI translation run yet | NOT emitted | NOT listed | Renders | Page exists but is noindex,follow + canonicalizes to English |
| `ai_translated` | AI draft committed; pre-review | NOT emitted | NOT listed | Renders | Same as placeholder (visible but not promoted) |
| `reviewed` | Operator + Sam Ray + Lauren sign-off complete | Emitted | Listed | Hidden | Promoted in hreflang and sitemap |
| `community_corrected` | Updated after public correction | Emitted | Listed | Hidden | Same as reviewed; revision log appended |
| `live` | Public production state (synonym of reviewed for older entries) | Emitted | Listed | Hidden | Promoted |

The Hugo partials `head-hreflang.html`, `language-switcher.html`, `ai-translation-disclosure.html`, and the `layouts/sitemap.xml` template all read this file. Update it, deploy, the surface area follows. **Do not** edit hreflang or sitemap output manually; edit the YAML.

---

## 2. AI tool selection per language

The `turon-translate` CLI runs a per-language candidate pool on Mac Studio and iterates until each translation clears the composite score threshold (≥ 95 native-voice rubric on the local panel + back-translation + chrF++ + COMET-Kiwi where supported). The recommendations below are starting candidates; the pipeline learns from CalibrationLogger trajectories and may surface preferred primaries over time.

| Language | Primary candidate | Backup candidate | Notes |
|---|---|---|---|
| Spanish (`es`) | DeepL Pro (US Spanish setting) | Claude Opus 4.7 | DeepL has strong US-Spanish register; Claude useful for civic-tone matching and tone repairs. |
| Traditional Chinese (`zh-Hant`) | Claude Opus 4.7 | Gemini 3.1 Pro | DeepL Traditional Chinese support is uneven; LLM with native-voice rubric outperforms. SFUSD reading list anchors most terminology. |
| Simplified Chinese (`zh-Hans`) | DeepL Pro | Claude Opus 4.7 | DeepL Simplified is strong; Claude as second opinion for civic register. |
| Tagalog (`tl`) | Claude Opus 4.7 | Gemini 3.1 Pro | DeepL does not support Tagalog. Avoid Google Translate for civic register; it produces stilted Filipino rather than community-readable Tagalog. |
| Vietnamese (`vi`) | Claude Opus 4.7 | Gemini 3.1 Pro | DeepL Vietnamese is acceptable but Claude renders civic tone better; Gemini handles long-form well. |
| Arabic (`ar`) | Claude Opus 4.7 | Gemini 3.1 Pro | DeepL Arabic is limited; LLM with explicit MSA-formal register prompt outperforms. Do not use Egyptian or Levantine colloquial. Modern Standard Arabic only. |

**Never use:** browser-page-translate engines, Google Translate as primary, or any tool without an exposed glossary mechanism. The glossary discipline (Section 4) requires a controllable terminology layer.

---

## 3. Verification method per translation

Every translation passes through five gates before its status moves from `ai_translated` → `reviewed`:

1. **Forward translation** — primary candidate produces v1; the CLI re-runs with the backup candidate to produce v2.
2. **Back-translation diff** — both v1 and v2 are back-translated to English and diffed against the source. Any back-translation that drops a number, drops a proper noun, or substantively reframes a claim is a hard fail.
3. **chrF++ + COMET-Kiwi (where supported)** — language-pair quality estimation. Threshold is set per language in the CLI config.
4. **Native-voice rubric (3-judge local panel)** — three local models score the translation on civic register, glossary compliance, FPPC-sensitive string preservation, and readability. Composite ≥ 95 to pass.
5. **Human review** — Sam Ray for FPPC-sensitive strings (Section 5); Lauren for any string containing a financial figure or trust-strip credential; operator for everything else. **Reviewers see the AI output, the back-translation, and the source side-by-side.**

A translation that fails any gate is flagged in the CalibrationLogger trace and held in `ai_translated` status. It does not appear in hreflang or sitemap. The page renders the pending banner to non-English readers.

---

## 4. File naming, frontmatter, and the glossary contract

### 4.1 File naming

Per Hugo `translationByFileName` mode (Architecture Decision 1), translations live in the same directory as the English source with a language suffix:

```text
content/about.md                            # English source
content/about.es.md                         # Spanish
content/about.zh-Hant.md                    # Traditional Chinese
content/about.zh-Hans.md                    # Simplified Chinese
content/about.tl.md                         # Tagalog
content/about.vi.md                         # Vietnamese
content/about.ar.md                         # Arabic
```

Page bundles (for any future page that lives in its own directory) use the same suffix on the bundle index:

```text
content/<bundle-name>/index.md
content/<bundle-name>/index.es.md
content/<bundle-name>/index.zh-Hant.md
...
```

v1.3.0 ships no page bundles — every translatable page is a regular page file at the language suffix. The pattern is documented here for future use (open letters, multi-asset campaign pages) when content is locked.

### 4.2 Frontmatter spec

The scaffold ships with frontmatter mirroring the English source plus three localization keys:

```yaml
inLanguage: "es"                  # BCP 47 tag matching the filename suffix
translation_status: "placeholder" # workflow updates this
translation_tool_primary: ""      # CLI writes the actual tool used
translation_tool_backup: ""       # CLI writes the actual tool used
```

The CLI writes `translation_tool_primary` and `translation_tool_backup` from its candidate-pool config. Do not hand-edit these; the calibration trail depends on them.

When promoting a translation to `reviewed`, the CLI appends a `review_log` block to the frontmatter:

```yaml
review_log:
  - reviewer: "sam_ray"
    role: "counsel"
    date: 2026-05-15
    scope: "FPPC footer + AI disclosure"
    result: "approved"
  - reviewer: "lauren_turon"
    role: "treasurer"
    date: 2026-05-15
    scope: "trust-strip credentials + financial figures"
    result: "approved"
```

### 4.3 Glossary — terms that stay English / Latin script

These do **not** translate. They appear in the target-language text verbatim:

- **Operational nouns:** ActBlue, FPPC, Cloudflare, Umami, Action Network, Brevo, MailChannels, Turnstile, Hugo, GitHub.
- **Proper nouns (people):** Michael Turon, Lauren Turon, Sam Ray.
- **Proper nouns (institutions):** SFUSD, UESF, San Francisco Unified School District, Royal Caribbean, HelloFresh, Cambridge.
- **Identifiers:** FPPC ID 1482971, EIN numbers, all case numbers.
- **Financial figures:** all dollar amounts, percentages, and dates render as Latin-script digits inside the target-language text. For Arabic specifically, wrap figure spans with `<bdi dir="ltr">…</bdi>` to keep the bidi flow correct.

The CLI's translator prompt is seeded with this list. Any output that translates a glossary term is a hard fail at gate 4.

### 4.4 Glossary — terms that localize

These **do** translate, with the per-language target captured in the CLI's terminology pack:

- Civic verbs: "Vote", "Endorse", "Volunteer", "Donate", "Sign up", "Read", "Watch", "Share".
- Role tag: "Data Scientist, SFUSD Parent" → target language equivalent. The phrase "Data Scientist" may use the loanword in some languages (common in Spanish, Tagalog) or the localized term in others (typical in Mandarin Chinese, Arabic). Sam Ray reviews each rendering. **Never** use Juris Doctor / attorney / lawyer / abogado / abogada / 律师 / 律師 / abogado / محامي / luật sư / abogado — in any language.
- Three pillar names: target-language equivalents drawn from SFUSD's own translated materials where available (the SFUSD Family Engagement office publishes Spanish, Cantonese, Mandarin, Vietnamese, Tagalog, and Arabic versions of district documents; their terminology is the strongest precedent).
- Page section labels: navigation, hero CTAs, form labels, success/error strings — these live in the i18n string tables, not in page content.

### 4.5 FPPC-sensitive strings — highest scoring threshold

These get the tightest review loop and the highest score threshold (≥ 97 composite, not ≥ 95):

- The FPPC §84305 footer disclosure (Deliverable 9). Glossary contract: "FPPC", "ID 1482971", "Michael Turon", "Lauren Turon", "SFUSD" stay English; the surrounding clauses translate.
- The AI translation disclosure body (Deliverable 8). Glossary contract: "info@turonsf.com" stays Latin-script; the surrounding clauses translate.
- Trust-strip credential descriptors: "Royal Caribbean", "HelloFresh", "Cambridge" stay English; surrounding text like "Cost savings at", "EBITDA swing", "Physics PhD", and "SFUSD parent through 2040" translates.
- Financial figures in trust strip ($72M, −$33M → +$9M): figures themselves never change. For Arabic, wrap with `<bdi dir="ltr">` so they read LTR inside the RTL flow.
- Pillar-1 LCFF / attendance figures: same contract — figures stay numeric, surrounding prose translates.

Every FPPC-sensitive string is flagged in the CLI output as **REQUIRES SAM RAY REVIEW BEFORE PUBLICATION**. Sam Ray sees the side-by-side comparison and signs off (or returns it for revision) before the status flips to `reviewed`.

---

## 5. Operator process — the ten steps you actually run

Once the Translation Pipeline v1 package is deployed on Mac Studio (separate JEC run; see `0_Translation_Pipeline_v1_Run_Guide.md`):

1. **Confirm CLI ready:** `turon-translate selftest --lang es` (repeat per language). All gates must pass on a known-good fixture before running real content.
2. **Run translation:** `turon-translate translate --source content/about.md --langs es,zh-Hant,zh-Hans,tl,vi,ar --output-dir content/`. The CLI writes the AI-translated content into the existing scaffold files (preserving the standardized comment block) and updates `data/translation_status.yaml` to `ai_translated` for each language.
3. **Review pipeline log:** `cat ~/Logs/turon-translate/$(date +%Y%m%d).jsonl | jq 'select(.composite < 95)'`. Anything below threshold is held.
4. **Review summary:** `turon-translate review --since-today --below-threshold` produces a Markdown digest of every flagged translation with the source, AI output, back-translation, judge notes, and the specific gate(s) that failed.
5. **Sam Ray spot-check (FPPC + AI disclosure):** counsel-in-loop on every FPPC-sensitive string flagged by the pipeline **and** a random 10% sample of clean translations. Email Sam the digest; expect 48-hour turnaround. Block status promotion on Sam's response.
6. **Lauren spot-check (financial figures + trust strip):** treasurer-in-loop on every trust-strip credential descriptor and every page that touches a financial figure. Email Lauren the digest; expect 24-hour turnaround.
7. **Commit:** the CLI generates a commit message of the form `i18n(es): translate /about/ — pipeline composite 96.3, sam_ray approved, lauren approved`. Push to the `phase1-7lang-build` branch.
8. **Cloudflare Pages preview:** the branch builds a preview. Walk every translated page on iPhone-narrow viewport and on desktop. Confirm the language switcher resolves correctly and the AI translation disclosure renders.
9. **Merge to main + status flip:** open the PR, get the preview link approved by Sam and Lauren (one PR per language is fine; one PR per page-language is also fine — the CLI supports both flows). On merge, run `turon-translate promote --page /about/ --lang es --status reviewed`, which updates `data/translation_status.yaml`. The next build emits hreflang, lists the page in the sitemap, and stops showing the pending banner.
10. **Monitor community channel:** info@turonsf.com is the public correction channel. The cadence in Section 7 applies. For each correction the operator decides to apply, run `turon-translate replay --trace <id> --override "<corrected text>"`, which re-runs the gates with the override locked in, then commits with a message like `i18n(es): correct /about/ — community feedback (anonymized) — pipeline composite 97.1, sam_ray approved` and bumps status to `community_corrected`. Do not identify the reporter without their explicit consent.

---

## 6. AI translation transparency disclosure — UX policy

The Hugo partial `ai-translation-disclosure.html` (Deliverable 4.5) renders the disclosure at the top of every non-English page. **The translation pipeline does not insert this disclosure into content body.** It is a template-rendered concern. The pipeline only translates content body.

What the pipeline does do: translate the two i18n keys `ai_translation_disclosure_body` and `ai_translation_disclosure_link_text` in each per-language TOML file. These two keys are FPPC-sensitive (Section 4.5) and require Sam Ray sign-off before the per-language TOML lands on main.

The disclosure is **non-dismissible**. There is no close button, no dismiss cookie, no "don't show me this again" affordance. The transparency commitment requires the disclosure to remain visible on every non-English page, every load.

---

## 7. Community-review channel — monitoring cadence

The disclosure routes correction reports to info@turonsf.com with a subject line that auto-populates the page title and language (the partial generates the mailto). The operator monitoring cadence:

- **First 14 days after a language goes `reviewed`:** check daily. New translations attract the most early correction reports.
- **Days 15 through end of campaign minus 30:** check Monday and Thursday.
- **Final 30 days before November 3, 2026:** check daily. Last-mile translation issues at peak attention need fast turnaround.
- **Election day +1 through +30:** check Monday and Thursday, then archive.

Every correction that lands in the inbox is logged in a private spreadsheet with: date, page, language, reporter (if consented), correction, decision (apply / decline / clarify), and the commit hash if applied. The spreadsheet is not public, but the operator publishes a quarterly anonymized rollup if the volume warrants it (Architecture Decision 9 §5).

---

## 8. Candidate community-review partner organizations

These are the organizations Step 1 Research surfaced as the strongest community-language partners in SF. **Present them as candidates; do not commit Michael to outreach without operator decision.** The outreach sequence (who to contact first, what to ask, how to introduce the project) is a separate conversation with Nate Allbee.

| Language | Candidate partners |
|---|---|
| Spanish | La Raza Community Resource Center; Mission Economic Development Agency (MEDA); Mission Cultural Center for Latino Arts |
| Cantonese (zh-Hant) | Chinese Progressive Association; Chinatown Community Development Center; Self-Help for the Elderly |
| Mandarin (zh-Hans) | Chinese Progressive Association; SF Chinese Newcomers Service Center |
| Tagalog (tl) | Filipino-American Development Foundation; West Bay Pilipino Multi-Service Center; Filipino Community Center |
| Vietnamese (vi) | Vietnamese American Roundtable; Southeast Asian Community Center; Vietnamese Voluntary Foundation |
| Arabic (ar) | Arab Resource & Organizing Center (AROC); Arab American Cultural Center of SF Bay Area |

The pitch is: "We use AI translation with English as canonical and we publicly invite community corrections; would your organization be willing to be listed as a community-review partner if we cite you on the AI translation disclosure?" That's a smaller ask than asking them to translate the site. It's also a more honest one.

---

## 9. Per-language readability targets

The English standard is **Flesch Reading Ease ≥ 75**. There is no Flesch equivalent that travels cleanly across all six target languages, so each language uses a qualitative bar enforced by the local panel rubric:

- **Spanish:** the Fernández Huerta or Szigriszt-Pazos index ≥ 65 (the rubric uses Fernández Huerta as primary).
- **Traditional Chinese / Simplified Chinese:** the rubric uses sentence-length and character-density heuristics calibrated against SFUSD's own translated parent communications. No standard readability index travels usefully for Chinese.
- **Tagalog:** the rubric checks for clarity-of-civic-register, sentence length, and absence of overly formal Spanish-loanword constructions. No standard readability index.
- **Vietnamese:** the rubric checks for clarity-of-civic-register and avoidance of overly Sino-Vietnamese formal register where colloquial register would read better. No standard readability index.
- **Arabic:** the rubric checks for Modern Standard Arabic register, avoidance of Quranic register, and sentence-length. No standard readability index.

The full rubric specs live in the Translation Pipeline v1 Run Guide; this document just references them.

---

## 10. Long-form chunking for `/platform/uesf-questionnaire/`

If and when Alex Schmaus permits publication, the UESF pledge questionnaire is ~14,000 words. That exceeds the context-efficient single-call budget for some translation tools. The `turon-translate` CLI handles chunking internally: it splits at question boundaries (the questionnaire is structured as numbered prompts with bounded responses), translates each chunk independently with carry-over glossary context, and stitches the result back together.

Recommended publication sequence:

1. English source page lands first (the page already exists as `content/platform/uesf-questionnaire.md` with `is_active: false`).
2. Alex confirms permission. Operator flips `is_active: true` and pushes. English goes live.
3. Translation runs per language in parallel (the CLI is per-language-independent). Each language goes live as its review gates clear. Spanish first (largest SFUSD EL population), then zh-Hant, zh-Hans, tl, vi, ar in any order the review bandwidth permits.
4. If a language takes more than 48 hours to clear review, the operator may publish the English-only page with the pending banner active for that language. This is the "staged publication" pattern Architecture Decision 9 contemplates.

---

## 11. What this workflow does NOT do

- **No machine translation outside this loop.** No browser auto-translate suggestions, no random ad-hoc Claude prompts to "translate this page." Every translation goes through the CLI so the calibration trail captures it.
- **No CMS, no translation widget, no Polylang, no Weglot, no Crowdin.** Markdown + git is locked.
- **No identification of community reporters without explicit consent.** Public correction logs are anonymized.
- **No translation of glossary-locked terms** (Section 4.3). Hard fail at gate 4.
- **No use of Juris Doctor / attorney / lawyer / abogado / 律师 / 律師 / محامي / luật sư** — in any language. Role tag is "Data Scientist, SFUSD Parent" or its localized equivalent only.

---

## 12. Document version

- **v1.0** — May 12, 2026. Ships with v1.3.0. Pairs with `0_Translation_Pipeline_v1_Run_Guide.md` (separate JEC run). Sam Ray review notation: **REQUIRES SAM RAY REVIEW** on FPPC-sensitive sections (4.5, 6); Lauren review notation: **REQUIRES LAUREN TURON REVIEW** on financial-figure sections (4.5, 5.6).
- **Next revision trigger:** when the Translation Pipeline v1 package ships, this document's Section 5 step numbers are validated end-to-end against the actual CLI behavior; any drift gets a v1.1.

— end of `Phase1_Translation_Workflow.md`
