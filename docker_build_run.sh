#!/bin/sh
testDir="$(realpath $(dirname $"0"))/test_videos"
docker build --tag p1204-test .
docker run --rm -i -v ${testDir}:/test_videos -t p1204-test /test_videos/test_video_h264.mkv
