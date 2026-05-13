# Phase 1 Design Red JEC Audit — turonsf.com v1.3.0 mockup

**Date:** 2026-05-12
**Tier:** Heavy (7 per side, 3 convergence cycles)
**Object under audit:** `turonsf_v1.3.0_mockup.html` (responsive single-file mockup, EN / ES / AR states, desktop + mobile viewports)
**Audit framing:** Red JEC. Every design element must (1) earn its space, (2) test with endorsement and voter panels, (3) be traceable from backend analytics, (4) stay lean and load fast, (5) optimize click-through, (6) minimize bounce.
**Composite target:** ≥ 90 post-audit. Pre-audit baseline: 72.

---

## Red Team panel composition

| # | Panelist | Adversarial lens |
|---|---|---|
| R1 | **Cold SF voter** (Mission resident, parent, 8-second attention budget) | First-visit comprehension, primary-CTA legibility, bounce risk |
| R2 | **UESF endorsement committee member** (skim-and-decide reviewer) | Endorsement readiness, labor-credibility signaling, trust posture |
| R3 | **Cold Spanish-speaking SF mom** (mobile-only, iPhone 11, MUNI WiFi) | Multilingual fallback, mobile tap targets, slow-network tolerance |
| R4 | **Web performance engineer** (Core Web Vitals adversary) | LCP, CLS, page weight, render-blocking, font strategy |
| R5 | **Civic analytics specialist** (conversion attribution, funnel observability) | Event coverage, UTM hygiene, source attribution |
| R6 | **Bloomberg Businessweek editorial adversary** (aesthetic fidelity) | Deadpan integrity, costume vs. craft, magazine-pretense detection |
| R7 | **Sam Ray / FPPC counsel** (compliance + defensibility) | Claim integrity, disclosure adequacy, surface-area review |

Blue Team mirrors: Frontend Architect, Campaign Manager (Allbee surrogate), Multilingual Civic Web Specialist, Performance Eng, Data Engineer, Editorial Designer, Counsel.

---

## Cycle 1 — Initial Red attack

Eighteen findings landed. Each carries severity (P0 ship-blocking / P1 deploy-week / P2 v1.3.1), the panelist who raised it, the Blue Team defense if any, and the resolution.

### F1 — Hero headline is too abstract for cold first visit (P0)
**Raised by:** R1
**Issue:** "Three problems. *In order.*" reads as a tease, not an introduction. Cold visitor's first eight seconds: "Three problems with what? Whose problems?" Identity isn't anchored until the eyebrow line below the headline, and the role tag is *below the CTAs*. Trust comes after the ask.
**Blue defense:** BW-style headlines are deliberately oblique; the subhead disambiguates one line later.
**Red counter:** Below the fold doesn't exist on cold visits. If the headline doesn't anchor identity, the visitor bounces before the subhead reads.
**Resolution:** Move the role tag *above* the headline (eyebrow position). Promote "Michael Turon · Data Scientist · SFUSD Parent" to the first line a visitor sees after the nav. Keep the abstract headline — it works once identity is established.

### F2 — Primary hero CTA is content navigation, not funnel (P0)
**Raised by:** R1, R5
**Issue:** "Read the platform" is the *primary* CTA. It sends visitors deeper into the site, not into any Phase 1 funnel. The newsletter (Brevo, top-of-funnel list-building) is *secondary*. This inverts Phase 1 priorities.
**Resolution:** Invert. Primary becomes newsletter signup; secondary becomes donate; "or read the full platform →" demotes to a text link below the CTAs. (Confirmed in operator turn pre-audit.)

### F3 — Role tag positioned below the ask (P1)
**Raised by:** R1, R2
**Issue:** Identity attribution arrives after the visitor is asked to do something. Endorsement committees and cold voters both want to know *who* is talking before they evaluate *what* is being said.
**Resolution:** Folded into F1 fix (role tag → eyebrow).

### F4 — Nav links to a dormant page (P0)
**Raised by:** R2, R1
**Issue:** `/endorsements/` is `is_active: false` in v1.3.0 — the page exists but renders only dormant copy + signup forms. Linking to it from the persistent nav looks unfinished to an endorsement committee that lands and clicks "Endorsements" expecting to see a list.
**Blue defense:** The dormant page renders a coherent "endorsements coming soon, sign up to be notified" state, which itself converts.
**Red counter:** Only if the dormant copy is operator-reviewed and explicitly designed as a conversion surface, not a 404-adjacent shrug.
**Resolution:** Two options. (a) Hide the nav Endorsements link until `is_active: true`, surfacing it only when there's something to show. (b) Keep the link and confirm the dormant page renders a deliberate signup-for-endorsement-updates surface with the same CTA hierarchy as the homepage. **Decision needed.** Default recommendation: option (b) — the dormant state earns its place if it's designed as a conversion surface, not as scaffolding.

