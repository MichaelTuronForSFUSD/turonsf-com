#!/usr/bin/env bash
#
# check-fppc-footer.sh
#
# Verifies that FPPC ID 1482971 appears in every rendered HTML page under public/.
# A missing footer on any page is a §84305 compliance failure.
#
# Reference: docs/Deliverable_9_FPPC_Footer_Disclosure.md, Preflight §5.

set -euo pipefail

PUBLIC_DIR="${1:-public}"
FPPC_ID="1482971"

if [[ ! -d "$PUBLIC_DIR" ]]; then
  echo "ERROR: $PUBLIC_DIR not found. Run 'hugo --minify' first." >&2
  exit 1
fi

# Find every rendered index.html (root + language + page subdirectories)
PAGES=$(find "$PUBLIC_DIR" -name "index.html" -type f)

if [[ -z "$PAGES" ]]; then
  echo "ERROR: no rendered index.html found under $PUBLIC_DIR" >&2
  exit 1
fi

FAIL=0
MISSING=()
while IFS= read -r page; do
  grep -q "http-equiv=refresh" "$page" && continue
  if ! grep -q "$FPPC_ID" "$page"; then
    MISSING+=("$page")
    FAIL=1
  fi
done <<< "$PAGES"

if [[ $FAIL -eq 1 ]]; then
  echo "FAIL: FPPC ID $FPPC_ID missing from the following pages:"
  for p in "${MISSING[@]}"; do echo "  $p"; done
  echo ""
  echo "Every public-facing page must carry the §84305 footer. Check the footer partial."
  exit 1
fi

PAGE_COUNT=$(echo "$PAGES" | wc -l | tr -d ' ')
echo "FPPC footer present: OK ($PAGE_COUNT pages, all carry ID $FPPC_ID)"
