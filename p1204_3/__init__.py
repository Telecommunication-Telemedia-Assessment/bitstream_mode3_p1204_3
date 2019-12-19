#!/usr/bin/env python3
import argparse
import sys
import os
import json
import multiprocessing

from p1204_3.utils import *


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
        default=os.path.join(os.path.dirname(__file__), "models/p1204_3"),
        help="model to be used for prediction",
    )
    parser.add_argument(
        "--cpu_count",
        type=int,
        default=multiprocessing.cpu_count(),
        help="thread/cpu count",
    )

    a = vars(parser.parse_args())

    assert_file(os.path.join(a["model"], "config.json"), "model folder is not valid")
    print(a["video"])


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