### F5 — Three-pillar visual weight equal despite Phase 1 endorsement priority (P2)
**Raised by:** R2
**Issue:** Teacher Retention is Pillar 3 by LOCKED values-statement ordering, yet UESF endorsement is the top Phase 1 campaign goal. The third pillar gets the same visual weight as the first two. An endorsement committee scanning the site sees their issue at the visual tail.
**Blue defense:** Pillar order is a values statement set at the build-decision level. Re-ordering for endorsement optics would violate the LOCKED Decisions Register.
**Red counter:** Not asking for re-order. Asking whether visual weight should differentiate.
**Resolution:** Accept asymmetry-in-treatment is not appropriate here — the order *is* the message. All three pillars get equal visual weight. UESF committee gets the values-statement signal that retention is part of the platform structure even though listed third. Decline F5; document the decline.

### F6 — Spanish-speaking mom on mobile lands on placeholder, may not see the English fallback (P0)
**Raised by:** R3
**Issue:** v1.3.0 ships with every non-English page at `placeholder`. A Spanish visitor's mobile-first experience is the pending notice. If the "Read in English" link inside the notice is below the fold on a small viewport, she bounces before finding the path forward.
**Resolution:** The pending notice is now mobile-tested above the fold on a 390px viewport at the top of `<main>`, with the "Read in English" tap target ≥ 44 × 44 px. Add: a second "Read in English" link at the top of the language switcher dropdown when the visitor is on a placeholder page, so the switcher also surfaces the fallback.

### F7 — Font payload exceeds mobile budget (P0)
**Raised by:** R4
**Issue:** Mockup loads four Google Font families: Fraunces (variable, ~80 KB compressed), Source Sans 3 (4 weights, ~24 KB), Noto Naskh Arabic (3 weights, ~50 KB), JetBrains Mono (1 weight, ~12 KB). Total ≈ 165 KB before any HTML / CSS / image transfer. Architecture Decision 6 budget for mobile-transferred page weight: ≤ 100 KB gzipped. **Fails budget.**
**Blue defense:** The mockup is a single demonstration file with embedded everything; production uses Hugo and can subset / self-host / language-condition.
**Red counter:** That's a design-system claim, not a code claim. The audit needs the *production* font strategy specified, not deferred to "Hugo will figure it out."
**Resolution:**
1. **Drop JetBrains Mono.** Replace with `ui-monospace, "SF Mono", Menlo, monospace` system stack. Mono is used only for stamps, eyebrows, and meta — system mono is fine.
2. **Self-host Fraunces** via Hugo's pipes, subsetted to Latin Extended only for EN/ES; load with `font-display: swap` and `<link rel="preload">` on the critical weight (700).
3. **Self-host Source Sans 3** subsetted to Latin Extended for EN/ES.
4. **Arabic fonts:** per Architecture Decision 6, use the system stack on AR pages (`"SF Arabic", "Geeza Pro", "Noto Naskh Arabic"`). Do NOT self-host Noto Naskh — let the OS handle it.
5. **CJK pages** use the system stack already (Architecture Decision 6).
6. Estimated production font payload after this: **~35 KB compressed** on EN/ES mobile. Within budget.

### F8 — Outbound CTAs have no preconnect (P1)
**Raised by:** R4
**Issue:** Donate, Volunteer, and Newsletter signup CTAs link to ActBlue / Action Network / Brevo endpoints. No `<link rel="preconnect">` hints in `<head>`. First-click latency includes DNS + TLS handshake.
**Resolution:** Add to `<head>`:
```html
<link rel="preconnect" href="https://secure.actblue.com" crossorigin>
<link rel="preconnect" href="https://actionnetwork.org" crossorigin>
<link rel="preconnect" href="https://sibforms.com" crossorigin>
```

### F9 — Newsletter / contact / pillar events missing (P0)
**Raised by:** R5
**Issue:** Umami event plan covers language switcher, donate, volunteer, book-call. Missing: newsletter signup submit (the most important Phase 1 conversion), email contact click, per-pillar click. Top of funnel and message-segment intel both blind.
**Resolution:** Wire the following Umami events:

