#!/usr/bin/env python3
"""
v1.3.5 patch — JEC-optimized disclosure language + Option A slim bar
4 change groups:
  1. 7 i18n TOML files — new ai_translation_disclosure_body + _link_text
  2. baseof.html — move partial call: inside <main> → between eyebrow and <header>
  3. ai-translation-disclosure.html — rewrite box → slim bar (.disclosure-slim)
  4. site.css — add .disclosure-slim rules

Run from: /Users/turonbot/www/turonsf_com
  python3 v135_patch.py
"""
import re, sys, shutil
from pathlib import Path

BASE  = Path("/Users/turonbot/www/turonsf_com")
THEME = BASE / "themes/turon-civic"

# ── helpers ───────────────────────────────────────────────────────────────────

def patch(path: Path, old: str, new: str, desc: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count == 0:
        print(f"  MISS  {desc}\n        not found in {path.relative_to(BASE)}")
        sys.exit(1)
    if count > 1:
        print(f"  AMBIG {desc}\n        {count} matches — tighten pattern")
        sys.exit(1)
    path.write_text(text.replace(old, new), encoding="utf-8")
    print(f"  OK    {desc}")


def patch_toml(path: Path, body: str, link: str) -> None:
    """Replace both disclosure TOML values in one file."""
    text = path.read_text(encoding="utf-8")
    for key, val in [
        ("ai_translation_disclosure_body",      body),
        ("ai_translation_disclosure_link_text", link),
    ]:
        pattern     = r'\[' + re.escape(key) + r'\]\nother = "[^"]*"'
        replacement = f'[{key}]\nother = "{val}"'
        text, n = re.subn(pattern, replacement, text)
        if n == 0:
            print(f"  MISS  {path.name}: [{key}] not found")
            sys.exit(1)
        if n > 1:
            print(f"  AMBIG {path.name}: [{key}] matched {n} times")
            sys.exit(1)
    path.write_text(text, encoding="utf-8")
    print(f"  OK    {path.name}")


# ── 1. i18n TOMLs — JEC-converged disclosure strings ─────────────────────────
# Panel scores by language:
#   ES 9.5 · 繁體 9.5 · 简体 9.5 · TL 9.33 · VI 9.5 · AR 9.5
# Five design rules locked:
#   (1) Purpose leads — WHY before HOW
#   (2) AI as tool ("with AI's help"), not author ("AI translated")
#   (3) Family frame — authentic for SFUSD parent candidate
#   (4) Collective-benefit CTA — help more families, not report errors
#   (5) Zero error priming — feedback/opinion/share, never error/mistake

print("\n1. Patching i18n TOMLs (7 files)")

TOML_STRINGS = {
    # EN — parity only; disclosure never renders on English pages.
    # Values document intent in English for audit trail.
    "en": (
        "This page was translated by AI so your family can read it in their language.",
        "Help us improve it for more families.",
    ),
    # ES — 9.5 · Cycle 4 convergence
    # "Queremos" (we want) = sincere personal voice
    # "como otras familias" = collective belonging without rights-pamphlet register
    # "con ayuda de IA" = AI as tool, not author
    # "¿nos ayudas a mejorarlo?" = intimate community ask, "lo" ties to translation
    "es": (
        "Queremos que tu familia pueda leer esto en español, como otras familias."
        " Lo hicimos con ayuda de IA.",
        "¿Nos ayudas a mejorarlo?",
    ),
    # 繁體 — 9.5 · Cycle 4 convergence
    # "借助AI進行了翻譯" = borrowed AI's help (tool frame)
    # "·" mid-dot pause = processing aid for older readers (Mr. Wong 9.0→9.5)
    # "寶貴意見" = Cantonese honorific for "valuable opinion" — signals deep respect
    # "讓更多家庭受益" = benefit more families (collective good)
    "zh-Hant": (
        "為讓您的家人能用中文閱讀 · 我們借助AI進行了翻譯。",
        "您的寶貴意見能讓更多家庭受益",
    ),
    # 简体 — 9.5 · Cycle 4 convergence
    # "真誠地借助AI" = sincerely with AI's help (Wei 9.0→9.5: signals candidate
    #   is not hiding behind technology)
    # Plain "您的意見" — "寶貴" omitted; in Mandarin reads as over-formal
    "zh-Hans": (
        "为让您的家人能用中文阅读，我们真诚地借助AI进行了翻译。",
        "您的意见能让更多家庭受益",
    ),
    # TL — 9.33 (Lorna 9.0 irreducible on AI term; Jose+Maria 9.5)
    # "Ginawa namin itong pahina" = We made this page (ownership, not disclaimer)
    # "para sa inyong pamilya" = for your family
    # "tulungan kami na mapabuti para sa lahat" = help us improve for everyone
    #   (bayanihan frame — community helping community)
    "tl": (
        "Ginawa namin itong pahina sa Filipino para sa inyong pamilya."
        " AI ang ginamit.",
        "Tulungan kami na mapabuti para sa lahat",
    ),
    # VI — 9.5 · Cycle 3 convergence (no Cycle 4 needed)
    # "muốn" (want) = the word that moved Bà Nguyễn to tears — a wish, not a notice
    # "góp ý giúp thêm nhiều gia đình" = contribute to help more families
    #   (cùng = together frame → collective benefit)
    "vi": (
        "Chúng tôi muốn gia đình bạn được đọc trang này bằng tiếng Việt."
        " AI đã dịch.",
        "Góp ý giúp thêm nhiều gia đình",
    ),
    # AR — 9.5 · Cycle 3 convergence (no Cycle 4 needed)
    # "حتى تقرأ عائلتك" = so that your family reads — purpose-first (Arabic rhetoric)
    # "استعنّا بالذكاء الاصطناعي" = we sought AI's help (tool frame)
    # "شاركنا رأيك" = share your opinion with us (imperative = warm invitation)
    # "لتستفيد عائلات أخرى" = so other families benefit (collective good)
    "ar": (
        "حتى تقرأ عائلتك هذه الصفحة بالعربية، استعنّا بالذكاء الاصطناعي للترجمة.",
        "شاركنا رأيك لتستفيد عائلات أخرى",
    ),
}

i18n_dir = THEME / "i18n"
toml_files = sorted(i18n_dir.glob("*.toml"))
if len(toml_files) != 7:
    print(f"  WARN  expected 7 TOML files, found {len(toml_files)}")

for toml_path in toml_files:
    # Derive lang key from filename (en.toml→en, zh-Hant.toml→zh-Hant, etc.)
    lang_key = toml_path.stem  # e.g. "zh-Hant"
    if lang_key not in TOML_STRINGS:
        print(f"  SKIP  {toml_path.name} — no string entry defined")
        continue
    body, link = TOML_STRINGS[lang_key]
    patch_toml(toml_path, body, link)


# ── 2. baseof.html — relocate partial: <main> → between eyebrow and <header> ─
print("\n2. Patching baseof.html — relocate ai-translation-disclosure partial")

baseof = THEME / "layouts/_default/baseof.html"

# Step 2a: remove from inside <main>
patch(
    baseof,
    '\n    {{ partial "ai-translation-disclosure.html" . }}\n    {{ block "main" . }}{{ end }}',
    '\n    {{ block "main" . }}{{ end }}',
    "remove partial from inside <main>",
)

# Step 2b: insert between eyebrow </nav> and <header class="site-header">
patch(
    baseof,
    '  <header class="site-header">{{ partial "site-nav.html" . }}</header>',
    '  {{ partial "ai-translation-disclosure.html" . }}\n  <header class="site-header">{{ partial "site-nav.html" . }}</header>',
    "insert partial between eyebrow and site-header",
)


# ── 3. ai-translation-disclosure.html — rewrite box → slim bar ───────────────
print("\n3. Rewriting ai-translation-disclosure.html")

partial_path = THEME / "layouts/partials/ai-translation-disclosure.html"

# Back up current version for audit trail
bak_path = partial_path.with_suffix(".html.v134.bak")
shutil.copy2(partial_path, bak_path)
print(f"  BAK   {bak_path.relative_to(BASE)}")

NEW_PARTIAL = """\
{{/*
  ai-translation-disclosure.html
  Option A slim bar — single persistent line between eyebrow and site-nav.
  JEC 6-language panel convergence v1.3.5 — 2026-05-14.

  Design rules (5 locked):
    1. Purpose leads — WHY before HOW
    2. AI as tool ("with AI's help"), not author ("AI translated")
    3. Family frame — authentic for SFUSD parent candidate
    4. Collective-benefit CTA — help more families, not report errors
    5. Zero error priming — feedback/share/opinion, never error/mistake

  Renders on non-EN pages where translation_status is "live" or "ai_translated".
  Translation status lookup: data/translation_status.yaml
  Key format: "/canonical/path/::lang" (uses canonical_path frontmatter if set)
*/}}
{{ $statusPath := .RelPermalink }}
{{ with .Params.canonical_path }}{{ $statusPath = . }}{{ end }}
{{ $lang := .Site.Language.Lang }}
{{ $key := printf "%s::%s" $statusPath $lang }}
{{ $status := index .Site.Data.translation_status $key }}
{{ if and (ne $lang "en") (or (eq $status "live") (eq $status "ai_translated")) }}
<div class="disclosure-slim" role="note">
  <span class="disclosure-slim__icon" aria-hidden="true">🌐</span>
  <span class="disclosure-slim__body">{{ i18n "ai_translation_disclosure_body" }}</span>
  <span class="disclosure-slim__sep" aria-hidden="true">·</span>
  <a class="disclosure-slim__link" href="mailto:{{ i18n "contact_email" }}">{{ i18n "ai_translation_disclosure_link_text" }}</a>
</div>
{{ end }}
"""

partial_path.write_text(NEW_PARTIAL, encoding="utf-8")
print(f"  OK    ai-translation-disclosure.html (old saved as .v134.bak)")


# ── 4. site.css — add .disclosure-slim rules ──────────────────────────────────
# Appended after .lang-eyebrow__sep rule (last eyebrow rule from v1.3.4).
# .translation-notice is intentionally kept — cached page safety.
print("\n4. Patching site.css — add .disclosure-slim block")

OLD_EYEBROW_SEP = (
    ".lang-eyebrow__sep { color: rgba(255,255,255,0.25); "
    "font-size: 0.65rem; padding: 0 0.15rem; }"
)

NEW_EYEBROW_SEP = (
    ".lang-eyebrow__sep { color: rgba(255,255,255,0.25); "
    "font-size: 0.65rem; padding: 0 0.15rem; }\n"
    # Option A — slim tint bar — JEC 6-language panel convergence v1.3.5
    ".disclosure-slim { background: rgba(7,26,47,0.055); "
    "border-bottom: 1px solid rgba(7,26,47,0.10); "
    "padding: 0.4rem 1rem; font-size: 0.78rem; color: var(--navy-700); "
    "display: flex; align-items: center; justify-content: center; "
    "gap: 0.4rem; line-height: 1.3; flex-wrap: wrap; }\n"
    ".disclosure-slim__icon { opacity: 0.45; font-size: 0.72rem; flex-shrink: 0; }\n"
    ".disclosure-slim__body { text-align: center; }\n"
    ".disclosure-slim__sep { color: var(--muted); opacity: 0.5; }\n"
    ".disclosure-slim__link { color: var(--accent); text-decoration: none; "
    "font-weight: 600; white-space: nowrap; }\n"
    ".disclosure-slim__link:hover { text-decoration: underline; }"
)

patch(
    THEME / "static/css/site.css",
    OLD_EYEBROW_SEP,
    NEW_EYEBROW_SEP,
    ".lang-eyebrow__sep → .lang-eyebrow__sep + .disclosure-slim block",
)


# ── done ──────────────────────────────────────────────────────────────────────
print("""
All patches applied. Run CI gates:

  hugo --minify --logLevel warn 2>/dev/null && echo "build OK"
  ./bin/check-i18n-parity.sh
  ./bin/check-fppc-footer.sh public/
  ./bin/check-utm-hygiene.sh public/
  ./bin/check-no-jd-references.sh
  ./bin/check-translation-status.sh

If all pass — build and deploy:

  hugo --minify --logLevel warn 2>/dev/null
  npx wrangler pages deploy public/ --project-name turonsf-com

Then commit and tag:

  git add -A
  git commit -m "feat(disclosure): slim bar Option A + JEC 6-language panel strings (v1.3.5)"
  git push origin main
  git tag v1.3.5
  git push origin v1.3.5

Sam Ray note: confirm 'help us improve' CTA without 'official English version'
clause satisfies your interpretation of clear-and-conspicuous for AI disclosure.
Old partial backed up at:
  themes/turon-civic/layouts/partials/ai-translation-disclosure.html.v134.bak
""")
