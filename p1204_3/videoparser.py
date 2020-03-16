#!/usr/bin/env python3
import os
import sys
import logging

from p1204_3.generic import *
from p1204_3.utils import file_open


def run_videoparser(video_seqment_file, output_dir_full_path, skipexisting=True):
    """
    Run video parser on a video, save report to output_dir_full_path
    """
    logging.info("run bitstream parser for {}".format(video_seqment_file))
    report_file_name = output_dir_full_path + "/" + os.path.splitext(os.path.basename(video_seqment_file))[0] + ".json.bz2"
    if skipexisting and os.path.isfile(report_file_name):
        return report_file_name
    this_path = os.path.dirname(os.path.realpath(__file__))
    cmd = this_path + """/bitstream_mode3_videoparser/parser.sh "{video}" --output "{report}" """.format(video=video_seqment_file, report=report_file_name)
    ret = os.system(cmd)
    if ret != 0:
        logging.error(f"there was something wrong with {video_seqment_file}")
        logging.error(f"please check the following command: \n {cmd}")
        return ""
    return report_file_name


def check_or_install_videoparser():
    """
    Check if videoparser is installed, otherwise install it
    """
    logging.info("check or install video parser")
    this_path = os.path.dirname(os.path.realpath(__file__))
    videoparser_directory = f"{this_path}/bitstream_mode3_videoparser"
    if os.path.isdir(videoparser_directory):
        logging.info("video parser is checked out")
        return
    os.system(f"git clone {VIDEOPARSER_REPO} {videoparser_directory}")
    os.system(f"{videoparser_directory}/build_and_test.sh")


