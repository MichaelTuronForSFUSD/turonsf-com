#!/usr/bin/env python3
"""
v1.3.4 patch — eyebrow language switcher
Run from: /Users/turonbot/www/turonsf_com
  python3 v134_patch.py
"""
import re, sys
from pathlib import Path

BASE  = Path("/Users/turonbot/www/turonsf_com")
THEME = BASE / "themes/turon-civic"

# ── helpers ──────────────────────────────────────────────────────────────────

def patch(path: Path, old: str, new: str, desc: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count == 0:
        print(f"  MISS  {desc}\n        pattern not found in {path.relative_to(BASE)}")
        sys.exit(1)
    if count > 1:
        print(f"  AMBIG {desc}\n        {count} matches in {path.relative_to(BASE)}")
        sys.exit(1)
    path.write_text(text.replace(old, new), encoding="utf-8")
    print(f"  OK    {desc}")


# ── 1. baseof.html ────────────────────────────────────────────────────────────
print("\n1. baseof.html — utility-bar → lang-eyebrow nav")

OLD_UTILITY = (
    '  <div class="utility-bar">'
    '{{ i18n "utility_election_label" }}: '
    '{{ i18n "election_date_display" }} — '
    'FPPC ID {{ .Site.Params.fppc_id }}</div>'
)

# Hugo template — double-quotes inside triple-quoted Python string are fine.
# $.AllTranslations uses $ (page root) so it works inside range .Site.Languages.
# {{ if $i }} is falsy for 0, truthy for 1..6 → separator between items only.
NEW_EYEBROW = """\
  <nav class="lang-eyebrow" aria-label="{{ i18n "language_switcher_label" }}">
    <div class="lang-eyebrow__inner">
      {{ $currentLang := .Site.Language.Lang }}
      {{ $labels := dict "en" "EN" "es" "Español" "zh-Hant" "繁體" "zh-Hans" "简体" "tl" "Fil" "vi" "Việt" "ar" "عربي" }}
      {{ range $i, $lang := .Site.Languages }}
        {{ if $i }}<span class="lang-eyebrow__sep" aria-hidden="true">|</span>{{ end }}
        {{ $href := printf "/%s/" $lang.Lang }}
        {{ range $.AllTranslations }}{{ if eq .Lang $lang.Lang }}{{ $href = .RelPermalink }}{{ end }}{{ end }}
        {{ $isActive := eq $lang.Lang $currentLang }}
        {{ $label := index $labels $lang.Lang | default $lang.Lang }}
        <a href="{{ $href }}" class="lang-eyebrow__link{{ if $isActive }} lang-eyebrow__link--active{{ end }}"{{ if $isActive }} aria-current="true"{{ end }} hreflang="{{ $lang.Lang }}">{{ if eq $lang.Lang "ar" }}<bdi dir="rtl">{{ $label }}</bdi>{{ else }}{{ $label }}{{ end }}</a>
      {{ end }}
    </div>
  </nav>"""

patch(THEME / "layouts/_default/baseof.html", OLD_UTILITY, NEW_EYEBROW,
      "utility-bar div → lang-eyebrow nav")


# ── 2. site-nav.html ──────────────────────────────────────────────────────────
print("\n2. site-nav.html — remove language-switcher partial include")

# Prefix newline so we don't leave a trailing blank line before </nav>
patch(THEME / "layouts/partials/site-nav.html",
      '\n  {{ partial "language-switcher.html" . }}',
      '',
      "drop language-switcher.html include from nav")


# ── 3. site.css ───────────────────────────────────────────────────────────────
print("\n3. site.css — swap .utility-bar rule for .lang-eyebrow block")

OLD_UTILITY_CSS = (
    ".utility-bar { background: var(--navy-900); color: var(--cream-50); "
    "font: 0.72rem var(--mono); letter-spacing: 0.04em; padding: 0.35rem 1rem; "
    "text-align: center; text-transform: uppercase; }"
)

# Design spec (Section 1.2): #0d1f3c background, locked font sizes, padding,
# overflow-x scroll fallback, scrollbar-width none.
NEW_EYEBROW_CSS = (
    ".lang-eyebrow { background: #0d1f3c; overflow-x: auto; scrollbar-width: none; }\n"
    ".lang-eyebrow::-webkit-scrollbar { display: none; }\n"
    ".lang-eyebrow__inner { display: flex; align-items: center; justify-content: center; "
    "padding: 0.45rem 0.75rem; gap: 0; white-space: nowrap; }\n"
    ".lang-eyebrow__link { font-size: 0.72rem; font-weight: 500; "
    "color: rgba(255,255,255,0.65); text-decoration: none; "
    "white-space: nowrap; padding: 0 0.4rem; }\n"
    ".lang-eyebrow__link--active { color: #ffffff; font-weight: 700; }\n"
    ".lang-eyebrow__link:hover:not(.lang-eyebrow__link--active) { color: rgba(255,255,255,0.85); }\n"
    ".lang-eyebrow__sep { color: rgba(255,255,255,0.25); font-size: 0.65rem; padding: 0 0.15rem; }"
)

patch(THEME / "static/css/site.css", OLD_UTILITY_CSS, NEW_EYEBROW_CSS,
      ".utility-bar → .lang-eyebrow rules")


# ── 4. i18n TOMLs — remove utility_election_label + election_date_display ────
print("\n4. i18n TOMLs — remove 2 deprecated keys from all 7 files")

KEYS = ["utility_election_label", "election_date_display"]
i18n_dir = THEME / "i18n"
toml_files = sorted(i18n_dir.glob("*.toml"))

if len(toml_files) != 7:
    print(f"  WARN  expected 7 TOML files, found {len(toml_files)}")

for toml_path in toml_files:
    text = toml_path.read_text(encoding="utf-8")
    original = text
    missing = []
    for key in KEYS:
        pattern = r'\[' + re.escape(key) + r'\]\nother = ".*?"\n?'
        new_text, n = re.subn(pattern, '', text)
        if n == 0:
            missing.append(key)
        else:
            text = new_text
    if text != original:
        toml_path.write_text(text, encoding="utf-8")
        status = "OK" if not missing else f"partial (missing: {missing})"
        print(f"  {status:6s}  {toml_path.name}")
    else:
        print(f"  SKIP    {toml_path.name}  (keys not found — check manually)")


# ── done ──────────────────────────────────────────────────────────────────────
print("""
All patches applied. Run CI gates:

  hugo --minify --logLevel warn 2>/dev/null && echo "build OK"
  ./bin/check-i18n-parity.sh
  ./bin/check-fppc-footer.sh public/
  ./bin/check-utm-hygiene.sh public/
  ./bin/check-no-jd-references.sh
  ./bin/check-translation-status.sh

If all pass:

  git add -A
  git commit -m "feat(eyebrow): language switcher in eyebrow bar — native labels, dropdown removed (v1.3.4)"
  git push origin main
  git tag v1.3.4
  git push origin v1.3.4
""")
