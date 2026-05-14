#!/usr/bin/env python3
"""
v1.3.5c patch — desktop copy-to-clipboard + help@turonsf.com + JEC toast strings
5 change groups:
  1. 7 i18n TOMLs — add disclosure_copied toast key (JEC 9.5 convergence)
  2. ai-translation-disclosure.html — help@ in mailto + dual link/button structure
  3. analytics.js — copy handler + toast renderer inside IIFE (CSP-safe)
  4. site.css — toast animation + mobile/desktop link toggle

UX contract:
  Mobile  (<768px): <a href="mailto:help@..."> → native mail app (unchanged)
  Desktop (≥768px): <button data-copy-email> → clipboard + i18n toast

Run from: /Users/turonbot/www/turonsf_com
  python3 v135c_patch.py
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


def add_toml_key(path: Path, anchor_link: str, new_key: str, new_val: str) -> None:
    """Append [new_key] block immediately after the anchor_link_text block."""
    text = path.read_text(encoding="utf-8")
    old = f'[ai_translation_disclosure_link_text]\nother = "{anchor_link}"'
    new = old + f'\n[{new_key}]\nother = "{new_val}"'
    count = text.count(old)
    if count == 0:
        print(f"  MISS  {path.name}: anchor link not found\n"
              f"        expected: {anchor_link[:60]}…")
        sys.exit(1)
    if count > 1:
        print(f"  AMBIG {path.name}: anchor matched {count} times")
        sys.exit(1)
    path.write_text(text.replace(old, new), encoding="utf-8")
    print(f"  OK    {path.name}")


# ── 1. i18n TOMLs — add disclosure_copied toast key ──────────────────────────
# JEC full-panel convergence — all 6 languages at 9.5.
# Structure: [action word] [instruction to write] help@turonsf.com
# EN added for parity only — English pages never show disclosure.
print("\n1. Adding disclosure_copied toast key to all 7 TOMLs")

TOML_UPDATES = {
    # anchor = current ai_translation_disclosure_link_text value (set by v1.3.5)
    # toast  = JEC-converged copy-confirmation string
    "en": {
        "anchor": "Help us improve it for more families.",
        "toast":  "Copied! Email us at help@turonsf.com",
    },
    # ES 9.5 — "¡Copiado!" celebratory · "Escríbenos" = write to us (familiar)
    # "a help@" correct Spanish preposition before email
    "es": {
        "anchor": "¿Nos ayudas a mejorarlo?",
        "toast":  "¡Copiado! Escríbenos a help@turonsf.com",
    },
    # 繁體 9.5 — "已複製" clean confirmation · "·" pause for older readers
    # "歡迎來信" = welcome to write (open/inviting) vs "請寫信至" (obligating)
    "zh-Hant": {
        "anchor": "您的寶貴意見能讓更多家庭受益",
        "toast":  "已複製 · 歡迎來信：help@turonsf.com",
    },
    # 简体 9.5 — mirrors 繁體 structure; "欢迎来信" preferred over "请写信至"
    # Wei/Jason (high literacy): conceded warm frame serves broader community
    "zh-Hans": {
        "anchor": "您的意见能让更多家庭受益",
        "toast":  "已复制 · 欢迎来信：help@turonsf.com",
    },
    # TL 9.5 — "Nakopya!" natural Filipino · "sa amin" (to us) = bayanihan warmth
    # Lorna 9.5 → bumped from 9.0 on Cycle 2 "sa amin" addition
    "tl": {
        "anchor": "Tulungan kami na mapabuti para sa lahat",
        "toast":  "Nakopya! Mag-email sa amin: help@turonsf.com",
    },
    # VI 9.5 — "Viết thư" (write a letter) > "gửi email" for all generations
    # Bà Nguyễn: "viết thư" is her frame — letter-writing, not email tech
    "vi": {
        "anchor": "Góp ý giúp thêm nhiều gia đình",
        "toast":  "Đã sao chép! Viết thư cho chúng tôi: help@turonsf.com",
    },
    # AR 9.5 — "نُسخ بنجاح" (copied successfully) = small celebratory win
    # "·" separator · "راسلنا" (correspond with us) = warm inviting imperative
    "ar": {
        "anchor": "شاركنا رأيك لتستفيد عائلات أخرى",
        "toast":  "نُسخ بنجاح · راسلنا: help@turonsf.com",
    },
}

i18n_dir = THEME / "i18n"
for toml_path in sorted(i18n_dir.glob("*.toml")):
    lang_key = toml_path.stem
    if lang_key not in TOML_UPDATES:
        print(f"  SKIP  {toml_path.name} — no entry defined")
        continue
    u = TOML_UPDATES[lang_key]
    add_toml_key(toml_path, u["anchor"], "disclosure_copied", u["toast"])


# ── 2. ai-translation-disclosure.html — help@ + dual link/button ─────────────
print("\n2. Patching ai-translation-disclosure.html")

partial = THEME / "layouts/partials/ai-translation-disclosure.html"
shutil.copy2(partial, partial.with_suffix(".html.v135b.bak"))
print(f"  BAK   {partial.with_suffix('.html.v135b.bak').relative_to(BASE)}")

# 2a. Change mailto URL: replace (i18n "contact_email") with hardcoded help@
# help@turonsf.com is a dedicated disclosure address — not translatable.
# contact_email (info@) remains unchanged for all other site uses.
patch(
    partial,
    'printf "mailto:%s?subject=Translation%%20feedback%%20-%%20%s%%20(%s)" '
    '(i18n "contact_email") $titleEscaped $langName }}',
    'printf "mailto:help@turonsf.com?subject=Translation%%20feedback%%20-%%20%s%%20(%s)" '
    '$titleEscaped $langName }}',
    "mailto: info@ → help@turonsf.com",
)

# 2b. Replace single <a> link with dual link + button structure.
# Mobile  (<768px): <a class="disclosure-link--mailto"> — opens native mail app
# Desktop (≥768px): <button class="disclosure-link--copy"> — clipboard + toast
# Both carry the same i18n link text; CSS show/hide determines which renders.
patch(
    partial,
    '      <a class="disclosure-slim__link" href="{{ $mailto }}">'
    '{{ i18n "ai_translation_disclosure_link_text" }}</a>',
    '      <a class="disclosure-slim__link disclosure-link--mailto" href="{{ $mailto }}">'
    '{{ i18n "ai_translation_disclosure_link_text" }}</a>'
    '<button class="disclosure-slim__link disclosure-link--copy" type="button" '
    'data-copy-email="help@turonsf.com" '
    'data-toast="{{ i18n \\"disclosure_copied\\" }}">'
    '{{ i18n "ai_translation_disclosure_link_text" }}</button>',
    "single <a> → <a> mobile + <button> desktop",
)


# ── 3. analytics.js — copy handler + toast inside IIFE ───────────────────────
# Per Section 2.4: add code INSIDE the IIFE before the closing })();
# Function names prefixed _disc_ to avoid collision with existing copy handler.
print("\n3. Patching analytics.js — disclosure copy handler")

analytics = THEME / "assets/js/analytics.js"

# Verify single IIFE close before patching (Section 2.4 landmine)
raw = analytics.read_text(encoding="utf-8")
iife_count = raw.count("})()")
if iife_count != 1:
    print(f"  ERROR analytics.js has {iife_count} occurrences of }})() — "
          f"expected exactly 1. Aborting.")
    sys.exit(1)
print(f"  OK    IIFE close count: {iife_count} (safe to patch)")

COPY_HANDLER = """
  // ── Disclosure link: copy-to-clipboard (v1.3.5c) ────────────────────────
  // Mobile  (<768px): .disclosure-link--mailto visible, handled by native href.
  // Desktop (≥768px): .disclosure-link--copy visible, handled by this handler.
  // data-copy-email: email address to copy (help@turonsf.com)
  // data-toast:      i18n confirmation string rendered by Hugo at build time

  function _discShowToast(msg) {
    var el = document.createElement('div');
    el.className = 'disclosure-toast';
    el.setAttribute('role', 'status');
    el.setAttribute('aria-live', 'polite');
    el.textContent = msg;
    document.body.appendChild(el);
    // Double rAF forces CSS transition to fire after paint
    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        el.classList.add('disclosure-toast--visible');
      });
    });
    setTimeout(function () {
      el.classList.remove('disclosure-toast--visible');
      setTimeout(function () {
        if (el.parentNode) el.parentNode.removeChild(el);
      }, 300);
    }, 2500);
  }

  function _discFallbackCopy(email, toast) {
    var ta = document.createElement('textarea');
    ta.value = email;
    ta.style.cssText = 'position:fixed;top:0;left:0;opacity:0;pointer-events:none;';
    document.body.appendChild(ta);
    ta.focus();
    ta.select();
    try { document.execCommand('copy'); _discShowToast(toast); } catch (err) {}
    document.body.removeChild(ta);
  }

  document.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-copy-email]');
    if (!btn) return;
    var email = btn.getAttribute('data-copy-email');
    var toast = btn.getAttribute('data-toast') || 'Copied!';
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(email)
        .then(function () { _discShowToast(toast); })
        .catch(function () { _discFallbackCopy(email, toast); });
    } else {
      _discFallbackCopy(email, toast);
    }
  });
  // ── end disclosure copy handler ───────────────────────────────────────────
