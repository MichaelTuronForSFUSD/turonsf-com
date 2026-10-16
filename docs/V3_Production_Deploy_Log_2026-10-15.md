# v3 production deploy log — 2026-10-15

**Result:** turonsf.com is serving the v3 endorsement hub in all 8 languages.  
**Final deployment:** `8f61f82c` (https://8f61f82c.turonsf-com.pages.dev), commit `25eb261`, uploaded with `bin/deploy.sh` (Wrangler direct upload).  
**Cloudflare:** Pages project `turonsf-com` in *Michael@turon.com's Account* (`67085892385248117e242d8307f8e5b5`). Wrangler is signed in as info@turonsf.com.  
**GitHub:** `main` pushed as Turon-SF. `gh` on this Mac now uses Turon-SF; CARE-ADM is still signed in but inactive.

## What happened

1. **First git push** (`f5c0864..b8de171`) was rejected for CARE-ADM, which has read-only access. After the GitHub CLI was authorized as Turon-SF, the push succeeded.
2. **The push did not deploy.** Cloudflare's GitHub-connected builds failed for `b8de171` and `f65c253`, as they have since May 27. `bin/deploy.sh` was added, mirroring careinstitute.ai's Wrangler deploy script.
3. **Wrangler login.** It first reached only CARE Institute's Cloudflare accounts. It was then signed in as info@turonsf.com; the project is in Michael@turon.com's Account.
4. **First Wrangler deploy** (`a9d6df11`, commit `ab71179`) was live, but production ignored every `_redirects` rule after #101 of 174. Arabic, Simplified Chinese, Filipino, and Vietnamese legacy URLs returned 404. That's far below Cloudflare's documented limits (2,000 static / 100 dynamic).
5. **Fix** (`25eb261`): the file was collapsed to 84 rules, one splat per retired page per language, keeping `/en` and `/en/` exact so they can't swallow `/en/sitemap.xml`. `bin/check-redirects.sh` now fails at more than 100 rules, and `deploy.sh` checks late-file redirects. Redeployed as `8f61f82c`.

## Verified live after the final deploy

- **Pages:** 200 for all 8 language home pages, `/llms.txt`, `/es/llms.txt`, `/sitemap.xml`, `/en/sitemap.xml`, `/robots.txt`, favicon, touch icon, and share image.
- **Redirects:** all 84 rules tested live (158 URL variants, with and without trailing slash). Each returns 301 to the right same-language page.
- **404s:** unknown URLs (English and Arabic) return 404 with the localized page. `/css/tokens.css.diff` is gone (404).
- **Headers:** the CSP includes `gateway.umami.is`, and a live page view returned 200, so Umami is counting again.
- **Indexing:** hreflang lists all 8 languages plus x-default (Cantonese as `zh-HK`). Translations are self-canonical. JSON-LD is present.
- **Rendering:** no console errors. Phone (375px, Arabic RTL): no horizontal scroll, 0 tap targets under 24px, 6 buttons. Desktop (1280px): cards on the grid, buttons aligned across all three candidates.

## Still to do (outside the code)

- Submit `https://turonsf.com/sitemap.xml` in Google Search Console and Bing Webmaster Tools, and request indexing of `/`.
- Refresh share previews (Facebook Sharing Debugger, LinkedIn Post Inspector) so old v2 cards update.
- The next careinstitute.ai deploy needs `wrangler login` as info@careinstitute.ai, because Wrangler on this Mac is now signed in to turonsf.com's Cloudflare.
- The Cloudflare↔GitHub auto-build for `turonsf-com` is still connected but fails on every push. Either fix the connection or disconnect it so failed builds stop appearing; `bin/deploy.sh` is the release path either way.
