#!/usr/bin/env bash
#
# check-no-jd-references.sh
#
# Enforces the LOCKED constraint that "Data Scientist, SFUSD Parent" is the only
# role tag used in any campaign-public content, in any language. References to
# Juris Doctor / attorney / lawyer (and translations) are forbidden anywhere a
# visitor might read them.
#
# Reference: Decisions Register (LOCKED) + audit F1-F14.

set -euo pipefail

# Patterns to search for, case-insensitive. Includes English + translated
# equivalents for the six target languages.
declare -a PATTERNS=(
  "juris doctor"
  "attorney"
  "lawyer"
  '\bJD\b'
  "abogad"            # Spanish: abogado/abogada
  "律师"               # Mandarin
  "律師"               # Traditional Chinese
  "abogado"           # Tagalog uses Spanish loanword
  "luật sư"           # Vietnamese
  "محامي"             # Arabic
)

# Search scope: only content/ and themes/turon-civic/i18n/. Skip docs/ and bin/
# (those discuss the prohibition explicitly).
declare -a SCOPE=(
  "content"
  "themes/turon-civic/i18n"
)

FAIL=0
for pattern in "${PATTERNS[@]}"; do
  for scope in "${SCOPE[@]}"; do
    if [[ ! -d "$scope" ]]; then continue; fi
    MATCHES=$(grep -rniE "$pattern" "$scope" 2>/dev/null || true)
    if [[ -n "$MATCHES" ]]; then
      echo "FAIL: forbidden pattern '$pattern' found in $scope:"
      echo "$MATCHES"
      echo ""
      FAIL=1
    fi
  done
done

if [[ $FAIL -eq 1 ]]; then
  echo "No-JD-references check FAILED. Role tag must be 'Data Scientist, SFUSD Parent' only."
  echo "If the match is legitimate (e.g., docs/ explaining the prohibition), move it out of content/ scope."
  exit 1
fi

echo "No JD/attorney/lawyer references: OK"