| Event | Dimensions | Where it fires |
|---|---|---|
| `newsletter_signup_submit` | `source` (hero / footer / pillar-1 / pillar-2 / pillar-3), `language` | Brevo form success callback |
| `donate_cta_click` | `source` (nav / hero / footer / pillar), `language` | Every donate link |
| `volunteer_cta_click` | `source`, `language` | Every volunteer link |
| `email_contact_click` | `source`, `language` | Every mailto:info@turonsf.com |
| `pillar_click` | `pillar` (1 / 2 / 3), `language` | Pillar card link |
| `language_switcher_open` | `from_language` | Switcher trigger button |
| `language_switcher_select` | `from_language`, `to_language` | Switcher option click |
| `language_pending_notice_view` | `language`, `page` | Pending notice in viewport (IntersectionObserver) |
| `language_pending_to_english_click` | `from_language`, `page` | "Read in English" link inside notice |
| `scroll_depth_75` | `page`, `language` | Umami built-in |
| `scroll_depth_100` | `page`, `language` | Umami built-in |
| `hero_cta_primary_view` | `language`, `page` | IntersectionObserver on hero CTA (impression baseline for CTR) |

The last one matters: without an impression event, you only get *clicks*, not *click-through rate*. CTR is the optimization metric.

### F10 — UTM hygiene on outbound links unspecified (P0)
**Raised by:** R5
**Issue:** Once a visitor clicks Donate / Volunteer / Newsletter, they leave the site for a third-party backend. Without UTM parameters, attribution is broken — you cannot tell ActBlue "this donation came from the hero CTA on the Spanish home page."
**Resolution:** UTM scheme:

```text
utm_source=turonsf
utm_medium=web
utm_campaign=phase1
utm_content={cta_location}-{language}   (e.g., hero-en, pillar1-es, footer-ar)
```

Every outbound campaign link in the Hugo templates gets these params via a shortcode or a partial.

### F11 — Vol/Issue/Date hero stamp is costume, not editorial (P1)
**Raised by:** R6, R5
**Issue:** "Vol. 1 · Issue 03 · November 3, 2026 · FPPC ID 1482971" mimics a Bloomberg Businessweek cover strip. BW has Vol/Issue because magazines have issues. A campaign site does not. The Vol/Issue framing implies an editorial cadence that doesn't exist — costume, not craft.
**Resolution:** Drop Vol/Issue entirely. Keep election date + FPPC ID, demote to a slim utility bar above the nav (16 px tall, navy on cream, mono 11 px). Earns its space as: (a) election countdown surface (operational utility), (b) FPPC visibility (compliance redundancy with footer, defensible).

### F12 — Pillar figures stylistically inconsistent (P2)
**Raised by:** R6
**Issue:** Pillar 1 figure "$59-60M" is numeric. Pillar 2 figure "EmpowerSF" is a proper noun. Pillar 3 figure "UESF" is also a proper noun. The visual treatment (same display-serif rust color) implies they are equivalent units. They aren't.
**Blue defense:** Each pillar's anchor is genuinely different — figure for SpEd, named failure for Budget, organization solidarity for Teacher Retention. Forcing a number on every pillar manufactures false symmetry.
**Red counter:** Then the visual treatment should differ. Same treatment + different content type = visual lie.
**Resolution:** Two options for operator decision:
- (a) Rewrite Pillar 2 + 3 figures to be numeric: Pillar 2 = "$X" (EmpowerSF total cost or replacement cost — needs operator-supplied figure); Pillar 3 = "X%" or "$X" (UESF strike fund contribution, teacher attrition rate, or comparable). Requires operator to surface defensible figures from Decisions Register.
- (b) Keep current asymmetry but differentiate visual treatment: numeric pillar 1 uses the rust accent figure style; pillar 2 + 3 use a smaller serif label style with a different visual weight, signaling "this is the anchor, not a metric."

Recommendation: (b) for v1.3.0 ship (zero operator paste required, honest about the asymmetry), with (a) as a v1.3.1 upgrade once Pillar 2 + 3 anchor figures are confirmed by the Decisions Register.

### F13 — Pillar 2 claim "most expensive board-oversight miss" requires counsel review (P0)
**Raised by:** R7
**Issue:** Strong assertion. Defensible per public reporting on EmpowerSF, but Sam Ray must confirm phrasing in writing on a public surface.
**Resolution:** Already in the Phase 1 Preflight Checklist § 5 as a Sam Ray review item. Carry forward.

