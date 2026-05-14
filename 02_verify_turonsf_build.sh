#!/usr/bin/env bash
set -Eeuo pipefail

SITE_DIR="${TURONSF_SITE_DIR:-$HOME/www/turonsf_com}"

say() { printf '\n== %s ==\n' "$*"; }
fail() { printf 'FAIL: %s\n' "$*" >&2; exit 1; }
warn() { printf 'WARN: %s\n' "$*" >&2; }
pass() { printf 'OK: %s\n' "$*"; }

case "$SITE_DIR" in
  "$HOME"/www/turonsf_com|/www/turonsf_com) ;;
  *) fail "Refusing target outside ~/www/turonsf_com or /www/turonsf_com. Got: $SITE_DIR" ;;
esac

[ -d "$SITE_DIR" ] || fail "$SITE_DIR does not exist"
cd "$SITE_DIR"

case "$(pwd)" in
  "$HOME"/www/turonsf_com|/www/turonsf_com) ;;
  *) fail "Wrong working directory: $(pwd)" ;;
esac

if [ -f ./TURONSF_PATH_GUARD.sh ]; then
  ./TURONSF_PATH_GUARD.sh
else
  warn "TURONSF_PATH_GUARD.sh not found"
fi

say "Wrong-site / credential guard"
if pwd | grep -Eiq 'CAREInstitute|careinstitute'; then
  fail "Current path contains CAREInstitute/careinstitute"
fi

if git remote -v 2>/dev/null | grep -Ei 'CAREInstitute|careinstitute|ghp_|github_pat_|CLOUDFLARE_API_TOKEN|OPENAI_API_KEY'; then
  fail "git remote or credential-like string found; remove before continuing"
else
  pass "no CAREInstitute or token-like string in git remotes"
fi

if grep -RInE 'ghp_|github_pat_|CLOUDFLARE_API_TOKEN|OPENAI_API_KEY|CAREInstitute|careinstitute' . \
  --exclude-dir=.git \
  --exclude-dir=docs \
  --exclude-dir=public \
  --exclude-dir=resources \
  --exclude='CODEX_TURONSF_BUILD_TASK.md' \
  --exclude='TURONSF_PATH_GUARD.sh' \
  --exclude='README_LOCAL_TURONSF.md' \
  --exclude='02_verify_turonsf_build.sh' \
  --exclude='README_RUN_ORDER.md' 2>/dev/null; then
  fail "wrong-site or credential-like string found in repo"
else
  pass "no obvious wrong-site strings or secrets in repo files"
fi

say "Tooling"
command -v hugo >/dev/null 2>&1 || fail "hugo is not installed or not on PATH"
hugo version
command -v python3 >/dev/null 2>&1 || fail "python3 is required for parity checks"

say "Required source files"
required=(
  "hugo.toml"
  "themes/turon-civic/theme.toml"
  "themes/turon-civic/assets/js/analytics.js"
  "themes/turon-civic/layouts/partials/analytics-script.html"
  "themes/turon-civic/layouts/partials/cta-link.html"
  "themes/turon-civic/layouts/partials/head-preconnects.html"
  "themes/turon-civic/layouts/partials/head-hreflang.html"
  "themes/turon-civic/layouts/partials/language-switcher.html"
  "themes/turon-civic/layouts/partials/ai-translation-disclosure.html"
  "themes/turon-civic/layouts/_default/baseof.html"
  "themes/turon-civic/layouts/index.html"
  "data/translation_status.yaml"
  "content/_index.md"
  "content/about.md"
  "content/platform/_index.md"
  "content/platform/pillar-1.md"
  "content/platform/pillar-2.md"
  "content/platform/pillar-3.md"
)
for f in "${required[@]}"; do
  [ -f "$f" ] || fail "missing required file: $f"
  echo "OK: $f"
done

say "Build"
rm -rf public resources
if hugo --minify --logLevel warn > /tmp/turonsf_hugo_verify.log 2>&1; then
  cat /tmp/turonsf_hugo_verify.log
  pass "hugo --minify completed"
else
  cat /tmp/turonsf_hugo_verify.log >&2
  fail "hugo build failed"
fi

if grep -qi '^WARN\|WARN ' /tmp/turonsf_hugo_verify.log; then
  cat /tmp/turonsf_hugo_verify.log >&2
  fail "hugo emitted warnings"
fi

say "Rendered pages"
pages=(
  "public/index.html"
  "public/about/index.html"
  "public/platform/index.html"
  "public/platform/pillar-1/index.html"
  "public/platform/pillar-2/index.html"
  "public/platform/pillar-3/index.html"
  "public/endorsements/index.html"
  "public/volunteer/index.html"
  "public/donate/index.html"
  "public/contact/index.html"
  "public/es/index.html"
  "public/zh-hant/index.html"
  "public/zh-hans/index.html"
  "public/tl/index.html"
  "public/vi/index.html"
  "public/ar/index.html"
)
for p in "${pages[@]}"; do
  [ -f "$p" ] || fail "missing rendered page: $p"
  echo "OK: $p"
