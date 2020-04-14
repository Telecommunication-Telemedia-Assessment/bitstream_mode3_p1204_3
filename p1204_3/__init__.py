#!/usr/bin/env python3
__version__ = "0.1.1" #
import argparse
import sys
import os
import json
import multiprocessing
import logging
import itertools

from p1204_3.utils import *
from p1204_3.model import P1204BitstreamMode3
from p1204_3.generic import *


def predict_quality(
    videofilename,
    model_config_filename,
    device_type="pc",
    device_resolution="3840x2160",
    viewing_distance="1.5xH",
    display_size=55,
    temporary_folder="tmp",
):
    return P1204BitstreamMode3().predict_quality(
        videofilename,
        model_config_filename,
        device_type,
        device_resolution,
        viewing_distance,
        display_size,
        temporary_folder,
    )


def main(_=[]):
    # argument parsing
    parser = argparse.ArgumentParser(
        description="ITU-T P.1204.3 video quality model reference implementation",
        epilog="stg7, rrao 2020",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("video", type=str, nargs="+", help="input video to estimate quality")
    parser.add_argument("--result_folder", type=str, default="reports", help="folder to store video quality results")
    parser.add_argument(
        "--model",
        type=str,
        default=os.path.join(os.path.dirname(__file__), "models/p1204_3/config.json"),
        help="model config file to be used for prediction",
    )
    parser.add_argument("--cpu_count", type=int, default=multiprocessing.cpu_count(), help="thread/cpu count")
    parser.add_argument("--device_type", choices=DEVICE_TYPES, default="pc", help="device that is used for playout")
    parser.add_argument(
        "--device_resolution",
        choices=DEVICE_RESOLUTIONS,
        default="3840x2160",
        help="resolution of the output device (width x height)",
    )
    parser.add_argument(
        "--viewing_distance",
        choices=VIEWING_DISTANCES,
        default="1.5xH",
        help="viewing distance relative to the display height",
    )
    parser.add_argument(
        "--display_size", choices=DISPLAY_SIZES, type=float, default=55, help="display diagonal size in inches"
    )
    parser.add_argument(
        "--tmp",
        type=str,
        default="./tmp",
        help="temporary folder to store bitstream stats and other intermediate results",
    )

    a = vars(parser.parse_args())
    logging.basicConfig(level=logging.DEBUG)

    assert_file(a["model"], "model folder is not valid")
    logging.info(f"handle the following videos (# {len(a['video'])}): \n  " + "\n  ".join(a["video"]))
    params = [
        (
            video,
            a["model"],
            a["device_type"],
            a["device_resolution"],
            a["viewing_distance"],
            a["display_size"],
            a["tmp"],
        )
        for video in a["video"]
    ]
    if a["cpu_count"] > 1:
        pool = multiprocessing.Pool(a["cpu_count"])
        results = pool.starmap(predict_quality, params)
    else:
        results = list(itertools.starmap(predict_quality, params))

    print(json.dumps(results, indent=4, sort_keys=True))
    logging.info(f"""store all results to {a["result_folder"]}""")
    os.makedirs(a["result_folder"], exist_ok=True)
    for result in results:
        if result == {} or "video_basename" not in result:
            # in case the video could not be processed, just ignore it
            continue
        reportname = os.path.join(a["result_folder"], os.path.splitext(result["video_basename"])[0] + ".json")
        json_store(reportname, result)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
