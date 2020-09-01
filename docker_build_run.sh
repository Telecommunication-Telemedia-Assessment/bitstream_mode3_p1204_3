#!/bin/sh
docker build --tag p1204-test .
docker run --rm -i -t p1204-test test_videos/test_video_h264.mkv