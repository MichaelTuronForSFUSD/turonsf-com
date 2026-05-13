# turonsf.com v1.3.0 — Phase 1 + 7-Language Build Manifest

**Build:** v1.3.0
**Date:** 2026-05-12
**Operator:** Michael Turon
**FPPC ID:** 1482971
**Election:** November 3, 2026 — SFUSD Board of Education
**Composite scorecard:** 92.46 (v1) → 95.18 (v2 projection)

This bundle is an **overlay on the v1.2.0 main checkout**. It adds files and modifies a small set of existing files via unified diffs. Apply with care; the Preflight Checklist in `docs/Phase1_Preflight_Checklist.md` is the gate.

---

## 1. What's in this bundle (114 files)

```
turonsf_v1.3.0/
├── MANIFEST.md                              # this file
├── .gitignore                               # operator-private exclusions (audit F18)
├── hugo.toml.diff                           # D1 — adds [languages] block for 7 langs
├── .github/workflows/
│   └── build-and-check.yml                  # CI — 5 parity checks on every PR
├── bin/                                     # CI scripts (executable)
│   ├── check-i18n-parity.sh                 # 7-language TOML key parity
│   ├── check-no-jd-references.sh            # LOCKED role-tag enforcement
│   ├── check-utm-hygiene.sh                 # UTM-on-every-CTA enforcement
│   ├── check-fppc-footer.sh                 # §84305 footer present on every page
│   └── check-translation-status.sh          # yaml ↔ scaffold consistency
├── layouts/
│   └── sitemap.xml                          # D10 — multilingual sitemap, data-driven
├── content/                                 # 68 files (2 English source + 66 scaffolds)
│   ├── endorsements.md                      # D6 — is_active:false default
│   ├── platform/
│   │   └── uesf-questionnaire.md            # D6 — CONDITIONAL, is_active:false
│   ├── {page}.{lang}.md                     # D7 — 60 unconditional + 6 conditional scaffolds
│   └── ...                                  # all at translation_status: placeholder
├── data/
│   ├── translation_status.yaml              # 66 entries, all placeholder at ship
│   └── endorsements.yaml                    # empty with example schema comment
├── docs/                                    # 11 files
│   ├── Deliverable_8_AI_Translation_Disclosure_Source.md
│   ├── Deliverable_9_FPPC_Footer_Disclosure.md
│   ├── Phase1_Translation_Workflow.md       # D11
│   ├── Phase1_Preflight_Checklist.md        # D12 part 1 (build correctness)
│   ├── Phase1_JEC_Scorecard.md              # D12 part 2 (build scorecard)
│   ├── Phase1_Design_Red_JEC_Audit.md       # design audit, 23 findings
│   ├── Phase1_Analytics_Spec.md             # canonical 14-event Umami taxonomy + UTM scheme
│   ├── Phase1_to_Phase2_Architecture_Readiness.md  # pre-lock + cookbook + Phase 2 scope
│   ├── Phase1_Deployment_Red_JEC_Audit.md   # deployment audit, 21 findings
│   ├── Phase1_Deployment_Preflight.md       # deployment preflight (post-build)
│   └── Phase1_Deployment_Run_Guide.md       # Mac Studio → live, 12 steps
├── static/                                  # 10 files
│   ├── robots.txt                           # 11-AI-bot allowlist preserved
│   ├── _headers                             # CSP + security headers (audit F21)
│   ├── _redirects                           # /give/ → /donate/ + future aliases
│   └── llms.{en,es,zh-Hant,zh-Hans,tl,vi,ar}.txt  # D10 — 7 files
└── themes/turon-civic/
    ├── assets/js/
    │   └── analytics.js                     # Umami shim, 14 events, prod-ready
    ├── i18n/                                # D2 — 7 TOML files, 42 keys each
    │   └── {en,es,zh-Hant,zh-Hans,tl,vi,ar}.toml
    ├── layouts/
    │   ├── partials/                        # 3 partials
    │   │   ├── language-switcher.html       # D3
    │   │   ├── head-hreflang.html           # D4
    │   │   └── ai-translation-disclosure.html  # D4.5
    │   └── shortcodes/
    │       └── cta.html                     # CTA shortcode w/ auto-UTM + event firing
    └── static/css/
        └── tokens.css.diff                  # D5 — RTL + CJK system font stacks
```

