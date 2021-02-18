#!/bin/sh
test_dir="$(realpath $(dirname $"0"))/test_videos"
mkdir -p tmp
mkdir -p reports
tmp="$(realpath $(dirname $"0"))/tmp"
reports="$(realpath $(dirname $"0"))/reports"

docker build --tag p1204-test .
docker run --rm -i -v ${test_dir}:/test_videos \
    -v ${tmp}:/tmp \
    -v ${reports}:/reports \
    -t p1204-test --tmp "/tmp" --result_folder "/reports" /test_videos/test_video_h264.mkv
