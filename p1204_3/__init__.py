#!/usr/bin/env python3
import argparse
import sys
import os
import json
import multiprocessing
import logging

from p1204_3.utils import *
from p1204_3.model import predict_quality
from p1204_3.generic import *


def main(_=[]):
    # argument parsing
    parser = argparse.ArgumentParser(
        description="ITU-T P.1204.3 video quality model reference implementation",
        epilog="stg7, rrao 2019",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "video", type=str, nargs="+", help="input video to estimate quality"
    )
    parser.add_argument(
        "--result_folder",
        type=str,
        default="reports",
        help="folder to store video quality results",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=os.path.join(os.path.dirname(__file__), "models/p1204_3/config.json"),
        help="model config file to be used for prediction",
    )
    parser.add_argument(
        "--cpu_count",
        type=int,
        default=multiprocessing.cpu_count(),
        help="thread/cpu count",
    )
    parser.add_argument(
        "--device_type",
        choices=DEVICE_TYPES,
        default="pc",
        help="device that is used for playout"
    )
    parser.add_argument(
        "--device_resolution",
        choices=DEVICE_RESOLUTIONS,
        default="3840x2160",
        help="resolution of the output device (width x height)"
    )
    parser.add_argument(
        "--viewing_distance",
        choices=VIEWING_DISTANCES,
        default="1.5xH",
        help="viewing distance relative to the display height"
    )
    parser.add_argument(
        "--display_size",
        choices=DISPLAY_SIZES,
        type=float,
        default=55,
        help="display diagonal size in inches"
    )

    a = vars(parser.parse_args())

    assert_file(a["model"], "model folder is not valid")
    logging.info(a["video"])

    pool = multiprocessing.Pool(a["cpu_count"])
    params = [(video, a["model"], a["device_type"], a["device_resolution"], a["viewing_distance"]) for video in a["video"]]
    results = pool.starmap(predict_quality, params)



if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
