#!/bin/bash

find p1204_3 -name *.py \
    | grep -v "bitstream_mode3_videoparser" \
    | grep -v "__pycache__" | xargs -i black -l 120 {}

find tests -name *.py \
    | grep -v "__pycache__" | xargs -i black -l 120 {}
