# v3 hub — SEO and GEO audit, 2026-10-15

**Scope:** the built v3 site (`v3-endorsement-hub` branch), all 8 language routes, checked against the local Hugo build and preview.  
**Limits:** Lighthouse isn't installed here, so it wasn't run. The checks below follow its SEO audit list and were done by hand on the built HTML and in a 375px mobile viewport. Nothing here can guarantee rankings or citations by AI assistants. Those depend on Google, Bing, and the AI providers, and on links from other sites.

## Scorecard

**SEO (English page; the Lighthouse SEO audits plus common extras)**

| Check | Before | After |
|---|---|---|
| Page is indexable (English) | Pass | Pass |
| `<title>` names the person, topic, and candidates (≤ 60 chars) | Fail: "My school board decision and endorsements" | Pass: "Michael Turon endorses Kim, Fisher, Hazelton for SFUSD board" (60) |
| Meta description present, ≤ 160 chars | Pass (138) | Pass. Spanish and Filipino trimmed from 161/169 to 153/149 |
| Canonical URL | Pass | Pass |
| hreflang | Pass (English + x-default; translations excluded while noindex) | Pass |
| Descriptive link text | Pass | Pass |
| Crawlable anchors, HTTP 200 | Pass | Pass |
| robots.txt valid, sitemap listed | Pass | Pass |
| Structured data (JSON-LD) | Fail: none | Pass: `WebSite`, `Person` (Michael), and `WebPage` with `dateModified`, `about` (Nov. 3 election), and `mentions` (the three candidates and their sites). Parses in the minified build |
| Social preview (Open Graph / Twitter) | Partial: no image, site name, or locale | Pass: 1200×630 image, `og:site_name`, `og:locale` per language, `summary_large_image` |
| Site name | Fail: "Michael Turon for SFUSD Board of Education"; Chinese versions said he is running (參選) | Pass: "Michael J. Turon" in every language. The FPPC footer and committee name are unchanged |
| Real 404 page | Fail. Without `404.html`, Cloudflare Pages serves the home page with status 200 for any bad URL (duplicate content). This also affects the live v2 site | Pass: `404.html` per language, `noindex` |
| Empty RSS feeds | Fail: 8 empty feeds | Pass: removed |
| Visible last-updated date | Fail | Pass: "Last updated October 14, 2026" with `<time datetime>` and matching `dateModified` |
| Mobile: no horizontal scroll | Pass | Pass (all 8 routes) |
| Mobile: touch targets ≥ 24px (WCAG 2.2) | Fail: 18 links at 18–22px; language links used 11.5px text | Pass: 0 under 24px; language links 31px tall, 12.8px text |

**GEO (being found and cited by AI assistants)**

| Check | Before | After |
|---|---|---|
| Content is in server-rendered HTML (no JS needed) | Pass | Pass |
| AI crawlers allowed in robots.txt (GPTBot, ClaudeBot, PerplexityBot, Google-Extended, etc.) | Pass | Pass |
| `/llms.txt` at the root | Fail: only `llms.en.txt` etc. | Pass: `/llms.txt` plus `/<lang>/llms.txt`, in llmstxt.org format with links |
| llms files match the page | Fail: written once by a script outside the repo, so they would drift | Pass: Hugo renders them from `data/hub_copy.json` and `data/hub_links.yaml`. Old `llms.<lang>.txt` URLs 301 to the new ones |
| Clear answer in the first paragraph (who, what, when) | Pass | Pass |
| Claims attributed and linked to primary sources | Pass (after the Oct. 14 copy audit) | Pass |
| Machine-readable entities | Fail | Pass (JSON-LD above) |
| Freshness signal | Fail | Pass (visible date and `dateModified`) |
| Consistent names (Michael J. Turon; candidates' full names) | Pass | Pass |

## Translations are indexable (owner's decision, 2026-10-15)

The seven translated pages are now `ai_published` in `data/translation_status.yaml`, a new status meaning "AI-translated, published for search, not yet human-reviewed". Each page:

- canonicalizes to itself and has no `noindex`;
- is listed in hreflang on every page (8 languages plus x-default) and in its language sitemap;
- still shows the AI disclosure bar and the "not yet reviewed by a human editor" note.

When a native speaker reviews a language, change its status to `reviewed`. Nothing else changes.

The Cantonese page uses `hreflang="zh-HK"`, because Google accepts only ISO 639-1 language codes and `yue` isn't one. Its `lang` attribute stays `yue-Hant`.

**Risk to weigh:** these pages are now visible in Spanish, Chinese, Filipino, Vietnamese, and Arabic search results. Any translation error is now public under Michael's name, and the AI notice is the only safeguard until review.

## Other recommendations (not done)

1. **After deploying,** submit `https://turonsf.com/sitemap.xml` in Google Search Console and Bing Webmaster Tools, and request indexing of the home page. Bing's index feeds ChatGPT search and Copilot.
2. **Links from elsewhere** (the candidates' sites, local coverage of the endorsement) will matter more for ranking than anything on the page. That's outside this repo.
3. **Refresh the date** in `data/hub_copy.json` (`updated`, and the date in `status`) and `data/hub_links.yaml` (`updated`) whenever the official candidate list is rechecked.

## Files changed

- `hugo.toml`: site title, `og_image`, `og_locale` per language, `llms` output format, RSS removed.
- `themes/turon-civic/layouts/_default/baseof.html`: title and description from hub data, Open Graph and Twitter tags, JSON-LD, 404 noindex.
- `themes/turon-civic/layouts/partials/hub-jsonld.html`: new.
- `themes/turon-civic/layouts/index.llms.txt`: new.
- `themes/turon-civic/layouts/404.html`: new.
- `themes/turon-civic/layouts/index.html`: visible updated date.
- `themes/turon-civic/static/css/site.css`: touch targets, language bar on narrow screens, updated-date style.
- `data/hub_copy.json`: SEO titles; `updated`, `notfound_title`, and `notfound_link` in 8 languages; Spanish and Filipino descriptions shortened.
- `data/hub_links.yaml`: `updated` date.
- `static/img/og-endorsements.png`: new share image.
- `static/_redirects`: old llms URLs.
- `static/robots.txt`: llms references.
- `static/llms.*.txt`: removed (now rendered).
- `content/_index.*.md`: titles and descriptions kept in step.

## Follow-up corrections, same day (web and mobile)

- **Official status rechecked Oct. 15:** SF.gov still lists 8 Board of Education filers without Michael. The status line and "last updated" now read October 15 in all 8 languages, and `dateModified` is 2026-10-15.
- **Old campaign URLs are now 301 (permanent).** That passes their link value to the hub. Restoring v2 means removing these rules, and some browsers may keep a cached 301 for a while.
- **Fixed three broken redirect rules** (`/yue-hant/`, `/zh-hant/`, `/zh-hans/` thank-you-volunteer) that had no space between source and destination. Added `bin/check-redirects.sh` to CI so this can't recur.
- **Touch targets:** the header section links, the translation-feedback link, and "Fil" in the language bar are now at least 24×24px. On 375px, 768px, and 1280px screens, 0 links are under 24px in all 8 languages, with no horizontal scroll.
- **Equal buttons on desktop:** on screens 841px and wider, the three candidate cards use a CSS subgrid. Headings, text, links, and both buttons line up and are the same size across cards.
- **Stylesheet is fingerprinted** (`/css/site.min.<hash>.css` with SRI), and CSS/JS get a one-year immutable cache header. Deploys can't leave visitors on stale styles, and repeat visits load faster.
