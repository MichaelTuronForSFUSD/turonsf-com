# Phase 1 Deployment Run Guide — turonsf.com v1.3.0

**Document role:** Step-by-step operator guide from Mac Studio (TuronBoacStudio, user `turonbot`) to live turonsf.com v1.3.0. Assumes the v1.3.0 bundle is unpacked to a working directory and the build preflight (`Phase1_Preflight_Checklist.md`) has passed.
**Total estimated wall time:** 90–120 minutes for the full deploy. ~45 minutes if the existing turonsf.com Cloudflare account is already campaign-isolated (decision F2 in the audit).
**Pairs with:** `Phase1_Deployment_Red_JEC_Audit.md`, `Phase1_Deployment_Preflight.md`.

This Run Guide is laid out as numbered steps. Each step has:
- **Goal:** what the step accomplishes
- **Commands:** literal terminal blocks (zsh on Mac Studio; no `#` comments inside command blocks per operator preference)
- **Verify:** how to confirm the step worked
- **Reference:** which audit / preflight item this closes

---

## Prerequisites — Mac Studio one-time setup

Skip any item already in place. Mac Studio M4 Max, user `turonbot`.

### P1 — Homebrew
```zsh
which brew || /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew --version
```

### P2 — Hugo (pinned to 0.125.7 per Architecture Decision)
```zsh
brew install hugo
hugo version
```

If `hugo version` reports a different version, install the pinned version explicitly:
```zsh
brew install hugo@0.125.7
brew link --force hugo@0.125.7
```

### P3 — Git (already on macOS; verify version)
```zsh
git --version
git config --global user.name "Michael Turon"
git config --global user.email "your-campaign-scoped-email@turonsf.com"
```

The git email matters for FPPC attribution. Use a campaign-scoped email, not a CARE-or-personal address.

### P4 — GitHub CLI (optional but recommended for repo + PR workflow)
```zsh
brew install gh
gh auth login
```

Choose: GitHub.com → HTTPS → Login with web browser. The browser opens; complete the OAuth flow.

### P5 — Confirm Mac Studio working directory
```zsh
ls -la /www
```

Expected: `/www/CAREInstitute_ai/` directory already exists (the nonprofit site, separate concern). The campaign site will live as a sibling at `/www/turonsf_com/`.

If `/www` does not exist as a directory or you don't have write permission there, resolve that before proceeding — your existing CAREInstitute_ai install used this path, so the convention is already established on this machine.

---

## Step 1 — Unpack v1.3.0 bundle and apply to working tree

**Goal:** turn the v1.3.0 overlay bundle into a complete Hugo site checkout.
**Reference:** `MANIFEST.md` §3.

### 1.1 — Unpack the bundle
```zsh
cd /www
tar -xzf ~/Downloads/turonsf_v1.3.0.tar.gz
ls turonsf_v1.3.0/
```

Expected output lists: `MANIFEST.md`, `hugo.toml.diff`, `content/`, `data/`, `docs/`, `themes/`, `layouts/`, `static/`, `bin/`, `.github/`, `.gitignore`.

### 1.2 — Decision branch: fresh repo or apply to existing v1.2.0 checkout?

**Decision F2 from the audit** controls this. Two paths.

**Path A — Fresh repo, fresh GitHub org, fresh Cloudflare account (audit F2 option a).** Recommended; cleanly resolves FPPC entanglement risk. ~90 minutes total wall time.

**Path B — Apply v1.3.0 as an update to existing turonsf.com repo on existing Cloudflare account.** Only if Lauren + Sam Ray have confirmed the existing setup is already campaign-isolated. ~30 minutes total wall time. Skip to step 7.

The remainder of this guide assumes **Path A**.

### 1.3 — Initialize the fresh working tree
```zsh
cd /www
mkdir -p turonsf_com
cp -r turonsf_v1.3.0/. turonsf_com/
cd turonsf_com
ls -la
```

Expected: all bundle contents copied to `/www/turonsf_com/`. `.github/`, `.gitignore`, etc. visible.

### 1.4 — Apply Hugo config diff
```zsh
git init
git apply hugo.toml.diff || cp hugo.toml.diff hugo.toml
```

