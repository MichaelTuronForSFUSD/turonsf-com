# Cantonese Production Deploy Log - 2026-05-27

## Purpose

This log records the production release path for the Cantonese (`yue-Hant`) language pages after the normal Cloudflare Pages Git deployment failed.

## Release

- Site: `https://turonsf.com/`
- Language route: `https://turonsf.com/yue-hant/`
- Git commit: `cbc634eee586f5f16520f0224f41b74d21d7e68f`
- Commit subject: `Add Cantonese language pages`
- Cloudflare Pages project: `turonsf-com`
- Production deployment ID: `25d80176-72cf-417f-a35a-fef967f4f564`
- Production preview URL: `https://25d80176.turonsf-com.pages.dev`

## Incident Summary

GitHub push to `main` succeeded, but the Cloudflare Pages Git-connected production deployment for commit `cbc634e` failed:

- Failed Git deployment ID: `9b16fe13-7d8e-4a45-8e7e-832ef7432848`
- Failed deployment URL: `https://9b16fe13.turonsf-com.pages.dev`
- Cloudflare build page: `https://dash.cloudflare.com/67085892385248117e242d8307f8e5b5/pages/view/turonsf-com/9b16fe13-7d8e-4a45-8e7e-832ef7432848`

To avoid holding the language release, production was deployed by direct Wrangler upload from the locally verified Hugo build artifact.

## Commands Used

Tool resolution:

```bash
type -a wrangler
type -a npx
type -a hugo
```

Wrangler was not installed globally, so `npx wrangler` was used.

Authentication and project checks:

```bash
npx --yes wrangler@latest whoami
npx --yes wrangler@latest pages project list
npx --yes wrangler@latest pages deployment list --project-name turonsf-com
```

Local production build:

```bash
hugo --minify --logLevel warn
```

Direct production upload:

```bash
npx --yes wrangler@latest pages deploy public --project-name turonsf-com --branch main --commit-hash cbc634eee586f5f16520f0224f41b74d21d7e68f --commit-message "Add Cantonese language pages" --commit-dirty=false
```

## Verification Evidence

Local build passed with Hugo `0.160.1` and rendered all configured languages:

- `EN`
- `ES`
- `YUE-HANT`
- `ZH-HANT`
- `ZH-HANS`
- `TL`
- `VI`
- `AR`

Wrangler upload result:

```text
Success! Uploaded 148 files
Deployment complete! Take a peek over at https://25d80176.turonsf-com.pages.dev
```

Live custom-domain checks passed:

```bash
curl -fsSL https://turonsf.com/yue-hant/ | rg "html lang=yue-Hant|html lang=\"yue-Hant|廣東話|三個問題"
curl -fsSL https://turonsf.com/ | rg "lang-eyebrow|yue-hant|zh-hant|廣東話|html lang"
```

Observed live evidence:

- `https://turonsf.com/yue-hant/` returns `html lang=yue-Hant`.
- `https://turonsf.com/yue-hant/` contains `廣東話`.
- `https://turonsf.com/yue-hant/` contains the Cantonese hero headline `三個問題。按次序解決。`
- `https://turonsf.com/` includes the Cantonese language switcher link `/yue-hant/`.

## Follow-up

The Git-connected Cloudflare Pages build path still needs investigation. The most likely first check is whether Cloudflare production is pinned to an older Hugo version than the locally verified `0.160.1`.

Recommended Cloudflare Pages settings to review:

- Build command: `hugo --minify`
- Output directory: `public`
- Production branch: `main`
- Hugo version: align with local verified version `0.160.1`, unless the build log identifies a different blocker.
