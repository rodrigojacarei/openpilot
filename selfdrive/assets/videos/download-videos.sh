#!/bin/bash
set -e
cd "$(dirname "$0")"

AZ_BASEDIR="https://commadataci.blob.core.windows.net/cesdemo"
MANIFEST="$AZ_BASEDIR/manifest.txt"

echo "downloading videos"
mkdir -p out/

while read -r line; do
  if [ -n "$line" ]; then
    wget "$AZ_BASEDIR/$line" -O "./$line"
  fi
done < <(curl -w '\n' -s "$MANIFEST")

echo "Success!"