If `hugo.toml.diff` is the full file (not a patch), the cp works. If it's a patch against a v1.2.0 hugo.toml that needs to land in this fresh repo, manually copy the v1.2.0 hugo.toml first, then apply the diff. The bundle's MANIFEST §3.3 documents which form `hugo.toml.diff` takes.

### 1.5 — Apply CSS diff
```zsh
ls themes/turon-civic/static/css/
```

If `tokens.css.diff` is present and the directory does not have a `tokens.css`, copy the v1.2.0 baseline first. The diff applies via:
```zsh
cd themes/turon-civic/static/css
git apply tokens.css.diff
cd -
```

### 1.6 — Make CI scripts executable
```zsh
chmod +x bin/*.sh
```

### 1.7 — Verify the working tree builds
```zsh
hugo --minify --logLevel warn
```

Expected: zero warnings, build succeeds, `public/` directory populated.

**Verify:** open `public/index.html` in browser, confirm rendered home page looks correct.

---

## Step 2 — Create fresh GitHub organization

**Goal:** GitHub org dedicated to the campaign committee. Audit F1.
**Owner:** Michael (with Lauren copy on the FPPC-attribution side).

### 2.1 — Open GitHub in browser
Sign in as Michael (personal GitHub account, not CAREInstitute).

### 2.2 — Create the org
- Top-right avatar → "Your organizations" → "New organization"
- Plan: **Free**
- Org name: `MichaelTuronForSFUSD` (or operator-chosen alternative)
- Contact email: campaign-scoped (suggest `info@turonsf.com` once Cloudflare Email Routing is set up in step 4, or use a temporary Lauren-controlled inbox initially)
- This organization belongs to: My personal account (with FPPC attribution noted in the campaign records)

### 2.3 — Verify org isolation
After creation, confirm in browser:
- Org has no other members yet (Michael only)
- Org has no repos yet
- Org is NOT a child of CAREInstitute or any nonprofit-attributed org

**Reference closes:** Deployment Preflight §1.1.

---

## Step 3 — Create fresh Cloudflare account

**Goal:** Cloudflare account dedicated to the campaign committee. Audit F2.
**Owner:** Michael + Lauren (treasurer).

### 3.1 — Sign up
Visit `https://dash.cloudflare.com/sign-up`. Use a campaign-scoped email for registration.

The chicken-and-egg: turonsf.com email forwarding (which provides `info@turonsf.com`) requires the Cloudflare account to exist. Initial Cloudflare account email is therefore Lauren-treasurer-controlled inbox; once the account is set up and Email Routing configured (step 4), update the Cloudflare account email to a `*@turonsf.com` address.

### 3.2 — Add turonsf.com as a zone
- Cloudflare dashboard → "Add a Site"
- Enter `turonsf.com`
- Choose Free plan
- Cloudflare scans existing DNS records

**If turonsf.com is currently on a different Cloudflare account (v1.2.0 deploy):**
- The existing account must release the domain. Cloudflare → existing account → turonsf.com zone → "Advanced Actions" → "Remove Site"
- THEN add to new account
- DNS records will be re-imported from authoritative sources or manually copied

**If turonsf.com is currently on a different DNS provider:**
- Cloudflare provides nameservers (e.g., `chris.ns.cloudflare.com`, `sara.ns.cloudflare.com`)
- Update domain registrar to use these nameservers
- Wait for propagation (15 min – 2 hours typically)

### 3.3 — Verify zone is active
Dashboard shows `turonsf.com` with status "Active". Audit F12 path (a) selected.

**Reference closes:** Deployment Preflight §1.2, §1.3, §3.1.

---

## Step 4 — Set up Cloudflare Email Routing

**Goal:** `info@turonsf.com` routes to operator inbox, owned by the campaign account. Audit F5.

### 4.1 — Enable Email Routing
- Cloudflare dashboard → turonsf.com zone → Email → Email Routing → "Get Started"
- Cloudflare auto-creates the MX + SPF records
- Add destination: Michael's personal or Lauren's mailbox initially