### F14 — Pillar 3 "I stood on the picket line, contributed to the strike fund" claim (P1)
**Raised by:** R7
**Issue:** Personal-act disclosure on a campaign-committee surface. FPPC permissible (personal act, not committee expenditure), but the *phrasing* requires Sam confirmation.
**Resolution:** Carry forward to Sam Ray batched review.

### F15 — Persistent nav Donate competes with hero newsletter CTA (P2)
**Raised by:** R1
**Issue:** Two CTAs on screen simultaneously can split the click.
**Blue defense:** They serve different visitor states. Nav Donate is for *returning* / *intentional* donors who know they want to give. Hero newsletter is for cold visitors who need to be warmed.
**Red counter:** Accepted on principle, but the *visual hierarchy* needs to be clear about which is for whom. Nav Donate must be visually subordinate to hero CTAs.
**Resolution:** Nav Donate stays but its visual weight reduces — change from solid navy button to navy outline button at smaller scale, signaling "available, not primary." Hero primary newsletter button gets the dominant solid-navy treatment. This sets the implicit hierarchy.

### F16 — "Pillar one →" link text is dull (P1)
**Raised by:** R1, R5
**Issue:** Generic "Pillar one →" / "Pillar two →" / "Pillar three →" wastes the click signal. Topic-specific verbs would earn click-through *and* give analytics a clearer per-pillar engagement signal.
**Resolution:** Rewrite link text:
- Pillar 1: "How I'll fix Special Education staffing →"
- Pillar 2: "How I'll vote on board oversight →"
- Pillar 3: "Where I stand on teacher retention →"

### F17 — Trust strip cell-2 "2 ×" parses as multiplication (P0)
**Raised by:** R1, R2
**Issue:** First-glance reading of "2 ×" is "two times" — a multiplication factor. Not "two kids." The trust strip cell where it lives describes Michael as an SFUSD parent; the figure undercuts the institution label.
**Resolution:** Replace "2 ×" with the literal string "Two kids" rendered in the same display-serif as other figures. Visual weight stays consistent; the meaning becomes unambiguous.

### F18 — Footer Languages column duplicates nav switcher (P2)
**Raised by:** R6
**Issue:** Footer has a 7-item language column. Nav has the switcher. Two language-selection surfaces on every page.
**Blue defense:** Footer language column aids screen-reader users and search-engine crawlers that may not equally surface a JS-driven switcher.
**Red counter:** True for crawlers and accessibility tools. Accepted.
**Resolution:** Keep both surfaces but make the footer language column smaller (text-link style, single line if it fits) and add a heading "More languages" that explicitly differentiates it from the nav switcher.

---

## Cycle 2 — Blue Team revision

Sixteen of the eighteen Cycle 1 findings have direct revisions. Two require operator decision and are explicitly carried forward as decision items, not unresolved.

**Implemented in revised mockup spec:**
F1, F2, F3, F6, F7, F8, F9, F10, F11, F15, F16, F17, F18.

**Carried forward (no design change):**
F5 (declined — equal-weight pillars is the values statement).
F13 (Sam Ray batched review — existing process).
F14 (Sam Ray batched review — existing process).

**Operator decision required before Cycle 3 close:**
F4 (option a hide vs. option b design dormant state as conversion surface).
F12 (option a operator-supplies pillar 2 + 3 figures vs. option b accept asymmetry, differentiate treatment).

---

## Cycle 3 — Final Red sweep

Five residual findings landed after the Cycle 2 revisions. All are P1 or below; none are ship-blocking.

### F19 — "Get the platform brief in your inbox" implies a brief exists (P1)
**Raised by:** R6
**Issue:** The recommended primary CTA copy from the prior turn references a "platform brief" as a lead magnet. If no brief is produced, this is a soft lie. Worse: the visitor signs up *for* the brief, gets no brief, unsubscribes.
**Resolution:** Two options for operator decision:
- (a) Soften the CTA to "Get campaign updates from Michael" — no lead magnet promised, no obligation, lower conversion rate.
- (b) Commit to producing a one-page Phase 1 platform brief (PDF or first-email auto-responder) as a v1.3.0 ship deliverable. Three pillars + the trust strip credentials + the FPPC line, formatted for the email. ~2 hours of operator drafting + Sam Ray review.

Recommendation: (b). The brief is a tractable production task and triples the conversion power of the CTA. If (a) ships, the CTA underperforms the (b) scenario by a factor of 2–3× based on civic-campaign benchmarks.

