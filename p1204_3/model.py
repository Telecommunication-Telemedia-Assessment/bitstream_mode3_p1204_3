#!/usr/bin/env python3
import logging

from p1204_3.utils import assert_file
from p1204_3.utils import assert_msg
from p1204_3.generic import *


def predict_quality(videofilename,
    model,
    device_type="pc",
    device_resolution="3840x2160",
    viewing_distance="1.5xH"):

    assert_file(videofilename, f"{videofilename} does not exist, please check")

    device_type = device_type.lower()
    assert_msg(device_type in DEVICE_TYPES, f"specified device_type '{device_type}' is not supported, only {DEVICE_TYPES} possible")
    assert_msg(device_resolution in DEVICE_RESOLUTIONS, f"specified device_resolution '{device_resolution}' is not supported, only {DEVICE_RESOLUTIONS} possible")
    assert_msg(viewing_distance in VIEWING_DISTANCES, f"specified viewing_distance '{viewing_distance}' is not supported, only {VIEWING_DISTANCES} possible")



    return {
        "per_second": [42],
        "per_sequence": 42
    }