### 4.2 — Create the info@ alias
- Email Routing → "Routes" → "Create address"
- Custom address: `info@turonsf.com`
- Action: Send to → (operator destination from 4.1)
- Save

### 4.3 — Test
From an external email account, send a test message to `info@turonsf.com`. Confirm receipt within 5 minutes.

**Reference closes:** Deployment Preflight §1.7, §5.10.

---

## Step 5 — Create fresh Umami Cloud account

**Goal:** Umami analytics property for turonsf.com, isolated from any CARE-related Umami. Audit F6.

### 5.1 — Sign up
Visit `https://cloud.umami.is`. Use a `*@turonsf.com` address now that Email Routing is set up (suggest `analytics@turonsf.com` → forward to operator).

### 5.2 — Create website property
- Umami dashboard → "Add website"
- Name: `turonsf.com (Phase 1)`
- Domain: `turonsf.com`
- Save

### 5.3 — Copy site_id and script tag
Umami shows:
- Website ID (UUID, e.g., `12345678-aaaa-bbbb-cccc-1234567890ab`)
- Tracking script: `<script defer src="https://us.umami.is/script.js" data-website-id="..."></script>`

Note the site_id. It goes into `hugo.toml` in step 6.

### 5.4 — Create the three Phase 1 dashboards
Per Analytics Spec §7:
- Dashboard 1: "Phase 1 conversion funnel"
- Dashboard 2: "Translation demand priority"
- Dashboard 3: "Pillar attention"

Each is configured via Umami's "Reports" or "Insights" interface; ~10 minutes each. Detailed steps in Analytics Spec §7.

**Reference closes:** Deployment Preflight §1.6, §5.1, §5.9.

---

## Step 6 — Configure hugo.toml with infrastructure IDs

**Goal:** wire Umami site_id, CTA destinations, language config into the build.

### 6.1 — Open hugo.toml
```zsh
cd /www/turonsf_com
$EDITOR hugo.toml
```

### 6.2 — Verify [params.umami] section
```toml
[params.umami]
  site_id = "PASTE-UMAMI-SITE-ID-FROM-STEP-5.3"
  script_url = "https://us.umami.is/script.js"
```

### 6.3 — Verify [params.cta_destinations] section
```toml
[params.cta_destinations]
  newsletter = "https://sibforms.com/serve/MUIFA..."
  donate     = "https://secure.actblue.com/donate/turonsf"
  volunteer  = "https://actionnetwork.org/forms/turonsf-volunteer"
  email      = "mailto:info@turonsf.com"
  platform   = "/platform/"
```

Replace placeholders with the actual Brevo signup form URL, ActBlue donate page URL, Action Network volunteer form URL. **These must be set before deploy.**

### 6.4 — Rebuild and verify Umami script renders
```zsh
hugo --minify
grep -c "us.umami.is" public/index.html
```

Expected: ≥ 1.

### 6.5 — Verify CTA shortcode wiring
```zsh
grep -oE "utm_source=turonsf" public/index.html | wc -l
```

Expected: ≥ 4 (one per outbound CTA on home page).

### 6.6 — Run CI scripts locally
```zsh
./bin/check-i18n-parity.sh
./bin/check-no-jd-references.sh
./bin/check-utm-hygiene.sh public/
./bin/check-fppc-footer.sh public/
./bin/check-translation-status.sh
```

All should report "OK". If any fail, fix before proceeding.

**Reference closes:** Deployment Preflight §5.1–§5.3, §6.1, §6.5.

---

## Step 7 — Push to GitHub

**Goal:** v1.3.0 lands in the fresh campaign GitHub org as the first commit on `main`.

### 7.1 — Create the repo via gh CLI
```zsh
cd /www/turonsf_com
gh repo create MichaelTuronForSFUSD/turonsf-com --public --source=. --remote=origin --description "Michael Turon for SFUSD Board of Education 2026 — campaign website"
```

If `gh` is not installed, create the repo manually at `https://github.com/organizations/MichaelTuronForSFUSD/repositories/new` then add the remote:
```zsh
git remote add origin https://github.com/MichaelTuronForSFUSD/turonsf-com.git
```

