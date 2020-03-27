#!/usr/bin/env python3
import os
import logging

from p1204_3.generic import VIDEOPARSER_REPO
from p1204_3.utils import run_cmd


def run_videoparser(video_segment_file, output_dir_full_path, skipexisting=True):
    """
    Run video parser on a video, save report to output_dir_full_path
    """
    logging.info("run bitstream parser for {}".format(video_segment_file))
    report_file_name = os.path.join(
        output_dir_full_path,
        os.path.splitext(os.path.basename(video_segment_file))[0] + ".json.bz2",
    )
    if skipexisting and os.path.isfile(report_file_name):
        return report_file_name
    this_path = os.path.dirname(os.path.realpath(__file__))
    parser_shellscript = os.path.join(
        this_path, "bitstream_mode3_videoparser", "parser.sh"
    )
    cmd = [parser_shellscript, video_segment_file, "--output", report_file_name]

    try:
        run_cmd(cmd)
        return report_file_name
    except Exception as e:
        logging.error(f"there was something wrong with {video_segment_file}")
        logging.error(f"please check the following command: \n {cmd}")
        logging.error(f"output: {e}")
        return ""

    return report_file_name


def check_or_install_videoparser():
    """
    Check if videoparser is installed, otherwise install it
    """
    logging.info("check or install video parser")
    this_path = os.path.dirname(os.path.realpath(__file__))
    videoparser_directory = os.path.join(this_path, "bitstream_mode3_videoparser")
    if os.path.isdir(videoparser_directory):
        logging.info("video parser is checked out")
    else:
        logging.info(
            "video parser is not checked out, will clone it, which may take a minute"
        )
        run_cmd(["git", "clone", VIDEOPARSER_REPO, videoparser_directory])
        logging.info("building the video parser, which may take a while")
        run_cmd([f"{videoparser_directory}/build_and_test.sh"])
