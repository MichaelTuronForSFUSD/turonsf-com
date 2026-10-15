# v3 — Endorsement hub release notes

**Branch:** `v3-endorsement-hub` (local, not pushed)  
**Built:** 2026-10-14  
**v2 backup:** `~/www/turonsf_com_v2/` and local tag `v2-campaign-site-final`  
**Source package:** `~/Projects/Ryan School Board Campaign 2026/Website Redesign/` (October 4 redesign package; the `~/Downloads/Revised TuronSF/` copy holds files 01–05 and the manifest only)

## What changed

turonsf.com becomes a single page in all eight languages: Michael's July 20, 2026 withdrawal and his endorsements of Phil Kim, Alida Fisher, and Ryan Hazelton. Flow: status check → three candidate cards → shared questionnaire answers → where the answers differ → official voting information.

| Area | v3 |
|---|---|
| Home layout | `themes/turon-civic/layouts/index.html` renders the hub from `data/hub_copy.json` (copy) and `data/hub_links.yaml` (links). |
| Copy | Generated from the package's `09-localized-copy.json`. Dropped the draft labels and the local click-count demo. Removed "draft" from the meta description. Moved the status-check date from October 4 to October 14 (see verification). |
| Candidate CTAs | Each card has two equal outlined buttons: campaign website and ActBlue donate page. Links open in a new tab with `noopener noreferrer`, `referrerpolicy="no-referrer"`, and no UTM parameters. |
| Retired pages | About, Contact, Donate, Endorsements, Meet, Newsletter, Platform (and pillars, UESF questionnaire), Thank-you, and Volunteer are removed in all languages. `static/_redirects` sends each legacy URL to the same-language hub with a 302. |
| Navigation and footer | Nav links jump to sections of the page. The donate button is gone. The footer keeps the email link and the existing FPPC disclosure and copyright, unchanged in every language. |
| Translations | Non-English routes are `ai_translated` in `data/translation_status.yaml`. Each shows the AI disclosure bar and the package's "not yet reviewed by a human editor" note. Each is `noindex` with a canonical link to English and stays out of the sitemap until promoted to `reviewed`/`live`. |
| Analytics | Umami page views are unchanged. Candidate click events exist but are off: set `track_candidate_clicks = true` in `hugo.toml` to send an aggregate `candidate_cta` event (source `phil-donate`, etc.). The redesign spec asks for a privacy review and a public notice before this is turned on. |
| Removed integrations | Brevo form config script, preconnects to ActBlue/Action Network/Brevo. The CSP drops the Brevo/ActBlue form origins and sets `form-action 'none'`. |
| llms files | `static/llms.{lang}.txt` were regenerated from the hub copy. |
| Fixes | The skip link sat at `left:-999px`, which widened RTL pages to 1374px on phones; this also affects the live Arabic site today. The header is no longer sticky below 840px so it doesn't cover section anchors. |
| CI | `bin/check-utm-hygiene.sh` now reads unquoted (minified) hrefs. It fails if any non-campaign outbound link carries `utm_` parameters, and still requires UTMs on Michael's own ActBlue/Brevo links if any return. |

## Verification (2026-10-14)

- **Official status:** SF.gov's candidate page lists 8 people who filed for Board of Education (3 seats): Autumn Brown Garibay, Virginia Cheung, Alida Fisher, Ryan Hazelton, Phil Kim, Laurance Lee, Reina Tello, Tim Tung. Michael is not listed. The page gives no reason and does not say a withdrawal was accepted. The copy still says only that.
- **Questionnaires:** All four SF Parents Action PDFs (Kim, Fisher, Hazelton, Turon) were downloaded. Each scores 4 = "Strongly Agree" on the same five items (priorities, transparency dashboard, literacy and math, governance, budget health). None shows a submission date. This confirms the "What they said in common" copy, and the package's PDF blocker is cleared.
- **Links:** All 21 outbound URLs return HTTP 200. The Mission Local forum article returned 429 once and 200 on retry.
- **Build and CI scripts:** `hugo --minify --gc` builds with no warnings. i18n parity, JD references, translation status, UTM hygiene, and the FPPC footer check (9/9 pages) all pass.
- **Rendering:** All 8 routes were checked in a browser: one H1, 3 cards, 6 CTAs, correct `lang`/`dir`, and no horizontal overflow at 375px (Arabic included). Desktop was checked at 1280px.

## Still required before pushing to `main`

1. Michael approves the first-person statement and reasons as published copy.
2. A qualified human reviewer checks each of the seven translations, Arabic RTL rendering included. Promote each to `reviewed`/`live` only after that review.
3. Legal review of the FPPC footer on a page that now links to other committees' donation pages. The disclosure was kept verbatim as the package directs.
4. Close the old asks off-site: the `turonsf` ActBlue page, Brevo newsletter list/forms, and any Action Network forms still accept sign-ups or money on their own. Keep records as the committee directs.
5. Recheck the official candidate page and all links on the day of release.
6. Do a keyboard, screen-reader, and zoom pass. Only automated and visual checks were done here.

Pushing `main` deploys to Cloudflare Pages. To roll back, redeploy tag `v2-campaign-site-final`.

## Correction (2026-10-14)

Michael withdrew on **July 20, 2026**, not October 3 as the redesign package states. All eight languages are corrected in `data/hub_copy.json` (and the generated `llms.*.txt`):

- The opening statement now reads "On July 20, 2026, I chose to withdraw…".
- The voting section dropped two sentences that said the August 31 voter guide came before the decision and did not explain its effect on the ballot. Both stopped being true once the decision moved before August 31. The guide was checked: it does not mention Michael.

The source package in `~/Projects/.../Website Redesign/` still says October 3.

## Copy audit and rewrite (2026-10-14)

The English copy was checked claim by claim against its sources. Thirteen errors and overclaims were fixed, and the copy was rewritten to remove AI writing patterns. All seven translations were rewritten from the new English. Each language now links its own official voter guide. See `docs/V3_Red_Team_Audit_2026-10-14.md`. Translations remain `ai_translated` until a human native speaker reviews them.

## SEO and GEO pass (2026-10-15)

Added search titles naming the candidates, Open Graph/Twitter tags with a share image, JSON-LD, a visible last-updated date, real 404 pages, and Hugo-rendered `llms.txt` per language. Removed empty RSS feeds, fixed touch-target sizes, and renamed the site from the committee name to "Michael J. Turon". See `docs/V3_SEO_GEO_Audit_2026-10-15.md`. The largest remaining gap is that the translations stay noindex until a human reviews them.

## Translations made indexable (2026-10-15)

At the owner's direction, the seven translations are `ai_published`: indexable, in hreflang and the sitemap, and still carrying the AI-translation notice. Human native-speaker review is still recommended. Promote each language to `reviewed` afterward. Cantonese uses `hreflang="zh-HK"`.

## Final pre-launch audit (2026-10-15)

Fixed an `/en/*` redirect that hid the English sitemap, a CSP gap that blocks Umami (also affecting the live site), and CI pinned to an old Hugo version. Also removed a publicly served diff file, added a favicon, fixed one contrast failure, removed duplicate section labels, and made the 404 link a full-size button. See `docs/V3_Go_Live_Runbook.md` for the checklist, deploy steps, and rollback.
