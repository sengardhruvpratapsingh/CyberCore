#!/bin/sh
set -eu

: "${CYBERCORE_API_HOST:?CYBERCORE_API_HOST must be set by render.yaml}"

case "$CYBERCORE_API_HOST" in
    http://*|https://*) api_base="$CYBERCORE_API_HOST" ;;
    *) api_base="https://$CYBERCORE_API_HOST" ;;
esac

printf 'window.__API_BASE__ = "%s";\n' "$api_base" > api-config.js
