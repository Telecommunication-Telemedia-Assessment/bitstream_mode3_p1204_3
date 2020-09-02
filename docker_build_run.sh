#!/bin/sh
testDir="$(realpath $(dirname $"0"))/test_videos"
docker build --tag p1204-test .
docker run --rm -i -t p1204-test -v ${testDir}:/test_videos /test_videos/test_video_h264.mkv
