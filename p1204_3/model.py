#!/usr/bin/env python3
import logging
import json

from p1204_3.utils import assert_file
from p1204_3.utils import assert_msg
from p1204_3.utils import ffprobe
from p1204_3.generic import *


def predict_quality(videofilename,
    model_config_filename,
    device_type="pc",
    device_resolution="3840x2160",
    viewing_distance="1.5xH",
    display_size=55):

    assert_file(videofilename, f"{videofilename} does not exist, please check")
    assert_file(model_config_filename, f"{model_config_filename} does not exist, please check")

    device_type = device_type.lower()
    assert_msg(device_type in DEVICE_TYPES, f"specified device_type '{device_type}' is not supported, only {DEVICE_TYPES} possible")
    assert_msg(device_resolution in DEVICE_RESOLUTIONS, f"specified device_resolution '{device_resolution}' is not supported, only {DEVICE_RESOLUTIONS} possible")
    assert_msg(viewing_distance in VIEWING_DISTANCES, f"specified viewing_distance '{viewing_distance}' is not supported, only {VIEWING_DISTANCES} possible")
    assert_msg(display_size in DISPLAY_SIZES, f"specified display_size '{display_size}' is not supported, only {DISPLAY_SIZES} possible")

    ffprobe_result = ffprobe(videofilename)
    assert_msg(ffprobe_result["codec"] in CODECS_SUPPORTED, f"your video codec is not supported by the model: {ffprobe_result['codec']}")

    with open(model_config_filename) as mfp:
        model_config = json.load(mfp)

    rf_model = model_config["rf"]
    model_coefficients = model_config["coefficients"]


    return {
        "per_second": [42],
        "per_sequence": 42
    }
