#!/bin/bash
set -e
cd "$(dirname "$0")"

echo "converting videos to mpeg4"
mkdir -p out/

for f in *.mp4; do
  ffmpeg -y -i "$f" -vf scale=2160:1080 -r 30 -c:v h264 -strict -2 "out/$f"
done;

echo "Success!"
