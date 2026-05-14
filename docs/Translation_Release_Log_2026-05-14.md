# Translation Release Log — 2026-05-14

## Purpose

This handoff documents the multilingual campaign-site translation pass for `turonsf.com`, so the team can review, commit, and push the new language drafts safely.

## Scope Completed

Languages translated to `ai_translated` draft status:

- `es` — Spanish
- `zh-Hant` — Traditional Chinese
- `zh-Hans` — Simplified Chinese
- `tl` — Tagalog
- `vi` — Vietnamese
- `ar` — Arabic, RTL

Active public pages translated for each language:

- `/`
- `/about/`
- `/platform/`
- `/platform/pillar-1/`
- `/platform/pillar-2/`
- `/platform/pillar-3/`
- `/endorsements/`
- `/volunteer/`
- `/donate/`
- `/contact/`
- `/newsletter/`
- `/thank-you/`

Intentionally not promoted:

- `/platform/uesf-questionnaire/` remains `placeholder` in every translated language until permission and review are complete.

## Important Status Note

The translated pages are marked `ai_translated`, not `reviewed` or `live`.

That means:

- Pages are available for local and preview review.
- Pages show the AI translation disclosure.
- Pages remain conservative for SEO until human review and promotion.
- Sam Ray review is still required for legal/compliance-sensitive wording.
- Lauren Turon review is still required for financial/treasurer-sensitive wording.

## Key Files Changed

Content drafts:

- `content/*.es.md`
- `content/*.zh-Hant.md`
- `content/*.zh-Hans.md`
- `content/*.tl.md`
- `content/*.vi.md`
- `content/*.ar.md`
- `content/platform/*.es.md`
- `content/platform/*.zh-Hant.md`
- `content/platform/*.zh-Hans.md`
- `content/platform/*.tl.md`
- `content/platform/*.vi.md`
- `content/platform/*.ar.md`

Language UI strings:

- `themes/turon-civic/i18n/es.toml`
- `themes/turon-civic/i18n/zh-Hant.toml`
- `themes/turon-civic/i18n/zh-Hans.toml`
- `themes/turon-civic/i18n/tl.toml`
- `themes/turon-civic/i18n/vi.toml`
- `themes/turon-civic/i18n/ar.toml`
- `themes/turon-civic/i18n/en.toml`

LLM guidance / review context:

- `static/llms.es.txt`
- `static/llms.zh-Hant.txt`
- `static/llms.zh-Hans.txt`
- `static/llms.tl.txt`
- `static/llms.vi.txt`
- `static/llms.ar.txt`

Translation status:

- `data/translation_status.yaml`

Template and routing support:

- `hugo.toml`
- `themes/turon-civic/layouts/partials/ai-translation-disclosure.html`
- `themes/turon-civic/layouts/partials/head-hreflang.html`
- `themes/turon-civic/layouts/partials/language-switcher.html`
- `themes/turon-civic/layouts/partials/cta-link.html`
- `themes/turon-civic/layouts/shortcodes/cta.html`
- `themes/turon-civic/layouts/_default/baseof.html`
- `themes/turon-civic/layouts/_default/list.html`
- `themes/turon-civic/layouts/_default/single.html`
- `themes/turon-civic/layouts/index.html`

Verification tooling:

- `02_verify_turonsf_build.sh`
- `bin/check-translation-status.sh`

## Template/Routing Fixes Included

- Added canonical BCP-47 language handling via `bcp47` language params.
- Preserved public language routes for `/zh-hant/`, `/zh-hans/`, `/tl/`, `/vi/`, and `/ar/`.
- Kept Tagalog public route as `/tl/` while allowing Hugo locale behavior to use `fil`.
- Localized internal CTA links per language.
- Preserved external campaign UTM parameters by language.
- Ensured AI translation notices and pending notices use the correct language/status lookup.
- Ensured platform list order stays fixed: Special Education, Budget Discipline, Teacher Retention.
- Confirmed Arabic renders with `html lang="ar"` and `dir="rtl"`.

## Verification Evidence

All of the following passed locally on 2026-05-14:

```bash
./TURONSF_PATH_GUARD.sh
hugo --minify --logLevel warn
git diff --check
bin/check-i18n-parity.sh
bin/check-translation-status.sh
bin/check-no-jd-references.sh
./02_verify_turonsf_build.sh
```

Observed pass evidence:

- Hugo rendered all language directories: `es`, `zh-hant`, `zh-hans`, `tl`, `vi`, `ar`.
- `translation_status` consistency passed with 78 entries.
- i18n parity passed across 7 TOML files with 64 keys each.
- No JD/attorney/lawyer references were detected.
- Full site verifier completed successfully.
- Active translated pages did not show pending-translation notices.
- UESF questionnaire pages remain placeholder/gated.
- Browser review completed for each language, ending with Arabic at `http://localhost:1313/ar/`.

## Local Review URLs

Use the running Hugo preview server:

- Spanish: `http://localhost:1313/es/`
- Traditional Chinese: `http://localhost:1313/zh-hant/`
- Simplified Chinese: `http://localhost:1313/zh-hans/`
- Tagalog: `http://localhost:1313/tl/`
- Vietnamese: `http://localhost:1313/vi/`
- Arabic: `http://localhost:1313/ar/`

Spot-check these pages in each language:

- home
- about
- platform
- each of the three pillar pages
- volunteer form
- newsletter form
- donate page
- contact page
- thank-you page

## Suggested Commit Plan

Recommended PR branch:

```bash
git switch -c codex/add-ai-translated-language-drafts-2026-05-14
git status --short
./02_verify_turonsf_build.sh
git add 02_verify_turonsf_build.sh bin/check-translation-status.sh hugo.toml data/translation_status.yaml static/llms.*.txt themes/turon-civic content docs/Translation_Release_Log_2026-05-14.md
git status --short
git commit -m "Add AI-translated campaign language drafts"
git push -u origin codex/add-ai-translated-language-drafts-2026-05-14
```

If the team intentionally commits directly to `main`, run the same verification first and push only after review:

```bash
git status --short
./02_verify_turonsf_build.sh
git add 02_verify_turonsf_build.sh bin/check-translation-status.sh hugo.toml data/translation_status.yaml static/llms.*.txt themes/turon-civic content docs/Translation_Release_Log_2026-05-14.md
git commit -m "Add AI-translated campaign language drafts"
git push origin main
```

## Promotion Checklist Before Marking `live`

Before any translated page moves from `ai_translated` to `live`:

- Operator reviews page language and layout.
- Native/fluent reviewer checks tone and naturalness.
- Sam Ray reviews FPPC/legal/compliance-sensitive language.
- Lauren Turon reviews financial and treasurer-sensitive language.
- Brevo form submissions are tested for translated `locale` values.
- Cloudflare Pages preview is checked on desktop and mobile.
- `./02_verify_turonsf_build.sh` passes after any status changes.

## Current Manual Blockers

- Human review is still required before `reviewed` or `live` status.
- UESF questionnaire remains gated and should not be promoted without permission.
- The build verifier still reports the existing manual blocker text: Spanish backend routing, Sam review, Lauren review.


## Sign-off — 2026-05-14

| Role | Name | Scope | Status |
|---|---|---|---|
| Counsel | Sam Ray | FPPC/legal language in all 6 translated languages | ✅ Signed off |
| Treasurer | Lauren Turon | Financial figures, treasurer identity in all 6 languages | ✅ Signed off |

All ai_translated entries promoted to live per above sign-offs.