done

say "Language output directories"
for lang in es zh-hant zh-hans tl vi ar; do
  [ -d "public/$lang" ] || fail "missing public/$lang output"
  echo "OK: public/$lang"
done

say "Analytics / event markers"
events=(
  newsletter_cta_click
  newsletter_signup_submit
  donate_cta_click
  volunteer_cta_click
  email_contact_click
  pillar_click
  platform_link_click
  hero_cta_primary_view
  trust_strip_view
  scroll_depth_75
  scroll_depth_100
  language_switcher_open
  language_switcher_select
  language_pending_notice_view
  language_pending_to_english_click
  nav_click
)
for event in "${events[@]}"; do
  if grep -R "$event" themes layouts content public hugo.toml 2>/dev/null >/dev/null; then
    echo "OK: $event"
  else
    fail "missing event marker: $event"
  fi
done

say "Outbound campaign UTM checks"
CAMPAIGN_LINKS="/tmp/turonsf_campaign_links.$$"
grep -RhoE 'href="https://(secure\.actblue\.com|actionnetwork\.org)[^"]*"' public/ 2>/dev/null | sort | uniq > "$CAMPAIGN_LINKS" || true
if [ -s "$CAMPAIGN_LINKS" ]; then
  cat "$CAMPAIGN_LINKS"
  for param in 'utm_source=turonsf' 'utm_medium=web' 'utm_campaign=phase1' 'utm_content='; do
    if grep -v "$param" "$CAMPAIGN_LINKS" >/tmp/turonsf_missing_param.$$; then
      cat /tmp/turonsf_missing_param.$$ >&2
      fail "campaign backend link missing $param"
    fi
  done
  pass "campaign backend links carry all required UTM parameters"
else
  fail "no rendered ActBlue or Action Network links found"
fi
rm -f "$CAMPAIGN_LINKS" /tmp/turonsf_missing_param.$$ 2>/dev/null || true

say "Preconnect checks"
for host in secure.actblue.com actionnetwork.org sibforms.com; do
  grep -E "rel=\"?preconnect\"? href=\"?https://$host\"?" public/index.html >/dev/null || fail "missing preconnect for $host"
  echo "OK: preconnect $host"
done

say "Placeholder SEO checks"
for lang in es zh-hant zh-hans tl vi ar; do
  grep -Eq 'name="?robots"? content="?noindex, follow"?' "public/$lang/index.html" || fail "missing noindex,follow on $lang home"
  echo "OK: noindex placeholder $lang"
done

say "i18n parity"
python3 - <<'PY_I18N'
from pathlib import Path
import re, sys
base = Path('themes/turon-civic/i18n')
files = sorted(base.glob('*.toml'))
if len(files) != 7:
    print(f'Expected 7 i18n TOML files; found {len(files)}', file=sys.stderr)
    sys.exit(1)
keys = {}
for p in files:
    text = p.read_text(encoding='utf-8')
    keys[p.name] = set(re.findall(r'^\[([^\]]+)\]', text, flags=re.M))
ref = keys.get('en.toml', set())
for name, got in keys.items():
    missing = sorted(ref - got)
    extra = sorted(got - ref)
    if missing or extra:
        print(f'{name}: missing={missing} extra={extra}', file=sys.stderr)
        sys.exit(1)
print(f'All {len(files)} TOML files share {len(ref)} keys')
PY_I18N
pass "i18n key parity passed"

say "translation_status row count"
python3 - <<'PY_STATUS'
from pathlib import Path
import re, sys
text = Path('data/translation_status.yaml').read_text(encoding='utf-8')
rows = re.findall(r'^\s+"/[^\"]*::(?:es|zh-Hant|zh-Hans|tl|vi|ar)"\s*:', text, flags=re.M)
if len(rows) != 78:
    print(f'Expected 78 translation_status rows; found {len(rows)}', file=sys.stderr)
    sys.exit(1)
print('translation_status rows:', len(rows))
PY_STATUS
pass "translation_status row count passed"

say "Launch blockers that may remain intentionally"
if grep -RIn 'MUIFAA_REPLACE_BEFORE_LIVE\|MUIFAA\.\.\.' hugo.toml themes content 2>/dev/null; then
  warn "Brevo placeholder still present. Replace before production."
else
  pass "no Brevo placeholder found"
fi

if grep -n 'umami_website_id = ""' hugo.toml >/dev/null; then
  warn "Umami website ID is blank. Fill before production analytics validation."
else
  pass "Umami website ID appears populated"
fi

say "Git status"
git status --short --branch || true

say "Verification complete"
echo "Build is locally checkable. Remaining manual blockers: Spanish backend routing, Sam review, Lauren review."
