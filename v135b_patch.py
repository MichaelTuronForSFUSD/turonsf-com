#!/usr/bin/env python3
"""
v1.3.5b patch — fix ai-translation-disclosure.html data path
Two root causes from bak inspection:
  1. Data path: index (index hugo.Data "translation_status") "pages"
     NOT .Site.Data.translation_status (misses nested "pages" key → nil → no render)
  2. Lang variable: must use bcp47 chain, not bare .Site.Language.Lang
  3. Restores placeholder state + mailto subject (page title + language for triage)
Run from: /Users/turonbot/www/turonsf_com
  python3 v135b_patch.py
"""
import sys
from pathlib import Path

BASE  = Path("/Users/turonbot/www/turonsf_com")
THEME = BASE / "themes/turon-civic"

# ── Rewrite partial with correct data path ────────────────────────────────────
print("1. Rewriting ai-translation-disclosure.html (data path fix)")

PARTIAL = THEME / "layouts/partials/ai-translation-disclosure.html"

# Keep .v134.bak intact — don't overwrite it.
# Write a .v135a.bak of the broken version for audit.
bak = PARTIAL.with_suffix(".html.v135a.bak")
import shutil
shutil.copy2(PARTIAL, bak)
print(f"  BAK   {bak.relative_to(BASE)}")

NEW_PARTIAL = """\
{{/*
  ai-translation-disclosure.html
  Option A slim bar — JEC v1.3.5 — 2026-05-14
  --------------------------------------------------------------------------
  Fix v1.3.5b (2026-05-14):
    - Correct data path: index (index hugo.Data "translation_status") "pages"
      (v1.3.5 used .Site.Data.translation_status — missed the nested "pages"
      sub-key, returned nil, condition never fired, nothing rendered)
    - Correct lang variable: bcp47 chain (matches original partial)
    - Restored placeholder state with English link
    - Restored mailto subject with page title + language (inbox triage)

  Behavior matrix (unchanged from v1.3.4):
    page.lang  translation_status              Render
    ---------  ------------------------------  ---------------------------------
    en         (any)                           NOTHING — English is canonical
    non-en     placeholder                     Pending notice + English link
    non-en     ai_translated / reviewed /      Slim AI disclosure bar (Option A)
               community_corrected / live

  Design (Option A — locked by JEC panel):
    - Single persistent line, no dismiss button, no JS toggle
    - Positioned between lang-eyebrow and site-header (baseof.html)
    - .disclosure-slim CSS block in site.css
    - JEC-converged strings in each language's i18n TOML

  OIL Decision 2 contracts preserved:
    - NOT dismissible
    - Does NOT replace FPPC §84305 footer (Deliverable 9)
    - Mailto subject auto-populates page title + language for operator triage
  --------------------------------------------------------------------------
*/}}
{{ $currentLang := .Site.Language.Params.bcp47 | default (.Site.Language.LanguageCode | default .Site.Language.Lang) }}
{{ if ne $currentLang "en" }}
  {{ $translationStatusData := index (index hugo.Data "translation_status") "pages" }}
  {{ $thisStatusPath := .RelPermalink }}
  {{ with .Params.canonical_path }}{{ $thisStatusPath = . }}{{ end }}
  {{ $thisPageKey := printf "%s::%s" $thisStatusPath $currentLang }}
  {{ $thisStatus := index $translationStatusData $thisPageKey | default "placeholder" }}
  {{/* Mailto subject: "Translation feedback - <Page Title> (<Language>)"
       Auto-populates so operator inbox sorts feedback by page + language. */}}
  {{ $titleEscaped := .Title | urlquery }}
  {{ $langName := .Site.Language.LanguageName }}
  {{ $mailto := printf "mailto:%s?subject=Translation%%20feedback%%20-%%20%s%%20(%s)" (i18n "contact_email") $titleEscaped $langName }}
  {{ if eq $thisStatus "placeholder" }}
    {{/* Translation-pending: show notice and link to English version. */}}
    {{ $englishPage := "" }}
    {{ with .AllTranslations }}
      {{ range . }}
        {{ if eq .Lang "en" }}{{ $englishPage = . }}{{ end }}
      {{ end }}
    {{ end }}
    <div class="disclosure-slim disclosure-slim--pending" role="note" lang="{{ $currentLang }}">
      <span class="disclosure-slim__icon" aria-hidden="true">📄</span>
      <span class="disclosure-slim__body">{{ i18n "translation_pending_notice" }}</span>
      {{ if $englishPage }}
        <span class="disclosure-slim__sep" aria-hidden="true">·</span>
        <a class="disclosure-slim__link"
           href="{{ $englishPage.Permalink }}"
           hreflang="en"
           lang="en">{{ i18n "translation_pending_link" }}</a>
      {{ end }}
    </div>
  {{ else }}
    {{/* AI disclosure bar — ai_translated, reviewed, community_corrected, live. */}}
    <div class="disclosure-slim" role="note" lang="{{ $currentLang }}">
      <span class="disclosure-slim__icon" aria-hidden="true">🌐</span>
      <span class="disclosure-slim__body">{{ i18n "ai_translation_disclosure_body" }}</span>
      <span class="disclosure-slim__sep" aria-hidden="true">·</span>
      <a class="disclosure-slim__link" href="{{ $mailto }}">{{ i18n "ai_translation_disclosure_link_text" }}</a>
    </div>
  {{ end }}
{{ end }}
{{/* End ai-translation-disclosure.html */}}
"""

PARTIAL.write_text(NEW_PARTIAL, encoding="utf-8")
print(f"  OK    ai-translation-disclosure.html (broken v1.3.5 saved as .v135a.bak)")

# ── done ──────────────────────────────────────────────────────────────────────
print("""
Fix applied. Run CI gates then deploy:

  hugo --minify --logLevel warn 2>/dev/null && echo "build OK" && \\
  ./bin/check-i18n-parity.sh && \\
  ./bin/check-fppc-footer.sh public/ && \\
  ./bin/check-utm-hygiene.sh public/ && \\
  ./bin/check-no-jd-references.sh && \\
  ./bin/check-translation-status.sh

Verify disclosure renders before deploy:

  hugo --minify --logLevel warn 2>/dev/null
  grep -c "disclosure-slim" public/es/index.html
  grep -c "disclosure-slim" public/zh-hant/index.html
  grep -c "disclosure-slim" public/ar/index.html

Expected: 1 on each. Then:

  npx wrangler pages deploy public/ --project-name turonsf-com

Confirm live:

  curl -s https://turonsf.com/es/ | grep -o "disclosure-slim[^<]*" | head -3
  curl -s https://turonsf.com/ar/ | grep -o "disclosure-slim[^<]*" | head -3

Then commit:

  git add -A
  git commit -m "fix(disclosure): correct data path + bcp47 lang — slim bar now renders (v1.3.5b)"
  git push origin main
  git tag v1.3.5b
  git push origin v1.3.5b
""")