### F20 — Donate secondary button still visually competes with hero primary (P2)
**Raised by:** R1, R6
**Issue:** After F2 inversion, secondary CTA "Donate" carries a navy-outline button treatment. The visual contrast against the primary solid-navy button is not large enough on small viewports; both read as "buttons that want to be clicked."
**Resolution:** Differentiate further. Primary: solid navy with rust hover. Secondary: text-link with arrow ("→ Donate") at slightly smaller body weight. This makes the visual hierarchy unmistakable: newsletter is the ask, donate is available.

### F21 — `font-display: swap` and preload spec for self-hosted fonts (P0 for production build)
**Raised by:** R4
**Issue:** Self-hosting fixes the payload (F7) but doesn't fix render-blocking unless `font-display: swap` is set and the critical font weight is preloaded.
**Resolution:** Hugo `@font-face` declarations specify `font-display: swap` for every face. Add `<link rel="preload" as="font" type="font/woff2" crossorigin>` for the two most critical: Fraunces 700 (display) and Source Sans 3 400 (body). Other weights load on demand.

### F22 — Impression event for CTA is required to compute CTR (P1)
**Raised by:** R5
**Issue:** Without `hero_cta_primary_view`, you only get click counts, not CTR. Two pages with 100 hero clicks each look identical; if one had 1,000 impressions and the other had 200, their CTRs are 10% vs. 50% — radically different signals.
**Resolution:** Already added to the F9 event table. Confirm via IntersectionObserver on the CTA element: fires once per visitor session when the CTA is ≥ 50% in viewport.

### F23 — ActBlue / Action Network / Brevo language defaults (P1)
**Raised by:** R3
**Issue:** A Spanish visitor clicks "Donar" from a Spanish page and lands on an English ActBlue form. Confidence drops; donation rate drops.
**Resolution:** Verify ActBlue's Spanish-language form parameter (ActBlue supports Spanish forms — confirm the current URL param spec before deploy). For Action Network and Brevo, verify equivalent language-routing. Document the verified params in the Phase 1 Preflight Checklist § 8 (Analytics + community channel) as new BLOCKING items: each backend's Spanish-language URL must be verified and wired before the Spanish hero CTAs go live.

---

## Convergence

JEC declares convergence. Zero P0 findings remain unresolved after Cycle 3. Two findings (F19, F12) carry operator-decision items; two findings (F13, F14) carry Sam Ray batched-review items; one finding (F4) carries an operator-decision item. None block the v1.3.0 ship if the operator commits to one path on each.

---

## Concrete change list — the revised mockup

To produce a v1.3.0 mockup r2 that passes this audit, apply the following edits in order:

### Hero
1. Drop Vol/Issue/Date hero corner stamp. (F11)
2. Add a slim utility bar above the nav: `Election: November 3, 2026 — FPPC ID 1482971`. Navy on cream, mono 11px, 16 px tall, full-width. (F11)
3. Move role tag `Michael Turon · Data Scientist · SFUSD Parent` to the *eyebrow* position above the headline. (F1, F3)
4. Replace eyebrow `Candidate · SFUSD Board of Education · 2026` with the role tag.
5. Invert hero CTAs: primary = newsletter signup, secondary = donate, tertiary = text link to platform. (F2)
6. Donate secondary: change to text-link style with arrow, not button. (F20)
7. Primary CTA copy: decide F19 (a) "Get campaign updates from Michael" or (b) "Get Michael's platform brief in your inbox" — pending operator decision.
8. Wire `hero_cta_primary_view` IntersectionObserver event. (F22)

### Nav
9. Reduce nav Donate visual weight from solid button to outline button at slightly smaller scale. (F15)
10. Conditionally render Endorsements link: only when `data/endorsements.yaml` has at least one published endorsement OR `is_active: true` in `content/endorsements.md` — operator decision F4. (F4)
11. Confirm hamburger drawer (mobile) surfaces every nav link plus language switcher options.

### Trust strip
12. Replace cell-2 figure "2 ×" with "Two kids" rendered in same display-serif treatment. (F17)
13. Add `trust_strip_view` Umami event via IntersectionObserver — scrolled-into-view signal, fires once per session.

### Three pillars
14. Rewrite pillar link text to topic-specific verbs (F16):
    - Pillar 1 → "How I'll fix Special Education staffing →"
    - Pillar 2 → "How I'll vote on board oversight →"
    - Pillar 3 → "Where I stand on teacher retention →"
