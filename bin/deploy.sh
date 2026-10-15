#!/usr/bin/env bash
# =============================================================================
# deploy.sh — build, check, and deploy turonsf.com to Cloudflare Pages
#
# The GitHub -> Pages auto-deploy for this project has failed since 2026-05-27
# (see docs/Cantonese_Production_Deploy_Log_2026-05-27.md), so a git push
# updates GitHub but not the site. This is the working path: build Hugo
# locally, run every CI check, and upload the build directly with Wrangler.
#
#   Project : turonsf-com   (Cloudflare Pages, production branch "main")
#   Login   : the Cloudflare account that owns turonsf-com
#             (wrangler logout && wrangler login)
#
# Usage:  ./bin/deploy.sh
# =============================================================================
set -euo pipefail

PROJECT="turonsf-com"
BRANCH="main"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$ROOT/public"   # gitignored

cd "$ROOT"

say() { printf '\033[36m▸\033[0m %s\n' "$*"; }
ok()  { printf '\033[32m✓\033[0m %s\n' "$*"; }
die() { printf '\033[31m✗\033[0m %s\n' "$*" >&2; exit 1; }

# ---- preconditions ----------------------------------------------------------
command -v hugo >/dev/null     || die "hugo not found (need extended 0.160.1): brew install hugo"
command -v wrangler >/dev/null || die "wrangler not found: brew install cloudflare-wrangler"

[[ "$(git rev-parse --abbrev-ref HEAD)" == "$BRANCH" ]] || die "Check out $BRANCH first."
[[ -z "$(git status --porcelain --untracked-files=no)" ]] || die "Uncommitted changes. Commit them so the deploy matches a commit."

if ! wrangler pages project list 2>/dev/null | grep -q " $PROJECT "; then
  die "This Wrangler login can't see the $PROJECT Pages project.
     Run:  wrangler logout && wrangler login   (sign in to the Cloudflare account that owns turonsf.com)"
fi
ok "Wrangler can see $PROJECT"

# ---- build + checks ---------------------------------------------------------
say "Building Hugo site (minify + gc)..."
rm -rf "$OUT"
hugo --minify --gc --logLevel warn --destination "$OUT"
[[ -f "$OUT/_headers" && -f "$OUT/_redirects" && -f "$OUT/404.html" ]] || die "_headers, _redirects, or 404.html missing from build"

say "Running checks..."
./bin/check-i18n-parity.sh
./bin/check-no-jd-references.sh
./bin/check-translation-status.sh
./bin/check-utm-hygiene.sh "$OUT"
./bin/check-fppc-footer.sh "$OUT"
./bin/check-redirects.sh static/_redirects "$OUT"
ok "Built $(find "$OUT" -type f | wc -l | tr -d ' ') files; all checks pass"

# ---- deploy -----------------------------------------------------------------
say "Deploying to Cloudflare Pages ($PROJECT, branch=$BRANCH)..."
wrangler pages deploy "$OUT" \
  --project-name="$PROJECT" \
  --branch="$BRANCH" \
  --commit-hash="$(git rev-parse HEAD)" \
  --commit-message="$(git log -1 --pretty=%s)" \
  --commit-dirty=false

# ---- verify -----------------------------------------------------------------
say "Verifying https://turonsf.com ..."
sleep 5
FAIL=0
check() { # expected-code path
  local got; got="$(curl -s -o /dev/null -w '%{http_code}' "https://turonsf.com$2?cb=$(date +%s)")"
  if [[ "$got" == "$1" ]]; then ok "$got $2"; else printf '\033[31m✗\033[0m got %s, want %s: %s\n' "$got" "$1" "$2"; FAIL=1; fi
}
for p in / /es/ /yue-hant/ /zh-hant/ /zh-hans/ /tl/ /vi/ /ar/ /llms.txt /sitemap.xml /en/sitemap.xml /favicon.ico; do check 200 "$p"; done
for p in /donate/ /platform/pillar-1/ /es/volunteer/ /llms.en.txt; do check 301 "$p"; done
check 404 /no-such-page/
curl -sI https://turonsf.com/ | grep -qi "gateway.umami.is" && ok "CSP allows gateway.umami.is" || { echo "✗ CSP missing gateway.umami.is"; FAIL=1; }
printf '  live title: '; curl -s "https://turonsf.com/?cb=$(date +%s)" | grep -o '<title>[^<]*' | sed 's/<title>//'

[[ $FAIL -eq 0 ]] || die "Post-deploy checks failed. Roll back in the Cloudflare dashboard if needed (Pages → $PROJECT → Deployments)."
ok "Deployed and verified. https://turonsf.com/"
