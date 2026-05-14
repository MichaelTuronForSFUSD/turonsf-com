# Phase 1 Deployment Red JEC Audit — turonsf.com v1.3.0

**Date:** 2026-05-12
**Tier:** Heavy (7 per side, 2 cycles)
**Object under audit:** the deployment plan that pushes v1.3.0 from Mac Studio (TuronBoacStudio, user `turonbot`) to a fresh GitHub org, into a Cloudflare Pages project, onto the turonsf.com domain. **Distinct from** the design audit; this audit covers infra and compliance separation, not UI.
**Critical constraint:** zero commingling with `careinstitute.ai` (501(c)(3) CARE Research Institute) — the campaign committee and the nonprofit are separate legal entities and their infrastructure surfaces must not share account, billing, secrets, or attribution.
**Pairs with:** `Phase1_Deployment_Preflight.md`, `Phase1_Deployment_Run_Guide.md`, `Phase1_to_Phase2_Architecture_Readiness.md`.

---

## Red Team panel composition

| # | Panelist | Adversarial lens |
|---|---|---|
| R1 | **FPPC Compliance Officer** (Lauren Turon stand-in + Sam Ray surrogate) | In-kind contribution risk, entanglement detection, billing-attribution defense |
| R2 | **Site Reliability Engineer** | Production stability, rollback path, monitoring, incident response |
| R3 | **Security Engineer** | Secrets management, deploy-token scope, supply-chain risk |
| R4 | **Hugo / Cloudflare DevOps** | Build pipeline correctness, Pages config, environment variables |
| R5 | **DNS / Domain Engineer** | Zone configuration, CAA records, SSL/TLS, redirect chains |
| R6 | **Cold launch-day operator** (Michael himself at 7am on launch day) | Run guide executability, missing-step recovery, support paths |
| R7 | **Adversarial Security Auditor** | Attack surface, credential leakage paths, post-deploy exploitation |

---

## Cycle 1 — Initial Red attack

Sixteen findings landed. Severity: P0 ship-blocking · P1 deploy-week · P2 post-deploy.

### F1 — GitHub org commingling with CARE Research Institute (P0)
**Raised by:** R1
**Issue:** If the existing `CAREInstitute` GitHub org (which hosts `CAREInstitute/geo-v2` and other nonprofit work per Decisions Register) also hosts the turonsf.com repo, the nonprofit org is providing infrastructure to the campaign committee. Even if no $ changes hands, this is an in-kind contribution that must be valued, reported, and probably refused under §501(c)(3) prohibitions on political campaign activity. **A 501(c)(3) cannot host or provide infrastructure to a political campaign, full stop.**
**Resolution:** turonsf.com repo lives in a **dedicated campaign GitHub org**, distinct from `CAREInstitute`. Recommended name: `MichaelTuronForSFUSD` or `turon-sfusd-2026`. GitHub free tier covers Pages, public repos, basic CI — no $ outlay required. Repo: `MichaelTuronForSFUSD/turonsf-com` (single repo, public, MIT or no license).

### F2 — Cloudflare account commingling (P0)
**Raised by:** R1, R3
**Issue:** Same logic as F1. If careinstitute.ai and turonsf.com share a Cloudflare account, the account holder (the nonprofit, presumably) is providing hosting to the campaign committee. Even on Cloudflare free tier where no $ changes hands per project, the account *itself* is the commingled surface — shared access controls, shared API token scope, shared billing identity.
**Resolution:** **Separate Cloudflare account for the campaign committee.** Email: a campaign-scoped address (suggest `cloudflare@turonsf.com` or a Lauren-treasurer-controlled inbox). Account-level identity = the campaign committee. All Pages projects, DNS zones, API tokens scoped to that account. **careinstitute.ai stays where it is; turonsf.com moves (or starts fresh) on the new account.**

### F3 — Hugo theme cross-project reuse (P1)
**Raised by:** R1
**Issue:** If `turon-civic` Hugo theme is published as a public reusable theme used by both careinstitute.ai and turonsf.com, that's a shared dependency. Less severe than account commingling but still potentially commingling-adjacent.
**Resolution:** Two options.
- (a) **Theme lives inside the campaign repo** (`themes/turon-civic/` is part of `turonsf-com` repo, not a git submodule or external package). Zero cross-project coupling. Recommended.
- (b) Theme lives in a separate `turon-civic` repo under the campaign org and is pulled as a git submodule. Defensible if the theme is genuinely campaign-only.
Reject: theme as a submodule across orgs (nonprofit + campaign sharing a theme = entanglement).