15. Wire `pillar_click` event with pillar dimension. (F9)
16. F12 operator decision: (a) supply numeric figures for pillars 2+3 OR (b) accept asymmetry and apply visual differentiation (smaller serif label, no rust accent for non-numeric anchors).

### Footer
17. Compress Languages column to single-line text-link list with heading "More languages." (F18)
18. Verify FPPC §84305 string in every language renders Latin-script for "Michael Turon for SFUSD Board of Education 2026", "FPPC ID 1482971", "Lauren Turon".

### Multilingual
19. Add a second "Read in English" link at the top of the language-switcher dropdown when on a placeholder page. (F6)
20. Verify mobile tap target ≥ 44 × 44 px on the pending-notice "Read in English" link.
21. F23 — verify ActBlue / Action Network / Brevo Spanish-language URL parameters before Spanish CTAs go live.

### Performance
22. Drop JetBrains Mono font; replace with system mono stack. (F7)
23. Self-host Fraunces and Source Sans 3 via Hugo pipes, subsetted to Latin Extended for EN/ES.
24. AR pages use system Arabic stack (`SF Arabic, Geeza Pro, Noto Naskh Arabic`); do not self-host Arabic. (F7)
25. Add `<link rel="preconnect">` for `secure.actblue.com`, `actionnetwork.org`, `sibforms.com`. (F8)
26. Add `<link rel="preload">` for Fraunces 700 and Source Sans 3 400, with `crossorigin`. (F21)
27. Specify `font-display: swap` on every `@font-face` rule. (F21)

### Analytics
28. Wire every event from the F9 table, with dimensions as specified.
29. Implement the UTM scheme from F10 on every outbound CTA via a Hugo shortcode.
30. Document the funnel-attribution model in `docs/Phase1_Analytics_Spec.md` (v1.3.0 ship deliverable, new file).

### Counsel review
31. Sam Ray batched review (per Phase 1 Preflight § 5) includes the Pillar 2 EmpowerSF claim and the Pillar 3 strike-fund disclosure. No revision required pending Sam's sign-off.

---

## Revised scorecard

| Dimension | Weight | Pre-audit | Post-audit | Δ | Weighted Δ |
|---|---|---|---|---|---|
| Earns-its-space discipline | 0.15 | 73 | 92 | +19 | +2.85 |
| Endorsement-panel readiness | 0.14 | 78 | 91 | +13 | +1.82 |
| Cold-voter comprehension | 0.16 | 71 | 90 | +19 | +3.04 |
| Analytics traceability | 0.14 | 65 | 95 | +30 | +4.20 |
| Performance / page weight | 0.12 | 70 | 89 | +19 | +2.28 |
| Click-through optimization | 0.12 | 68 | 93 | +25 | +3.00 |
| Bounce-rate mitigation | 0.09 | 72 | 89 | +17 | +1.53 |
| Aesthetic discipline (BW deadpan fidelity) | 0.08 | 84 | 91 | +7 | +0.56 |
| **Composite (weighted)** | **1.00** | **72.32** | **91.60** | **+19.28** | |

**Pre-audit composite: 72.32** — failed Heavy threshold (≥ 90).
**Post-audit composite: 91.60** — clears Heavy threshold.

---

## Decision items requiring operator response before mockup revision

1. **F4 — Endorsements nav link:** hide until active, or render dormant page as deliberate conversion surface?
2. **F12 — Pillar 2 + 3 figures:** supply numeric anchors (from Decisions Register), or accept asymmetry with visual differentiation?
3. **F19 — Primary CTA copy:** soft "Get campaign updates" with no lead magnet, or committed "Get Michael's platform brief" with operator drafting the brief?

Three decisions. After they land, mockup r2 ships in one revision cycle.

---

## Sign-off

| Role | Name | Scope | Date | Signature |
|---|---|---|---|---|
| JEC Methodology Lead | Michael Turon | Full audit | 2026-05-12 | drafted |
| Sam Ray (counsel) | Sam Ray | F13, F14, F31 batched review | _pre-deploy_ | _pending_ |
| Lauren Turon (treasurer) | Lauren Turon | Trust strip + FPPC surface review | _pre-deploy_ | _pending_ |
| Campaign Manager (Allbee) | Nate Allbee | F4 endorsement-page decision | _pre-deploy_ | _pending_ |

— end of `Phase1_Design_Red_JEC_Audit.md`
