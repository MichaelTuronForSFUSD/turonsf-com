#!/usr/bin/env bash
#
# check-i18n-parity.sh
#
# Verifies that the [section] key sets in all 7 i18n TOML files are identical.
# A key added or removed in one language must be reflected in all seven, or
# this script fails CI.
#
# Reference: docs/Phase1_to_Phase2_Architecture_Readiness.md §2.1 + audit F11.

set -euo pipefail

I18N_DIR="themes/turon-civic/i18n"
LANGS=(en es zh-Hant zh-Hans tl vi ar)

if [[ ! -d "$I18N_DIR" ]]; then
  echo "ERROR: $I18N_DIR not found" >&2
  exit 1
fi

# Extract [section] header lines from each TOML file, sort, compare against en.toml as canonical.
EN_KEYS=$(grep -E '^\[[a-z_]+\]$' "$I18N_DIR/en.toml" | sort)

FAIL=0
for lang in "${LANGS[@]}"; do
  if [[ "$lang" == "en" ]]; then continue; fi
  KEYS=$(grep -E '^\[[a-z_]+\]$' "$I18N_DIR/$lang.toml" | sort)
  DIFF=$(diff <(echo "$EN_KEYS") <(echo "$KEYS") || true)
  if [[ -n "$DIFF" ]]; then
    echo "FAIL: $lang.toml key set differs from en.toml"
    echo "$DIFF"
    FAIL=1
  fi
done

if [[ $FAIL -eq 1 ]]; then
  echo ""
  echo "i18n key parity check FAILED. All 7 language files must share the same [section] keys."
  exit 1
fi

echo "i18n key parity: OK (7 language files, all sections match)"