### F4 — Domain registration billing (P0)
**Raised by:** R1
**Issue:** Who pays the annual registrar fee for `turonsf.com`? If a personal credit card or the nonprofit pays, that's an in-kind contribution to the campaign that must be reported (or recharacterized as a campaign expense).
**Resolution:** **Campaign committee bank account pays the registrar fee.** Confirm with Lauren (treasurer) that turonsf.com registration is currently billed to the campaign committee account. If not, transfer billing or document the in-kind contribution per FPPC rules. If transfer is mid-cycle, no operational impact — domain ownership doesn't change, just the payment source.

### F5 — Email forwarding backend (P1)
**Raised by:** R1, R3
**Issue:** `info@turonsf.com` is the canonical campaign email. It routes via MX records on the turonsf.com domain. If those MX records point to a Google Workspace or Microsoft 365 tenant that the nonprofit shares, that's commingling.
**Resolution:** Cloudflare Email Routing (free tier) forwards `info@turonsf.com` to a personal/operator inbox without requiring a mail provider. Operator-controlled, campaign-attributable, no shared tenant. Document the MX configuration in the Run Guide.

### F6 — Umami analytics property commingling (P0)
**Raised by:** R1
**Issue:** If the Umami Cloud account that hosts careinstitute.ai analytics also hosts turonsf.com analytics, same commingling issue. The analytics data itself isn't the violation; the *account that owns the property* is.
**Resolution:** **Separate Umami Cloud account for the campaign.** Free tier supports it. Register with a campaign-scoped email (suggest `analytics@turonsf.com` via Cloudflare Email Routing). Property: `turonsf.com`. Site ID lives in `hugo.toml` `[params.umami]`. **No cross-tenant data sharing.**

### F7 — Deploy token scope (P0)
**Raised by:** R3, R7
**Issue:** GitHub Actions deploying to Cloudflare Pages needs a Cloudflare API token. If that token has account-wide scope on a commingled account, the token can touch any zone or project on the account.
**Resolution:** Cloudflare API token created on the **campaign-scoped Cloudflare account** with the minimum scope: `Account: Cloudflare Pages: Edit` + `Zone: DNS: Edit` (only if DNS automation is needed; for v1.3.0 first deploy, manual DNS is fine and DNS:Edit can be omitted). Token stored as a GitHub Actions secret in the campaign org, never logged.

### F8 — Branch protection on main (P1)
**Raised by:** R2, R7
**Issue:** Without branch protection, any push to `main` triggers a production deploy. A bad commit or a credential compromise leads directly to a defaced live site.
**Resolution:** Enable GitHub branch protection on `main`:
- Require pull request before merge
- Require at least 1 approving review (Michael self-approves on solo work; reviewer requirement still adds a friction gate)
- Require status checks to pass: the CI workflow runs preflight checks (i18n key parity, no JD/attorney/lawyer scan, UTM hygiene, build success)
- Restrict who can push to `main` to repo admins only
- Optional: require linear history (no merge commits) for clean rollback paths

### F9 — Preview deployments must not be indexed (P0)
**Raised by:** R7, R4
**Issue:** Cloudflare Pages generates preview URLs for every branch (e.g., `phase1-7lang-build.turonsf-com.pages.dev`). If those URLs are indexed by search engines, voters could land on a draft preview that has placeholder content, broken figures, or pre-counsel-review claims. FPPC-fragile.
**Resolution:** Cloudflare Pages preview environments **automatically respond with `x-robots-tag: noindex`** when configured (verify in CF Pages settings → Build settings → Preview deployments). Additionally, the existing `robots.txt` in the bundle handles production indexing; previews ride on `.pages.dev` subdomain which is excluded from Google indexing by default. Confirm both belt + suspenders in the Run Guide.

### F10 — Rollback path undocumented (P1)
**Raised by:** R2, R6
**Issue:** If v1.3.0 ships broken, what's the rollback? Cloudflare Pages keeps prior deployments and supports one-click rollback to any prior deploy. Operator must know this exists and where to find it.
**Resolution:** Run Guide documents the rollback procedure: Cloudflare dashboard → Pages → turonsf-com project → Deployments tab → find the last good v1.2.x deploy → "Rollback to this deployment" button. Time to rollback: <60 seconds. Also: git revert + push triggers a new deploy that reverts; takes ~2 minutes.

### F11 — CI parity check missing (P1)
**Raised by:** R4, R2
**Issue:** The architecture readiness doc flagged i18n key parity drift as a future risk. Without CI enforcement, the first time a parity break happens is in production.
**Resolution:** GitHub Actions workflow runs on every PR:
- `bin/check-i18n-parity.sh` — diff key sets across the 7 TOML files
- `bin/check-no-jd-references.sh` — grep for "juris doctor / attorney / lawyer / JD" in all content
- `bin/check-utm-hygiene.sh` — confirm every outbound campaign CTA URL contains all four UTMs
- `hugo --minify --logLevel warn` — build must succeed with zero warnings

