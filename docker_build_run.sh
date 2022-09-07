#!/usr/bin/env bash

set -e

cd "$(dirname "$0")" || exit 1

test_dir="$(realpath $(dirname $"0"))/test_videos"
mkdir -p tmp
mkdir -p reports
tmp="$(realpath $(dirname $"0"))/tmp"
reports="$(realpath $(dirname $"0"))/reports"

if ! [[ -d p1204_3/bitstream_mode3_videoparser ]]; then
    git clone https://github.com/Telecommunication-Telemedia-Assessment/bitstream_mode3_videoparser.git p1204_3/bitstream_mode3_videoparser
else
    git -C p1204_3/bitstream_mode3_videoparser fetch --all
    git -C p1204_3/bitstream_mode3_videoparser reset --hard origin/master
fi

docker build --tag p1204-test .
docker run --rm -i -v ${test_dir}:/test_videos \
    -v ${tmp}:/tmp \
    -v ${reports}:/reports \
    -t p1204-test --tmp "/tmp" --result_folder "/reports" /test_videos/test_video_h264.mkv
