#!/usr/bin/env bash
set -Eeuo pipefail

case "$(pwd)" in
  "$HOME"/www/turonsf_com|/www/turonsf_com) ;;
  *)
    echo "ERROR: This command must run only from ~/www/turonsf_com or /www/turonsf_com" >&2
    exit 1
    ;;
esac

if pwd | grep -Eiq 'CAREInstitute|careinstitute'; then
  echo "ERROR: Refusing CAREInstitute path." >&2
  exit 1
fi

echo "OK: Turon path guard passed at $(pwd)"