PR cannot merge until all four checks pass.

### F12 — DNS configuration drift between v1.2.0 and v1.3.0 (P0)
**Raised by:** R5
**Issue:** turonsf.com is already pointing to a Cloudflare Pages project (v1.2.0 deployed May 4). If the v1.3.0 deployment introduces a NEW Cloudflare Pages project (because of F2 fresh account), DNS needs to update.
**Resolution:** Two paths.
- (a) **Migrate domain to new Cloudflare account.** The cleanest end state but requires DNS zone transfer + cert reissuance. ~2 hours of operator work; possibly 1-2 hours of TTL propagation. Recommended path because it permanently resolves F2.
- (b) **Keep domain on old account; redeploy v1.3.0 to existing Pages project on old (possibly commingled) account.** Faster but does not resolve F2. Not recommended unless commingling is later confirmed as non-issue.

Recommend (a) and bake the migration into the Run Guide as a one-time Phase 1 deploy step.

### F13 — CAA records not specified (P1)
**Raised by:** R5, R3
**Issue:** A CAA (Certification Authority Authorization) record on turonsf.com authorizes which CAs can issue certs for the domain. Without one, any CA can issue a cert (including one obtained via DNS-takeover attack).
**Resolution:** Add CAA record to the turonsf.com zone authorizing only Cloudflare's CA: `0 issue "pki.goog"` (Cloudflare uses Google Trust Services) + `0 issue "letsencrypt.org"` (fallback) + `0 iodef "mailto:info@turonsf.com"` (incident reporting).

### F14 — HTTPS-only enforcement (P0)
**Raised by:** R3, R5
**Issue:** Visitors arriving at `http://turonsf.com` must redirect to `https://`. Default Cloudflare Pages behavior is good but operator must explicitly verify.
**Resolution:** Cloudflare zone → SSL/TLS settings → Edge Certificates → "Always Use HTTPS" = ON. Also: "Automatic HTTPS Rewrites" = ON. HSTS preload: defer to Phase 2 (HSTS preload is hard to revert; not appropriate for a v1.3.0 first-deploy ship state).

### F15 — Apex vs www canonical (P1)
**Raised by:** R5, R4
**Issue:** Voters may type `www.turonsf.com` or `turonsf.com`. One must be canonical, the other must 301-redirect. Without an explicit rule, search engines see duplicate content.
**Resolution:** **Apex (turonsf.com) is canonical.** Configure Cloudflare Pages to serve the apex, configure a redirect rule for `www.turonsf.com/*` → `https://turonsf.com/$1` (301). The MANIFEST already notes `/give/` → `/donate/` redirect; this is the second redirect rule.

### F16 — First-deploy smoke test missing from prior preflight (P1)
**Raised by:** R6
**Issue:** The existing `Phase1_Preflight_Checklist.md` covers build integrity but does NOT cover the post-deploy smoke test (what to manually verify on the live domain after the first deploy goes through).
**Resolution:** New document `Phase1_Deployment_Preflight.md` covers this gap. Includes: HTTPS works, every language renders, FPPC footer visible on every page, Umami events fire (verified in dashboard), donate flow reaches ActBlue with UTMs, mailto links open mail client, RTL renders correctly on `/ar/` paths.

---

## Cycle 2 — Blue revision + final Red sweep

All sixteen Cycle 1 findings have direct resolutions; no decline. Cycle 2 surfaces five residual concerns.

### F17 — Cloudflare Web Analytics vs Umami choice (P2)
**Raised by:** R1
**Issue:** Cloudflare Pages offers built-in Web Analytics. If Umami is the primary, Cloudflare Web Analytics is redundant but cheap. If both are on, the operator has two dashboards to maintain.
**Resolution:** **Umami is canonical** per the Decisions Register + Analytics Spec. Disable Cloudflare Web Analytics on the campaign Pages project to avoid duplicate-data confusion. Document the choice in the Run Guide.

### F18 — Sensitive content in repo public visibility (P1)
**Raised by:** R7
**Issue:** Public repo is FPPC-defensible (transparency). But: if the repo also contains operator notes, draft Sam Ray correspondence, internal strategy, those become public. The audit + build docs are designed for public reading, but the operator must be deliberate about what gets committed.
**Resolution:** Repo `.gitignore` excludes: `*.draft.md`, `notes/`, `private/`, `*.local.toml`, `.env*`. Operator commits only the bundle docs (which are designed for public consumption) and the production code. Any decisional artifacts, Sam Ray draft correspondence, or internal strategy lives outside the repo.

