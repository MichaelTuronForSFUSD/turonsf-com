#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

fail() { printf '❌ %s\n' "$*" >&2; exit 1; }
warn() { printf '⚠️  %s\n' "$*" >&2; }
pass() { printf '✅ %s\n' "$*"; }

command -v hugo >/dev/null 2>&1 || fail "hugo is not installed or not on PATH"

printf '\n== Build ==\n'
hugo --minify --logLevel warn >/tmp/turonsf_hugo_build.log 2>&1 || { cat /tmp/turonsf_hugo_build.log >&2; fail "hugo build failed"; }
if grep -qi "WARN" /tmp/turonsf_hugo_build.log; then
  cat /tmp/turonsf_hugo_build.log >&2
  fail "hugo emitted warnings; inspect and fix before deploy"
fi
pass "hugo --minify --logLevel warn exits clean"

[[ -d public ]] || fail "public/ was not generated"
for lang in es yue-hant zh-hant zh-hans tl vi ar; do
  [[ -d "public/$lang" ]] || fail "missing public/$lang output"
done
pass "all seven non-English language output directories exist"

printf '\n== Static guards ==\n'
if grep -rEn "TODO|XXX|FIXME" public/ >/tmp/turonsf_todo_hits 2>/dev/null; then
  cat /tmp/turonsf_todo_hits >&2
  fail "TODO/XXX/FIXME marker rendered into public/"
fi
pass "no TODO/XXX/FIXME markers rendered"

if grep -rEi "juris doctor|attorney|lawyer|\bJD\b|abogad|律师|律師|محامي|luật sư" public/ >/tmp/turonsf_role_hits 2>/dev/null; then
  cat /tmp/turonsf_role_hits >&2
  fail "role/JD/attorney/lawyer forbidden term rendered"
fi
pass "forbidden role terms absent"

printf '\n== i18n key parity ==\n'
python3 - <<'PY'
from pathlib import Path
import re, sys
base = Path('themes/turon-civic/i18n')
files = sorted(base.glob('*.toml'))
if len(files) != 8:
    print(f'Expected 8 i18n TOML files; found {len(files)}', file=sys.stderr)
    sys.exit(1)
keys = {}
for p in files:
    text = p.read_text()
    keys[p.name] = re.findall(r'^\[([^\]]+)\]', text, flags=re.M)
ref_name = 'en.toml'
ref = set(keys.get(ref_name, []))
for name, got_list in keys.items():
    got = set(got_list)
    missing = sorted(ref - got)
    extra = sorted(got - ref)
    if missing or extra:
        print(f'{name}: missing={missing} extra={extra}', file=sys.stderr)
        sys.exit(1)
print(f'All {len(files)} TOML files share {len(ref)} keys')
PY
pass "i18n keys match across all languages"

printf '\n== translation_status rows ==\n'
python3 - <<'PY'
from pathlib import Path
import re, sys
text = Path('data/translation_status.yaml').read_text()
rows = re.findall(r'^\s+"/[^"]*::(?:es|yue-Hant|zh-Hant|zh-Hans|tl|vi|ar)"\s*:', text, flags=re.M)
if len(rows) != 91:
    print(f'Expected 91 translation_status rows; found {len(rows)}', file=sys.stderr)
    sys.exit(1)
print('translation_status rows:', len(rows))
PY
pass "translation_status row count valid"

printf '\n== Analytics + UTM ==\n'
[[ -f themes/turon-civic/assets/js/analytics.js ]] || fail "analytics.js missing"
[[ -f themes/turon-civic/layouts/partials/cta-link.html ]] || fail "cta-link.html missing"
[[ -f themes/turon-civic/layouts/shortcodes/cta.html ]] || fail "cta shortcode missing"
pass "analytics shim and CTA renderer files exist"

# Campaign backend links must carry UTM parameters after templates are converted.
# This check is non-fatal for the overlay itself, because the v1.2.0 checkout's
# templates may not yet have been converted when this script is first copied.
if grep -RhoE 'href="https://(secure\.actblue\.com|actionnetwork\.org)[^"]*"' public/ >/tmp/turonsf_campaign_links 2>/dev/null; then
  if grep -v 'utm_source=turonsf' /tmp/turonsf_campaign_links >/tmp/turonsf_missing_utm; then
    cat /tmp/turonsf_missing_utm >&2
    fail "campaign backend link missing utm_source=turonsf"
  fi
  for param in utm_medium=web utm_campaign=phase1 utm_content=; do
    if grep -v "$param" /tmp/turonsf_campaign_links >/tmp/turonsf_missing_param; then
      cat /tmp/turonsf_missing_param >&2
      fail "campaign backend link missing $param"
    fi
  done
  pass "campaign backend links carry required UTMs"
else
  warn "no rendered ActBlue/Action Network/Brevo backend links found; confirm templates were converted or links are intentionally absent"
fi

if grep -R "analytics" public/*.html public/*/*.html >/dev/null 2>&1; then
  pass "analytics asset appears in rendered HTML"
else
  warn "analytics asset not found in rendered HTML; include partial \"analytics-script.html\" before launch"
fi

printf '\n== SEO live posture ==\n'
for lang in es yue-hant zh-hant zh-hans tl vi ar; do
  if [[ -f "public/$lang/index.html" ]]; then
    if grep -q 'name="robots" content="noindex, follow"' "public/$lang/index.html"; then
      fail "unexpected noindex,follow on live $lang home"
    fi
  fi
done
pass "language homes are indexable live pages"

printf '\nPreflight static checks completed. Manual review items remain in docs/Phase1_Preflight_Checklist.md.\n'
