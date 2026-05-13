#!/usr/bin/env bash
#
# check-translation-status.sh
#
# Verifies that every (page, language) pair in data/translation_status.yaml has
# either a corresponding scaffold file in content/ OR is marked as deferred.
# Catches the case where a page is added to translation_status but the scaffold
# never landed (would cause hreflang to reference a non-existent URL).
#
# Reference: docs/Phase1_to_Phase2_Architecture_Readiness.md §2.2.

set -euo pipefail

YAML="data/translation_status.yaml"
CONTENT="content"

if [[ ! -f "$YAML" ]]; then
  echo "ERROR: $YAML not found" >&2
  exit 1
fi

# Extract page paths from YAML keys like "/about/::es"
ENTRIES=$(grep -oE '"/[^:]*::[a-zA-Z\-]+"' "$YAML" | tr -d '"' || true)

if [[ -z "$ENTRIES" ]]; then
  echo "WARN: no translation_status entries found"
  exit 0
fi

ENTRY_COUNT=$(echo "$ENTRIES" | wc -l | tr -d ' ')

# For each entry, derive expected scaffold path and verify existence.
FAIL=0
while IFS= read -r entry; do
  PAGE="${entry%%::*}"
  LANG="${entry##*::}"

  # Map page path to scaffold filename
  # "/" → content/_index.{lang}.md (home is a section)
  # "/about/" → content/about.{lang}.md (regular page)
  # "/platform/" → content/platform/_index.{lang}.md (section bundle — _index pattern)
  # "/platform/pillar-1/" → content/platform/pillar-1.{lang}.md (regular page in section)
  # "/letters/uesf-2026-05-12/" → content/letters/uesf-2026-05-12/index.{lang}.md (page bundle)

  if [[ "$PAGE" == "/" ]]; then
    EXPECTED="$CONTENT/_index.$LANG.md"
  elif [[ "$PAGE" == "/letters/"* ]]; then
    BUNDLE_DIR="${PAGE%/}"
    EXPECTED="$CONTENT$BUNDLE_DIR/index.$LANG.md"
  elif [[ "$PAGE" == "/platform/" ]]; then
    EXPECTED="$CONTENT/platform/_index.$LANG.md"
  else
    SLUG="${PAGE%/}"  # strip trailing slash
    EXPECTED="$CONTENT$SLUG.$LANG.md"
  fi

  if [[ ! -f "$EXPECTED" ]]; then
    echo "FAIL: translation_status entry $entry expects scaffold at $EXPECTED but it doesn't exist"
    FAIL=1
  fi
done <<< "$ENTRIES"

if [[ $FAIL -eq 1 ]]; then
  echo ""
  echo "translation_status consistency FAILED. Every YAML entry must have a corresponding scaffold."
  exit 1
fi

echo "translation_status consistency: OK ($ENTRY_COUNT entries, all scaffolds present)"
