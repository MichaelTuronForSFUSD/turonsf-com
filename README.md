# turonsf.com

Hugo static site for Michael J. Turon. v3 (branch `v3-endorsement-hub`) is a single endorsement hub in eight languages; the v2 campaign site is preserved at tag `v2-campaign-site-final`. See `docs/V3_Endorsement_Hub_Release_Notes.md`.

## Local build

```bash
hugo --minify
```

## Local preview

```bash
hugo server --bind 127.0.0.1 --baseURL http://127.0.0.1:1313/
```

## Editing the hub

- Copy, all languages: `data/hub_copy.json`
- Links and candidate order: `data/hub_links.yaml`
- Translation state per language: `data/translation_status.yaml`

## Going live

A git push does **not** deploy (the Cloudflare auto-build has been broken since 2026-05-27). Deploy with `./bin/deploy.sh` (Wrangler direct upload). See `docs/V3_Go_Live_Runbook.md`: pre-flight checklist, deploy commands, post-deploy checks, and rollback.

## Checks (also run in CI)

```bash
hugo --minify
./bin/check-i18n-parity.sh && ./bin/check-no-jd-references.sh && ./bin/check-translation-status.sh
./bin/check-utm-hygiene.sh public && ./bin/check-fppc-footer.sh public && ./bin/check-redirects.sh static/_redirects public
```
