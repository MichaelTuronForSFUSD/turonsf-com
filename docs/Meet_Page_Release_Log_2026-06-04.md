# /meet Page Release Log — 2026-06-04

## Scope

Added a multilingual `/meet/` booking page for Michael Turon for SFUSD Board of Education.

Source references:

- `/Users/turonbot/Projects/www_turonSF_phase1/Meet Michael/Turon_meet_copy_8_languages_v1.0.md`
- `/Users/turonbot/Projects/www_turonSF_phase1/Meet Michael/meet_qr.png`
- `/Users/turonbot/Projects/www_turonSF_phase1/Meet Michael/meet_qr.svg`

## Booking Link

Primary Google Appointment Scheduling URL:

`https://calendar.app.google/kuDZVx7TyBLKx3B87`

This URL is now the site-level `calendar_url` in `hugo.toml` and is used by all `/meet/` language variants.

## New Routes

- `https://turonsf.com/meet/`
- `https://turonsf.com/es/meet/`
- `https://turonsf.com/yue-hant/meet/`
- `https://turonsf.com/zh-hant/meet/`
- `https://turonsf.com/zh-hans/meet/`
- `https://turonsf.com/tl/meet/`
- `https://turonsf.com/vi/meet/`
- `https://turonsf.com/ar/meet/`

## Implementation Notes

- Added `content/meet*.md` in all eight active site languages.
- Added a dedicated Hugo layout at `themes/turon-civic/layouts/_default/meet.html`.
- Added QR assets to `static/img/meet/`.
- Added `Meet` navigation entry after `About` across all language menus.
- Added `meet_booking_click` analytics markers for primary, secondary, and QR booking paths.
- Added `/meet/` rows to `data/translation_status.yaml`; non-English rows are marked `live` for sitemap and hreflang inclusion.
- Updated `llms.*.txt` language guidance with `/meet/` URLs.
- Updated verification row-count guards from 91 to 98 translated rows.

## Manual Review Notes

The copy follows `Turon_meet_copy_8_languages_v1.0.md`. Native-speaker review is still recommended before paid distribution, especially for Cantonese and Arabic public-facing materials.

## Operator Verification Commands

```bash
cd "$HOME/www/turonsf_com" || exit 1
type -a git
type -a hugo
type -a npx
type -a curl
hugo --minify --logLevel warn
bin/check-i18n-parity.sh
bin/check-translation-status.sh
bin/preflight-check.sh
./02_verify_turonsf_build.sh
bin/check-no-jd-references.sh
bin/check-utm-hygiene.sh
bin/check-fppc-footer.sh
```

## Verification Evidence

Local verification passed on 2026-06-04:

- `hugo --minify --logLevel warn` completed without warnings.
- `bin/check-i18n-parity.sh` passed with 8 language files and 67 shared keys.
- `bin/check-translation-status.sh` passed with 98 entries and all scaffolds present.
- `bin/preflight-check.sh` passed.
- `./02_verify_turonsf_build.sh` passed and confirmed all `/meet/` rendered pages.
- `bin/check-no-jd-references.sh` passed.
- `bin/check-utm-hygiene.sh` passed with 41 outbound campaign URLs carrying required UTMs.
- `bin/check-fppc-footer.sh` passed with 117 rendered pages carrying FPPC ID 1482971.
- Each `/meet/` page renders three `meet_booking_click` booking paths, one QR image, the shared calendar URL, and exactly one `<main>` element.
- Each language sitemap includes `/meet/` and hreflang alternates.

## Deploy Attempt

Commit prepared locally:

`f9da863 Add multilingual meet booking page`

Wrangler deploy was attempted from the committed tree on 2026-06-04, but the local Cloudflare session failed with `Authentication error [code: 10000]`. Operator action required: run `wrangler login` or provide a valid Cloudflare API token/session before retrying the deploy command below.

## Wrangler Deploy Command

Wrangler Pages deploy syntax was checked against the Cloudflare Wrangler Pages command reference on 2026-06-04.

```bash
cd "$HOME/www/turonsf_com" || exit 1
npx --yes wrangler@latest pages deploy public \
  --project-name turonsf-com \
  --branch main \
  --commit-hash "$(git rev-parse HEAD)" \
  --commit-message "$(git log -1 --pretty=%s)" \
  --commit-dirty=false
```