"""

patch(
    analytics,
    "\n})();",
    COPY_HANDLER + "\n})();",
    "add _discShowToast + _discFallbackCopy + click handler inside IIFE",
)

# Verify still exactly one IIFE close
raw2 = analytics.read_text(encoding="utf-8")
iife_count2 = raw2.count("})()")
if iife_count2 != 1:
    print(f"  ERROR post-patch IIFE count is {iife_count2} — expected 1. "
          f"Check analytics.js manually.")
    sys.exit(1)
print(f"  OK    post-patch IIFE close count: {iife_count2} ✓")


# ── 4. site.css — toast animation + link toggle ───────────────────────────────
print("\n4. Patching site.css — toast + link toggle")

# Anchor: last rule added in v1.3.5b
OLD_CSS_ANCHOR = ".disclosure-slim__link:hover { text-decoration: underline; }"

NEW_CSS_BLOCK = """\
.disclosure-slim__link:hover { text-decoration: underline; }
/* Mobile/desktop link toggle — mirrors .share-mailto-btn / .share-copy-btn pattern */
.disclosure-link--mailto { }
.disclosure-link--copy { display: none; background: none; border: none; \
cursor: pointer; font: inherit; padding: 0; }
@media (min-width: 768px) {
  .disclosure-link--mailto { display: none; }
  .disclosure-link--copy { display: inline; }
}
/* Copy confirmation toast */
.disclosure-toast { position: fixed; bottom: 1.5rem; left: 50%; \
transform: translateX(-50%) translateY(0.5rem); background: var(--navy-900); \
color: var(--cream-50); font-size: 0.82rem; font-family: var(--sans); \
padding: 0.55rem 1.25rem; border-radius: 999px; white-space: nowrap; \
z-index: 500; opacity: 0; pointer-events: none; \
transition: opacity 0.2s ease, transform 0.2s ease; \
box-shadow: 0 4px 16px rgba(7,26,47,0.22); }
.disclosure-toast--visible { opacity: 1; transform: translateX(-50%) translateY(0); }\
"""

patch(
    THEME / "static/css/site.css",
    OLD_CSS_ANCHOR,
    NEW_CSS_BLOCK,
    "toast animation + .disclosure-link mobile/desktop toggle",
)


# ── done ──────────────────────────────────────────────────────────────────────
print("""
All patches applied. Verify IIFE integrity then run CI gates:

  grep -c "})()" themes/turon-civic/assets/js/analytics.js

  hugo --minify --logLevel warn 2>/dev/null && echo "build OK" && \\
  ./bin/check-i18n-parity.sh && \\
  ./bin/check-fppc-footer.sh public/ && \\
  ./bin/check-utm-hygiene.sh public/ && \\
  ./bin/check-no-jd-references.sh && \\
  ./bin/check-translation-status.sh

Local disclosure check:

  grep -c "disclosure-slim" public/es/index.html
  grep -c "disclosure-link--copy" public/es/index.html
  grep -c "disclosure-link--mailto" public/es/index.html

Expected: 5 / 1 / 1 on each non-EN page. Then deploy:

  npx wrangler pages deploy public/ --project-name turonsf-com

Confirm live (ES spot check):

  curl -s https://turonsf.com/es/ | grep -o "disclosure-link--[a-z]*"

Then commit and tag:

  git add -A
  git commit -m "feat(disclosure): desktop copy+toast, help@ routing, JEC toast strings (v1.3.5c)"
  git push origin main
  git tag v1.3.5c
  git push origin v1.3.5c

Sam Ray note: help@turonsf.com in mailto only — info@turonsf.com unchanged
everywhere else on site. Confirm dedicated address satisfies your review.
""")