### 7.2 — Commit and push
```zsh
git add .
git status
```

Review the list. Confirm: no `.env*` files, no `*.draft.md`, no `notes/` content, no operator-private files. If anything looks wrong, do NOT proceed — fix `.gitignore` or remove the file before commit.

```zsh
git commit -m "feat(i18n): v1.3.0 Phase 1 + 7-language scaffolds"
git branch -M main
git push -u origin main
```

### 7.3 — Verify on GitHub
Browser → `https://github.com/MichaelTuronForSFUSD/turonsf-com`. Confirm:
- File tree matches local
- `.github/workflows/build-and-check.yml` present
- README or MANIFEST.md renders (if either is named appropriately)

### 7.4 — Enable repo settings
On the repo Settings page:
- General → Disable wikis (not needed)
- General → Disable Discussions (not needed)
- Pages → Source = None (audit F19)
- Code security → Enable secret scanning (audit F20)
- Code security → Enable Dependabot alerts
- Branches → Add branch protection rule for `main`:
  - Require pull request before merging (1 approval)
  - Require status checks to pass: `Phase 1 preflight checks`
  - Do not allow bypassing the above settings
  - Restrict who can push to admins only

**Reference closes:** Deployment Preflight §2.1–§2.8.

### 7.5 — Test the CI workflow
```zsh
git checkout -b ci-smoke-test
echo "# CI smoke test" >> SMOKE_TEST.md
git add SMOKE_TEST.md
git commit -m "ci: smoke test"
git push -u origin ci-smoke-test
gh pr create --title "ci: smoke test" --body "Verifies the CI workflow runs all preflight checks."
```

Wait ~3 minutes. Browser → repo Pull Requests → the PR. CI workflow runs. All checks should pass green. Close the PR without merging:
```zsh
gh pr close ci-smoke-test
git checkout main
git branch -D ci-smoke-test
git push origin --delete ci-smoke-test
```

**Reference closes:** Deployment Preflight §2.9.

---

## Step 8 — Connect Cloudflare Pages to GitHub repo

**Goal:** Cloudflare Pages auto-deploys on push-to-main.

### 8.1 — Create Pages project
- Cloudflare dashboard (campaign account) → Workers & Pages → Create → Pages → Connect to Git
- Authorize Cloudflare to access the `MichaelTuronForSFUSD` GitHub org (scope: this org only)
- Select repo: `turonsf-com`
- Project name: `turonsf-com`
- Production branch: `main`

### 8.2 — Build configuration
- Framework preset: Hugo
- Build command: `hugo --minify --gc`
- Build output directory: `public`
- Root directory: `/` (default)

### 8.3 — Environment variables
- `HUGO_VERSION` = `0.125.7`
- `NODE_VERSION` = `20` (or leave unset)

### 8.4 — Save and deploy
Click "Save and Deploy". Cloudflare clones the repo, builds Hugo, deploys.

Wait ~2–3 minutes. Preview URL appears: `turonsf-com.pages.dev`. Click through and verify the build deployed.

### 8.5 — Walk the preview build
On `https://turonsf-com.pages.dev/`, confirm:
- Home page renders correctly
- Utility bar shows election date + FPPC ID
- Hero shows role tag eyebrow, headline, primary CTA "Get campaign updates"
- Three pillars render with correct figures
- Footer carries FPPC disclosure
- Switch language to Spanish: AI disclosure renders OR pending notice renders (depending on translation_status)
- Switch to Arabic: RTL layout works, language switcher has "Read in English" promo

**Reference closes:** Deployment Preflight §4.1–§4.9.

---

## Step 9 — Attach custom domain turonsf.com

**Goal:** turonsf.com points to the Pages project.

### 9.1 — Add custom domain
Cloudflare Pages → turonsf-com project → Custom domains → Set up a custom domain
- Domain: `turonsf.com`
- Cloudflare auto-creates the DNS record (CNAME or A) and issues the SSL cert

### 9.2 — Wait for cert issuance
~30 seconds to ~5 minutes. Cloudflare shows "Active" when ready.

