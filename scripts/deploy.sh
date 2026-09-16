#!/usr/bin/env bash
# Deploy the static site to the Lightsail host.
#
#   ./scripts/deploy.sh preview   -> https://bdtirupati.com/preview/
#   ./scripts/deploy.sh live      -> https://bdtirupati.com/
set -euo pipefail

TARGET="${1:-preview}"
KEY="${BD_SSH_KEY:-$HOME/Documents/brhad-mrdanga.pem}"
HOST="${BD_SSH_HOST:-ubuntu@13.232.71.204}"
SRC="$(cd "$(dirname "$0")/.." && pwd)/public/"

case "$TARGET" in
  preview) DEST=/var/www/html/bd-site-preview ;;
  live)    DEST=/var/www/html/bd-site ;;
  *) echo "usage: $0 [preview|live]" >&2; exit 1 ;;
esac

ssh -i "$KEY" -o StrictHostKeyChecking=no "$HOST" "sudo mkdir -p $DEST && sudo chown -R ubuntu:ubuntu $DEST"
rsync -az --delete -e "ssh -i $KEY -o StrictHostKeyChecking=no" "$SRC" "$HOST:$DEST/"

echo "Deployed to $DEST"
[ "$TARGET" = preview ] && echo "https://bdtirupati.com/preview/" || echo "https://bdtirupati.com/"
