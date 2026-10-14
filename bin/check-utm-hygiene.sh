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
# Michael's own campaign backends (v2 CTAs). The v3 hub has none of these.
CAMPAIGN_HOSTS_PATTERN='secure\.actblue\.com/donate/turonsf|sibforms\.com'
REQUIRED_UTMS=(utm_source utm_medium utm_campaign utm_content)

# Extract every absolute <a> href, quoted or unquoted (hugo --minify drops quotes).
ALL_URLS=$(grep -rohE "<a [^>]*href=(\"[^\"]*\"|[^ >]+)" "$PUBLIC_DIR" --include='*.html' \
  | sed -E 's/.*href=//; s/^"//; s/"$//' | grep -E '^https?://' | sort -u || true)

# v3: links to endorsed candidates' sites and donation pages, and to sources,
# must carry NO tracking parameters (redesign spec, "Candidate actions and privacy").
LEAKS=$(echo "$ALL_URLS" | grep -vE "^https?://(www\.)?turonsf\.com" | grep -vE "${CAMPAIGN_HOSTS_PATTERN}" | grep -E '[?&]utm_' || true)
if [[ -n "$LEAKS" ]]; then
  echo "FAIL: tracking parameters on non-campaign outbound links:"
  echo "$LEAKS"
  exit 1
fi

URLS=$(echo "$ALL_URLS" | grep -E "^https?://(${CAMPAIGN_HOSTS_PATTERN})" || true)

if [[ -z "$URLS" ]]; then
  echo "UTM hygiene: OK (no campaign-backend CTAs; $(echo "$ALL_URLS" | grep -c . ) outbound links carry no utm_ parameters)"
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