---

## 2. Deliverable map (12 of 12 complete)

| # | Deliverable | Path | Status |
|---|---|---|---|
| 1 | Hugo config | `hugo.toml.diff` | ✅ |
| 2 | i18n string tables (7 × TOML) | `themes/turon-civic/i18n/*.toml` | ✅ |
| 3 | Language switcher partial | `themes/turon-civic/layouts/partials/language-switcher.html` | ✅ |
| 4 | hreflang head partial | `themes/turon-civic/layouts/partials/head-hreflang.html` | ✅ |
| 4.5 | AI translation disclosure partial | `themes/turon-civic/layouts/partials/ai-translation-disclosure.html` | ✅ |
| 5 | CSS additions (RTL + CJK) | `themes/turon-civic/static/css/tokens.css.diff` | ✅ |
| 6 | English source pages (2) | `content/endorsements.md`, `content/platform/uesf-questionnaire.md` | ✅ |
| 7 | Translation scaffolds (66) | `content/*.{lang}.md` | ✅ |
| 8 | AI translation disclosure source | `docs/Deliverable_8_AI_Translation_Disclosure_Source.md` | ✅ |
| 9 | FPPC footer disclosure | `docs/Deliverable_9_FPPC_Footer_Disclosure.md` | ✅ |
| 10 | llms.txt × 7 + robots.txt + sitemap.xml | `static/llms.*.txt`, `static/robots.txt`, `layouts/sitemap.xml` | ✅ |
| 11 | Translation workflow doc | `docs/Phase1_Translation_Workflow.md` | ✅ |
| 12 | Preflight + scorecard | `docs/Phase1_Preflight_Checklist.md` + `docs/Phase1_JEC_Scorecard.md` | ✅ |

---

## 3. Applying the build

### 3.1 Branch + apply
```bash
git checkout main
git pull
git checkout -b phase1-7lang-build
```

### 3.2 Copy bundle into checkout
```bash
# from the turonsf checkout root
cp -rv /path/to/turonsf_v1.3.0/content/.        ./content/
cp -rv /path/to/turonsf_v1.3.0/data/.           ./data/
cp -rv /path/to/turonsf_v1.3.0/docs/.           ./docs/
cp -rv /path/to/turonsf_v1.3.0/static/.         ./static/
cp -rv /path/to/turonsf_v1.3.0/themes/.         ./themes/
cp     /path/to/turonsf_v1.3.0/layouts/sitemap.xml ./layouts/sitemap.xml
```

### 3.3 Apply diffs
```bash
git apply /path/to/turonsf_v1.3.0/hugo.toml.diff
git apply /path/to/turonsf_v1.3.0/themes/turon-civic/static/css/tokens.css.diff
```

### 3.4 Operator-supplied verbatim text — none required

This build ships with **no operator-paste blockers**. The letter page (`/letters/uesf-2026-05-12/`) and the talk page (`/talk/`) were removed from v1.3.0 scope; they will ship in a later build (v1.3.1 or v1.4.0) once their content is locked. The UESF questionnaire page (`/platform/uesf-questionnaire/`) ships dormant with `is_active: false` and returns 404 in production until you flip the flag (gated on Alex Schmaus permission).

### 3.5 Build + preflight
```bash
hugo --minify --logLevel warn
```
Walk `docs/Phase1_Preflight_Checklist.md` top to bottom. Every BLOCKING item must be ✅.

### 3.6 Push for preview
```bash
git add -A
git commit -m "feat(i18n): v1.3.0 — Phase 1 + 7-language scaffolds"
git push -u origin phase1-7lang-build
```
Cloudflare Pages builds a preview. Walk every English page + spot-check each language home with the pending banner.

### 3.7 Sam Ray + Lauren review
- Sam Ray reviews `docs/Deliverable_8_AI_Translation_Disclosure_Source.md` and `docs/Deliverable_9_FPPC_Footer_Disclosure.md` (English sources). Per-language reference translations in D9 are flagged for Sam's batched review BEFORE any language promotes out of `placeholder`.
- Lauren reviews trust-strip credentials + FPPC footer treasurer name + financial figures.