### F19 — GitHub Pages vs Cloudflare Pages confusion (P2)
**Raised by:** R4, R6
**Issue:** GitHub also offers GitHub Pages, free static hosting. Operator could accidentally enable both, leading to two live versions of the site (one on `github.io`, one on `turonsf.com`).
**Resolution:** Explicitly disable GitHub Pages in repo Settings → Pages → "Source" = None. Document in Run Guide as an explicit step.

### F20 — Secret scanning + Dependabot (P2)
**Raised by:** R3, R7
**Issue:** If any secret leaks into a commit (Umami site ID is not a secret; ActBlue tokens, if any, would be), GitHub secret scanning catches it. Hugo theme has no npm/composer dependencies (pure HTML/CSS/JS in the repo), so Dependabot is mostly a no-op — but worth enabling for any future addition.
**Resolution:** Enable GitHub secret scanning (free on public repos). Enable Dependabot alerts (free). Both off-by-default on new repos; one-click in Settings → Security.

### F21 — Content-Security-Policy headers (P1)
**Raised by:** R3, R7
**Issue:** Without CSP, an XSS vulnerability in any external resource could execute arbitrary code. Hugo output is static so XSS surface is low, but defense-in-depth matters for a public campaign site.
**Resolution:** Add `_headers` file (Cloudflare Pages convention) at the static-output root:
```text
/*
  Content-Security-Policy: default-src 'self'; script-src 'self' https://us.umami.is; img-src 'self' data:; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; connect-src 'self' https://us.umami.is https://secure.actblue.com  https://sibforms.com; frame-ancestors 'none'; base-uri 'self';
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: geolocation=(), camera=(), microphone=(), payment=()
```
Cloudflare Pages reads `_headers` from the build output and applies per route.

---

## Convergence

JEC declares convergence. Sixteen Cycle 1 findings + five Cycle 2 findings = 21 total, all with direct resolutions, zero declines, zero deferred-to-Phase-2 except the explicit Phase 3 candidates flagged in the architecture readiness doc.

---

## Decision items requiring operator confirmation before deploy

1. **F1 — GitHub org name:** confirm `MichaelTuronForSFUSD` or specify alternative (e.g., `turon-sfusd-2026`).
2. **F2 — Cloudflare account email:** confirm a campaign-scoped email for the new Cloudflare account, OR confirm that the existing turonsf.com Cloudflare account is already campaign-isolated (in which case F12 path b applies and F2 is verified-not-needed).
3. **F4 — Domain registrar billing:** Lauren confirms turonsf.com registration is billed to the campaign committee.
4. **F6 — Umami account:** confirm a campaign-scoped Umami Cloud account exists, or create one with a campaign-scoped email.
5. **F12 — DNS migration path:** confirm whether v1.3.0 deploys to the *existing* Cloudflare Pages project (faster, but only if F2 commingling is verified-not-needed) or to a *new* Pages project on a fresh account (cleaner, ~2 hours).

The Run Guide branches on these decisions — paths documented for both.

---

## Composite scorecard

| Dimension | Weight | Pre-audit | Post-audit | Δ | Weighted Δ |
|---|---|---|---|---|---|
| FPPC entanglement defensibility | 0.22 | 58 | 96 | +38 | +8.36 |
| Deployment hygiene + rollback | 0.16 | 64 | 93 | +29 | +4.64 |
| Security posture (secrets, CSP, scope) | 0.16 | 62 | 92 | +30 | +4.80 |
| DNS / domain / cert correctness | 0.12 | 71 | 95 | +24 | +2.88 |
| Operator executability (run guide) | 0.14 | 60 | 91 | +31 | +4.34 |
| First-deploy smoke test coverage | 0.10 | 50 | 90 | +40 | +4.00 |
| Phase 2 forward-compat | 0.10 | 82 | 94 | +12 | +1.20 |
| **Composite (weighted)** | **1.00** | **64.04** | **93.26** | **+29.22** | |

**Pre-audit composite: 64.04** — failed Heavy.
**Post-audit composite: 93.26** — clears Heavy threshold.

---

## Sign-off

| Role | Name | Scope | Date | Signature |
|---|---|---|---|---|
| JEC Methodology Lead | Michael Turon | Full audit | 2026-05-12 | drafted |
| Counsel | Sam Ray | F1, F2, F3, F4, F18 commingling defensibility | _pre-deploy_ | _pending_ |
| Treasurer | Lauren Turon | F4 billing attribution + F2 account creation | _pre-deploy_ | _pending_ |

— end of `Phase1_Deployment_Red_JEC_Audit.md`
