#!/usr/bin/env bash
#
# check-utm-hygiene.sh
#
# Verifies that every outbound campaign URL in the rendered Hugo output
# (public/) carries all four UTM parameters: utm_source, utm_medium,
# utm_campaign, utm_content.
#
# Failing CI here prevents shipping a CTA that doesn't attribute. Audit F10.
# Reference: docs/Phase1_Analytics_Spec.md §2.
#
# Usage: ./check-utm-hygiene.sh path/to/public

set -euo pipefail

PUBLIC_DIR="${1:-public}"

if [[ ! -d "$PUBLIC_DIR" ]]; then
  echo "ERROR: $PUBLIC_DIR not found. Run 'hugo --minify' first." >&2
  exit 1
fi

# Campaign backend hostnames that must carry UTMs
CAMPAIGN_HOSTS_PATTERN='secure\.actblue\.com|actionnetwork\.org|sibforms\.com'

REQUIRED_UTMS=(utm_source utm_medium utm_campaign utm_content)

# Find every href to a campaign backend hostname
URLS=$(grep -rohE "<a [^>]*href=\"https?://(${CAMPAIGN_HOSTS_PATTERN})[^\"]*\"" "$PUBLIC_DIR" | grep -oE "href=\"[^\"]*\"" | sed 's/^href="//;s/"$//' \
  | sed 's/^href="//; s/"$//' \
  | sort -u || true)

if [[ -z "$URLS" ]]; then
  echo "WARN: no outbound campaign URLs found in $PUBLIC_DIR. Expected at least donate + volunteer + newsletter links."
  exit 0
fi

FAIL=0
while IFS= read -r url; do
  for utm in "${REQUIRED_UTMS[@]}"; do
    if ! echo "$url" | grep -q "$utm="; then
      echo "FAIL: missing $utm in URL: $url"
      FAIL=1
    fi
  done
done <<< "$URLS"

if [[ $FAIL -eq 1 ]]; then
  echo ""
  echo "UTM hygiene check FAILED. Every campaign CTA URL must carry all four UTMs."
  echo "Use the {{< cta >}} shortcode in templates to auto-append UTMs."
  exit 1
fi

URL_COUNT=$(echo "$URLS" | wc -l | tr -d ' ')
echo "UTM hygiene: OK ($URL_COUNT outbound campaign URLs, all carry 4 UTMs)"
