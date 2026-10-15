#!/usr/bin/env bash
#
# check-redirects.sh
#
# Validates static/_redirects for Cloudflare Pages: every rule is exactly
# "<source> <destination> <status>", sources start with "/", status is a
# redirect code, no source repeats, and splat (dynamic) rules stay under the
# 100-rule platform limit.

set -euo pipefail

FILE="${1:-static/_redirects}"
FAIL=0

while IFS= read -r line; do
  case "$line" in ''|'#'*) continue ;; esac
  read -r -a f <<< "$line"
  if [[ ${#f[@]} -ne 3 ]]; then echo "FAIL: not 3 fields: $line"; FAIL=1; continue; fi
  [[ "${f[0]}" == /* ]] || { echo "FAIL: source must start with /: $line"; FAIL=1; }
  [[ "${f[2]}" =~ ^(301|302|303|307|308)$ ]] || { echo "FAIL: bad status: $line"; FAIL=1; }
done < "$FILE"

DUPES=$(grep -vE '^\s*(#|$)' "$FILE" | awk '{print $1}' | sort | uniq -d)
if [[ -n "$DUPES" ]]; then echo "FAIL: duplicate sources:"; echo "$DUPES"; FAIL=1; fi

SPLATS=$(grep -vE '^\s*(#|$)' "$FILE" | awk '$1 ~ /\*|:/' | wc -l | tr -d ' ')
if [[ "$SPLATS" -ge 100 ]]; then echo "FAIL: $SPLATS dynamic rules (limit 100)"; FAIL=1; fi

[[ $FAIL -eq 0 ]] || exit 1
RULES=$(grep -cvE '^\s*(#|$)' "$FILE")
echo "Redirects: OK ($RULES rules, $SPLATS dynamic)"
