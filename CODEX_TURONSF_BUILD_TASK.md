# Codex task — turonsf.com Hugo launch repo

You are working only in the current directory:

```text
/Users/turonbot/www/turonsf_com
```

Hard rule: do not inspect, read, copy, edit, or touch:

```text
/Users/turonbot/www/CAREInstitute_ai
/Users/turonbot/www/CAREInstitute_ai/site
```

These are separate sites with separate credentials.

Before writing anything, run:

```bash
pwd
./TURONSF_PATH_GUARD.sh
find . -maxdepth 2 -print | sort
```

## Source overlay

Use this Phase 1 overlay source:

```text
/Users/turonbot/Experiments/www_turonsf_com/turonsf_v1.3.1_phase1_overlay
```

If it is a ZIP, unzip it into a temporary folder and use the contained `turonsf_v1.3.1_phase1_overlay/` directory.

## Goal

Create and validate a static Hugo repo for `turonsf.com`.

Do not add a CMS, database, Next.js, Astro, React app shell, server-side rendering, or Cloudflare Workers. The architecture is Hugo + Cloudflare Pages static.

## Required build behavior

1. Initialize git if needed.
2. Copy overlay files into this repo.
3. Create a real `hugo.toml` from the overlay diff and launch requirements.
4. Keep theme `turon-civic`.
5. Keep languages: en, es, zh-Hant, zh-Hans, tl, vi, ar.
6. English must render at root URLs, not `/en/`.
7. Non-English pages must render under language prefixes.
8. `[params.cta_destinations]` must exist.
9. Brevo and Umami placeholders remain blockers unless live values are supplied by the operator.
10. Do not create or set git remotes.
11. Do not store secrets, tokens, or credentials.

## Analytics requirements

Every campaign CTA should use `cta-link.html` or the `cta` shortcode.
Outbound campaign CTAs must include:

- `utm_source=turonsf`
- `utm_medium=web`
- `utm_campaign=phase1`
- `utm_content={source}-{lang}`

The repo must carry event wiring for:

- `newsletter_cta_click`
- `newsletter_signup_submit`
- `donate_cta_click`
- `volunteer_cta_click`
- `email_contact_click`
- `pillar_click`
- `platform_link_click`
- `hero_cta_primary_view`
- `trust_strip_view`
- `scroll_depth_75`
- `scroll_depth_100`
- `language_switcher_open`
- `language_switcher_select`
- `language_pending_notice_view`
- `language_pending_to_english_click`
- `nav_click`

## Design / audit requirements

- Hero identity appears before the abstract headline.
- Hero primary CTA is newsletter.
- Hero donate is a subordinate text-level CTA.
- Nav donate is subordinate.
- Trust strip says `Two kids`.
- Add preconnects for ActBlue, Action Network, and Brevo.
- Add language pending notice and English fallback.
- Use system mono stack, not JetBrains Mono.
- Do not add third-party font payloads unless explicitly reviewed.

## Validation

Run:

```bash
./02_verify_turonsf_build.sh
```

Fix all Hugo build failures and script failures. Leave live-launch placeholders flagged; do not invent live Brevo, Umami, ActBlue, or Action Network values.