### 3.8 Merge to main
After sign-offs in `docs/Phase1_Preflight_Checklist.md` Section 10, merge. The first production deploy ships with all non-English pages at `placeholder` (visible via language switcher with pending banner, noindex,follow, canonical to English). The Translation Pipeline v1 + Workflow run separately to promote pages through `ai_translated` → `reviewed` → `live`.

---

## 4. Locked constraints (preserved across v1.3.0)

- **Direction A design tokens:** `--navy-900`, `--accent`, `--cream-50`, font choices — UNCHANGED.
- **Trust strip Sequence F Option β:** Royal Caribbean $72M → SFUSD Parent → HelloFresh −$33M→+$9M → Cambridge — UNCHANGED, DOM order locked.
- **Three-pillar order:** Special Education → Budget Discipline → Teacher Retention — LOCKED.
- **Hero copy structure:** operator-credential anchored headline + three-pillar reference subheadline + dual CTA — UNCHANGED.
- **info@turonsf.com:** canonical email.
- **FPPC ID 1482971:** literal in every footer in every language.
- **Role tag:** "Data Scientist, SFUSD Parent" — NEVER JD / attorney / lawyer / Juris Doctor in any language.
- **No CMS, no translation widget:** markdown + git only.

---

## 5. OIL decisions ratified May 12, 2026

1. **Chinese script mapping:** Cantonese → `zh-Hant`; Mandarin → `zh-Hans`. SFUSD LAO match.
2. **AI translation methodology + disclosure:** AI-translated, transparently disclosed at top of every non-English page via `ai-translation-disclosure.html`; community-review channel info@turonsf.com; English canonical; non-dismissible disclosure.
3. **Launch scope:** existing v1.2.0 pages × 6 target languages. v1.3.0 ships scaffolds only; separate workflow runs translations.
4. **`/talk/` and `/letters/uesf-2026-05-12/`:** deferred from v1.3.0 scope (operator decision May 12, 2026). i18n infrastructure stays ready; pages re-add in a later build when their content is locked.

---

## 6. Three documented prompt-architecture divergences (resolved)

| # | Issue | Prompt position | Architecture position | Resolution | Documented in |
|---|---|---|---|---|---|
| 1 | llms.txt structure | 7 separate per-language files | 1 multilingual file | Follow PROMPT (7 separate files) | Scorecard §4 Cycle 2 |
| 2 | uesf-questionnaire path | Section: `content/platform/uesf-questionnaire/_index.md` | Single file: `content/platform/uesf-questionnaire.md` | Follow ARCHITECTURE (single file pattern consistent with pillars) | Scorecard §4 Cycle 1 |
| 3 | AI disclosure draft length | 28 words at Flesch 81 | 20 words | Converged at 18 words, Flesch 82, two i18n keys | Scorecard §4 Cycle 1 + D8 source doc |

---

## 7. JEC composite

**v1 composite: 92.46** (revised) — clears Heavy minimum (≥ 90). Up from 91.86 in the original scope: the scope reduction (letter + talk pages removed) eliminated the two operator-paste BLOCKING items, lifting Executability from 92 → 95 and removing two of the four Sam-Ray-sensitive content flags. Trade: a small loss on Voter Reach Fidelity (one fewer page surface in each language) is more than offset by the executability gain. See `docs/Phase1_JEC_Scorecard.md` for the revised dimension-by-dimension breakdown.

**v2 projection: 95.18** — clears stretch (≥ 95). Six v2 drivers remain (down from eight); the two paste-related drivers are retired.

---

## 8. Next steps after this bundle ships

1. **Pre-deploy (operator):** axe-DevTools audit on Cloudflare Pages preview; Mac Studio smoke test of full Hugo build; i18n key-parity CI check.
2. **Pre-first-language-promotion (Sam Ray):** batched review of six per-language FPPC footer reference translations.
3. **First 30 days post-deploy (operator + Nate Allbee):** one outreach call to each candidate community-review partner organization.
4. **When Translation Pipeline v1 ships:** Section 5 ten-step process in `Phase1_Translation_Workflow.md` is end-to-end validated; any drift drives v1.1 of the workflow doc.
5. **v1.3.1 patch (operator + Sam Ray):** add "Read in English →" link inside AI disclosure; add "Legal posture as of [date]" block to D8 source doc.

— end of MANIFEST.md
