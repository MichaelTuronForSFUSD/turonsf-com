#!/usr/bin/env python3
"""
v1.3.5d patch — fix duplicate disclosure link
Root cause: <a> + <button> both visible because CSS show/hide was unreliable.
Fix: single <a data-copy-email> element; JS intercepts click on desktop
  (≥768px → e.preventDefault() + clipboard), mobile falls through to
  native mailto: naturally. No CSS toggle needed. No duplicate HTML.

Run from: /Users/turonbot/www/turonsf_com
  python3 v135d_patch.py
"""
import re, sys, shutil
from pathlib import Path

BASE  = Path("/Users/turonbot/www/turonsf_com")
THEME = BASE / "themes/turon-civic"

def patch(path: Path, old: str, new: str, desc: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count == 0:
        print(f"  MISS  {desc}\n        not found in {path.relative_to(BASE)}")
        sys.exit(1)
    if count > 1:
        print(f"  AMBIG {desc}\n        {count} matches")
        sys.exit(1)
    path.write_text(text.replace(old, new), encoding="utf-8")
    print(f"  OK    {desc}")


# ── 1. Partial — replace <a>+<button> with single <a data-copy-email> ─────────
print("\n1. Patching ai-translation-disclosure.html")

partial = THEME / "layouts/partials/ai-translation-disclosure.html"
shutil.copy2(partial, partial.with_suffix(".html.v135c.bak"))
print(f"  BAK   {partial.with_suffix('.html.v135c.bak').relative_to(BASE)}")

# Replace dual element structure with single <a> that carries both behaviours:
# - href="$mailto"  → mobile: native mail app
# - data-copy-email → desktop: JS intercepts, copies, shows toast
patch(
    partial,
    '      <a class="disclosure-slim__link disclosure-link--mailto" href="{{ $mailto }}">'
    '{{ i18n "ai_translation_disclosure_link_text" }}</a>'
    '<button class="disclosure-slim__link disclosure-link--copy" type="button" '
    'data-copy-email="help@turonsf.com" '
    'data-toast="{{ $copied }}">'
    '{{ i18n "ai_translation_disclosure_link_text" }}</button>',
    '      <a class="disclosure-slim__link" href="{{ $mailto }}" '
    'data-copy-email="help@turonsf.com" '
    'data-toast="{{ $copied }}">'
    '{{ i18n "ai_translation_disclosure_link_text" }}</a>',
    "<a>+<button> → single <a data-copy-email>",
)


# ── 2. analytics.js — add matchMedia desktop gate + e.preventDefault() ────────
# The existing handler targets [data-copy-email] and copies unconditionally.
# Update: on desktop intercept + copy; on mobile let href="mailto:" fire natively.
print("\n2. Patching analytics.js — desktop gate + preventDefault")

analytics = THEME / "assets/js/analytics.js"
raw = analytics.read_text(encoding="utf-8")
iife_n = raw.count("})()")
if iife_n != 1:
    print(f"  ERROR IIFE count {iife_n} ≠ 1"); sys.exit(1)
print(f"  OK    IIFE count: {iife_n}")

patch(
    analytics,
    # old handler — copies on every click, no desktop gate
    "  document.addEventListener('click', function (e) {\n"
    "    var btn = e.target.closest('[data-copy-email]');\n"
    "    if (!btn) return;\n"
    "    var email = btn.getAttribute('data-copy-email');\n"
    "    var toast = btn.getAttribute('data-toast') || 'Copied!';\n"
    "    if (navigator.clipboard && navigator.clipboard.writeText) {\n"
    "      navigator.clipboard.writeText(email)\n"
    "        .then(function () { _discShowToast(toast); })\n"
    "        .catch(function () { _discFallbackCopy(email, toast); });\n"
    "    } else {\n"
    "      _discFallbackCopy(email, toast);\n"
    "    }\n"
    "  });",
    # new handler — desktop: intercept + copy; mobile: fall through to mailto
    "  document.addEventListener('click', function (e) {\n"
    "    var link = e.target.closest('[data-copy-email]');\n"
    "    if (!link) return;\n"
    "    // Desktop (≥768px): prevent mailto: navigation, copy to clipboard instead.\n"
    "    // Mobile (<768px): fall through — href='mailto:...' opens natively.\n"
    "    if (window.matchMedia && window.matchMedia('(min-width: 768px)').matches) {\n"
    "      e.preventDefault();\n"
    "      var email = link.getAttribute('data-copy-email');\n"
    "      var toast = link.getAttribute('data-toast') || 'Copied!';\n"
    "      if (navigator.clipboard && navigator.clipboard.writeText) {\n"
    "        navigator.clipboard.writeText(email)\n"
    "          .then(function () { _discShowToast(toast); })\n"
    "          .catch(function () { _discFallbackCopy(email, toast); });\n"
    "      } else {\n"
    "        _discFallbackCopy(email, toast);\n"
    "      }\n"
    "    }\n"
    "  });",
    "add matchMedia desktop gate + e.preventDefault()",
)

iife_n2 = analytics.read_text(encoding="utf-8").count("})()")
if iife_n2 != 1:
    print(f"  ERROR post-patch IIFE count {iife_n2}"); sys.exit(1)
print(f"  OK    post-patch IIFE count: {iife_n2}")


# ── 3. site.css — remove .disclosure-link--mailto/copy toggle rules ────────────
# No longer needed — single element approach removes all show/hide CSS.
# .disclosure-toast rules stay (still needed for the toast animation).
# Both duplicate occurrences removed (v135c wrote them twice by accident).
print("\n3. Cleaning site.css — remove link toggle rules (both duplicates)")

TOGGLE_BLOCK = (
    ".disclosure-link--mailto { }\n"
    ".disclosure-link--copy { display: none; background: none; border: none; "
    "cursor: pointer; font: inherit; padding: 0; }\n"
    "@media (min-width: 768px) {\n"
    "  .disclosure-link--mailto { display: none; }\n"
    "  .disclosure-link--copy { display: inline; }\n"
    "}"
)

css_path = THEME / "static/css/site.css"
css = css_path.read_text(encoding="utf-8")
count = css.count(TOGGLE_BLOCK)
print(f"  INFO  toggle block occurrences in CSS: {count}")
if count == 0:
    print("  MISS  toggle block not found — check site.css manually")
    sys.exit(1)

# Remove all occurrences (was accidentally written twice)
cleaned = css.replace(TOGGLE_BLOCK, "")
css_path.write_text(cleaned, encoding="utf-8")
print(f"  OK    removed {count} occurrence(s) of toggle block")


# ── done ──────────────────────────────────────────────────────────────────────
print("""
All patches applied. Run CI gates:

  hugo --minify --logLevel warn 2>/dev/null && echo "build OK" && \\
  ./bin/check-i18n-parity.sh && \\
  ./bin/check-fppc-footer.sh public/ && \\
  ./bin/check-utm-hygiene.sh public/ && \\
  ./bin/check-no-jd-references.sh && \\
  ./bin/check-translation-status.sh

Local structure check:

  grep -c "disclosure-link--mailto" public/es/index.html
  grep -c "disclosure-link--copy" public/es/index.html
  grep -c "data-copy-email" public/es/index.html

Expected: 0 / 0 / 1 — single <a> with data-copy-email only.

If all pass, deploy:

  npx wrangler pages deploy public/ --project-name turonsf-com

Then commit:

  git add -A
  git commit -m "fix(disclosure): single-element link — JS desktop intercept, mobile mailto native (v1.3.5d)"
  git push origin main
  git tag v1.3.5d
  git push origin v1.3.5d
""")