### 9.3 — Verify HTTPS works
```zsh
curl -sIv https://turonsf.com/ 2>&1 | head -20
```

Expected:
- HTTP/2 200 (or 308 if redirect)
- `server: cloudflare`
- Cert chain visible, issued by Cloudflare or Let's Encrypt

### 9.4 — Configure www → apex redirect
Cloudflare zone → Rules → Redirect Rules → Create rule:
- Name: `www to apex`
- Match: `Hostname` equals `www.turonsf.com`
- Action: Static redirect → `https://turonsf.com/{path}` with status 301

### 9.5 — SSL/TLS settings
Cloudflare zone → SSL/TLS:
- SSL/TLS encryption mode: **Full (Strict)**
- Edge Certificates → "Always Use HTTPS" = ON
- Edge Certificates → "Automatic HTTPS Rewrites" = ON

### 9.6 — Add CAA record
Cloudflare zone → DNS → Add record:
- Type: CAA
- Name: `@` (apex)
- Tag: `issue`
- Value: `pki.goog`

Add a second CAA record with value `letsencrypt.org` for fallback.

Add a third CAA record:
- Tag: `iodef`
- Value: `mailto:info@turonsf.com`

**Reference closes:** Deployment Preflight §3, §4.10–§4.12.

---

## Step 10 — Verify production deploy + walk smoke test

**Goal:** v1.3.0 is live, observable, and correct. Final pre-lock confidence step.

### 10.1 — Open production URL
Browser → `https://turonsf.com/`. Confirm everything renders.

### 10.2 — Walk Deployment Preflight §7
Every BLOCKING item in `Phase1_Deployment_Preflight.md` Section 7 — execute now, mark each ✅.

