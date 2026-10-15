# v3 go-live runbook

**Branch:** `v3-endorsement-hub` (local; `main` and `origin/main` are still at v2, `f5c0864`)  
**Hosting:** Cloudflare Pages project `turonsf-com`. **A git push does not deploy:** the GitHub→Pages auto-build has failed since 2026-05-27, so releases go out by Wrangler direct upload via `bin/deploy.sh`. The live site reports Hugo 0.160.1, the same version v3 is built and tested with.  
**Final audit:** 2026-10-15. See "What the final audit found and fixed" below.

## 1. Before you push (your decisions and off-site steps)

- [ ] **Approve the copy.** Read the English page and confirm the first-person sentences, especially "My own questionnaire answer is closest to Ryan's: no more delays."
- [ ] **Disclosure review.** The footer still reads "Paid for by Michael Turon for SFUSD Board of Education 2026. FPPC ID 1482971." on a page that now links to other committees' donation pages. Have your treasurer or counsel confirm the wording.
- [ ] **Close your own asks off-site.** The `turonsf` ActBlue page, the Brevo newsletter form, and any Action Network forms still accept sign-ups and money on their own. Close or redirect them, and keep records as the committee directs.
- [ ] **Recheck the official candidate list** at https://www.sf.gov/candidates-november-3-2026-general-election on launch day. If the date changes, update it in three places:
  - `data/hub_copy.json`: the date inside `status` and the `updated` line, in all 8 languages;
  - `data/hub_links.yaml`: `updated`.
- [ ] **Cloudflare login:** `wrangler whoami` lists the account that owns the `turonsf-com` Pages project.

## 2. Deploy

```bash
cd ~/www/turonsf_com
git switch main && git pull --ff-only
wrangler whoami            # must be the Cloudflare account that owns turonsf-com
./bin/deploy.sh
```

`bin/deploy.sh` stops unless Wrangler can see the `turonsf-com` project and the tree is clean. It then builds `public/`, runs every CI check, uploads with `wrangler pages deploy`, and runs the checks in section 3 against turonsf.com. If Wrangler is signed in to a different Cloudflare account (for example CARE Institute's), run `wrangler logout && wrangler login` and sign in to the turonsf.com account.

Pushing to GitHub keeps the repo and CI current but does not change the site.

## 3. Check the live site (about 5 minutes)

```bash
for u in / /es/ /yue-hant/ /ar/ /llms.txt /es/llms.txt /sitemap.xml /en/sitemap.xml /favicon.ico; do curl -s -o /dev/null -w "%{http_code} $u\n" "https://turonsf.com$u"; done
for u in /donate/ /platform/pillar-1/ /es/volunteer/ /llms.en.txt /give; do curl -s -o /dev/null -w "%{http_code} -> %{redirect_url}  $u\n" "https://turonsf.com$u"; done
curl -s -o /dev/null -w "%{http_code} /no-such-page/\n" https://turonsf.com/no-such-page/
curl -sI https://turonsf.com/ | grep -i content-security-policy | grep -o gateway.umami.is
```

**Expected:**
- The first loop returns 200 for every URL. In particular, `/en/sitemap.xml` returns 200, not a redirect.
- The second loop returns 301 to the same-language home page.
- `/no-such-page/` returns 404.
- The last command prints `gateway.umami.is`.

**Then:**
- [ ] Open the site on a phone and on a computer, and switch through all 8 languages.
- [ ] Umami → Realtime should show your visit.
- [ ] Google Search Console and Bing Webmaster Tools: submit `https://turonsf.com/sitemap.xml` and request indexing of `/`.
- [ ] Optional: run the URL through Google's Rich Results Test, and through a share-preview tool (Facebook Sharing Debugger or LinkedIn Post Inspector) to refresh the cached preview.

## 4. Roll back if needed

The fastest way: Cloudflare dashboard → Pages → the project → Deployments → the last v2 deployment → **Rollback**. This is instant and changes nothing in git.

To restore v2 in git as well:

```bash
git switch main
git revert --no-edit f5c0864..HEAD
git push origin main
```

v2 is also preserved at tag `v2-campaign-site-final` and in `~/www/turonsf_com_v2/`. Browsers that already followed one of the new 301 redirects may keep it cached for a while.

## What the final audit found and fixed (2026-10-15)

| Area | Finding | Fix |
|---|---|---|
| SEO | The `/en/*` redirect also caught `/en/sitemap.xml`, so Google would have been sent to the home page instead of the English sitemap | Rule narrowed to `/en/`. `bin/check-redirects.sh static/_redirects public` now fails CI if any rule would hide a real built file |
| Analytics | Umami now sends to `gateway.umami.is`, which the CSP blocked. **This is also blocking page-view counts on the live site today** | Added to `connect-src`; verified 200 from the browser under production headers |
| Analytics | Local and preview builds sent page views to the production Umami site | `data-domains="turonsf.com"` on the Umami script |
| CI | GitHub Actions has failed every run since at least May 27, because it pinned Hugo 0.125.7 and the site needs a newer version | Pinned to 0.160.1, matching production |
| Public files | `/css/tokens.css.diff`, an internal design diff, is publicly downloadable on the live site | Removed (kept in git history and the v2 backup) |
| Favicon | None. Every browser request for one hit the 404 page | `favicon.ico`, a 32px PNG, `apple-touch-icon.png`, and `theme-color` |
| Contrast | The translation-feedback link was 4.27:1 (WCAG AA needs 4.5:1) | Darkened to #964220 (5.8:1). All other text pairs pass (4.77–17.5:1) |
| Layout | Small labels repeated the section headings ("WHERE THEY AGREE" over "Where they agree") in every language | Removed from all four sections |
| Mobile | The 404 page's home link was under 24px tall | Now a 47px button |

**Verified after the fixes:**
- **Pages:** all 16 (8 home pages and 8 404 pages) are structurally valid HTML: one H1 each, no skipped heading levels, no duplicate IDs, every new-tab link has `noopener`.
- **Layout:** at 375px, 768px, and 1280px, every page has no horizontal scroll, no link under 24px, no text under 12px, and 6 equal candidate buttons.
- **Production headers** (local simulator applying `_headers`, `_redirects`, and Cloudflare's 404 rules): no CSP violations; X-Frame-Options and frame-ancestors work; old URLs return 301; unknown URLs return a localized 404.
- **Links:** all 26 unique outbound links return 200.
- **CI checks:** all pass.

**Not verifiable from here:** Cloudflare's actual `HUGO_VERSION` setting, Google/Bing indexing, and how the share preview looks inside each social app.
