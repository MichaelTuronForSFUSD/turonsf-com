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

## Before pushing v3 to `main`

Cloudflare Pages deploys on push to `main`. Work through "Still required before pushing" in the v3 release notes first.