### 10.3 — Verify Umami events fire
- Browser → click hero "Get campaign updates" button (don't actually submit Brevo form — just trigger the click event)
- Umami dashboard → Live view → confirm `newsletter_cta_click` event appears within 5 seconds
- Repeat for donate, volunteer, language switcher

### 10.4 — Verify analytics dashboards populate
After 5 minutes of test traffic, the three Phase 1 dashboards should show:
- Phase 1 conversion funnel: at least page_view + cta_click impressions
- Pillar attention: pillar_click events for each pillar
- Translation demand priority: language_pending_notice_view counts per language

### 10.5 — Send test message to info@turonsf.com
From an external account (Gmail, etc.), send a test email. Confirm receipt at operator destination within 5 minutes.

### 10.6 — Validate security headers
```zsh
curl -sI https://turonsf.com/ | grep -iE "(content-security-policy|x-frame-options|x-content-type-options|referrer-policy|permissions-policy)"
```

Expected: all five headers present per `_headers` file.

### 10.7 — Validate redirects
```zsh
curl -sI https://www.turonsf.com/ | grep -iE "^(http|location)"
curl -sI https://turonsf.com/give/ | grep -iE "^(http|location)"
```

Expected: 301 redirects to `https://turonsf.com/` and `https://turonsf.com/donate/` respectively.

### 10.8 — Submit to Search Console
- Google Search Console → Add property `turonsf.com`
- Verify via TXT record (Cloudflare zone → DNS → add TXT record)
- Submit sitemap: `https://turonsf.com/sitemap.xml`

**Reference closes:** Deployment Preflight §7, §8, §5.5–§5.7, §5.10.

---

## Step 11 — Rollback procedure (reference, not executed)

If v1.3.0 ships broken — anything from a build failure to a content issue — these are the rollback paths in order of speed.

### Fast rollback (< 60 seconds): Cloudflare Pages deployment rollback
1. Cloudflare dashboard → Workers & Pages → turonsf-com → Deployments
2. Find the last good v1.2.x deployment
3. Three-dot menu → "Rollback to this deployment"
4. Confirm
5. The previous build is now serving traffic

### Medium rollback (~2 minutes): git revert + push
```zsh
cd /www/turonsf_com
git log --oneline -n 5
git revert HEAD
git push origin main
```

Cloudflare detects the new commit, builds, deploys. Site returns to the pre-revert state.

### Heavy rollback (~5 minutes): hard reset to v1.2.x tag
```zsh
git tag -l "v1.2.*"
git reset --hard v1.2.x-last
git push --force origin main
```

Use only if `git revert` doesn't cleanly resolve the issue and the v1.3.0 commit must be excised from history. Force-push is normally prohibited by branch protection; admin override required.

**Reference closes:** Deployment Preflight §9.

---

## Step 12 — Lauren + Sam Ray sign-off

**Goal:** treasurer and counsel close the §10 sign-off block on the Deployment Preflight.

### 12.1 — Lauren walkthrough
Walk Lauren through the live site on iPhone + desktop. Confirm:
- FPPC §84305 footer on every page
- FPPC ID 1482971 visible in footer + utility bar
- Treasurer name "Lauren Turon" in footer in every language
- Trust strip financial figures unchanged from v1.2.0
- ActBlue donate flow reaches an ActBlue page with UTMs intact
- info@turonsf.com receives test mail

Get Lauren's verbal or written sign-off; record in Preflight §10.

### 12.2 — Sam Ray batched review
Send Sam the four items queued from prior audits as a single email:
- D8 AI translation disclosure source string (English) — `docs/Deliverable_8_AI_Translation_Disclosure_Source.md`
- D9 FPPC footer per-language reference translations — `docs/Deliverable_9_FPPC_Footer_Disclosure.md`
- Pillar 2 "most expensive board-oversight miss" claim phrasing (live URL or rendered HTML)
- Pillar 3 strike-fund disclosure phrasing (live URL)
- Plus: this Deployment Run Guide + Deployment Audit for Sam's review of F1, F2, F4 entanglement defense

Expected turnaround: 48–72 hours.

Apply Sam's notes (if any). Sam returns sign-off in writing. Record in Preflight §10.

### 12.3 — Final lock
After both sign-offs land, the v1.3.0 deploy is FPPC-defensible and ready for promotion. Lock the version: tag the commit `v1.3.0`.

```zsh
git tag v1.3.0
git push origin v1.3.0
```

---

## Appendix A — Common Cloudflare gotchas

**"DNS only" vs "Proxied" toggle:** for the apex `turonsf.com` A/CNAME record, set to "Proxied" (orange cloud) so Cloudflare's edge serves the request. For TXT and CAA records, "DNS only" is fine.

**Pages custom domain stuck on "Verifying":** wait 5 minutes. If still stuck, remove and re-add the custom domain.

**Cert reissuance failure:** check CAA records — if you added a CAA record that doesn't include Cloudflare's authorized CA, the cert can't issue. Either widen CAA or wait for the existing cert to renew normally.

**Build fails with "Hugo version not found":** confirm `HUGO_VERSION` env var is set in Pages project settings to `0.125.7`.

**Build succeeds but pages 404 on live domain:** confirm output directory is `public` (not `dist` or `build`).

---

## Appendix B — Operator quick-reference command bundle

For repeated workflows after first deploy. All commands run from `/www/turonsf_com/`.

| Task | Command |
|---|---|
| Local preview | `hugo serve --buildDrafts --buildFuture` |
| Local production build | `hugo --minify --gc` |
| Run all CI checks locally | `./bin/check-i18n-parity.sh && ./bin/check-no-jd-references.sh && ./bin/check-utm-hygiene.sh public/ && ./bin/check-fppc-footer.sh public/ && ./bin/check-translation-status.sh` |
| Create branch + PR | `git checkout -b feat/<name>; git add -A; git commit -m "<message>"; git push -u origin feat/<name>; gh pr create` |
| Promote a translation to reviewed | Edit `data/translation_status.yaml` → flip status; commit; push |
| Add an endorser | Edit `data/endorsements.yaml` → append entry; commit; push |
| Trigger redeploy without code change | Cloudflare Pages → Deployments → "Retry" on latest |
| Watch live Umami events | Umami dashboard → Live view |

---

## Sign-off

| Role | Name | Date | Signature |
|---|---|---|---|
| Operator | Michael Turon | | |
| Counsel | Sam Ray | | |
| Treasurer | Lauren Turon | | |

— end of `Phase1_Deployment_Run_Guide.md`
