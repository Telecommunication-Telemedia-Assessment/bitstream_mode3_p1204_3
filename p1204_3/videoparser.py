#!/usr/bin/env python3
import os
import sys
import logging

from p1204_3.generic import VIDEOPARSER_REPO


def __video_parser_dir():
    this_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(
        this_path,
        "bitstream_mode3_videoparser",
    )


def run_videoparser(video_segment_file, output_dir_full_path, skipexisting=True):
    """
    Run video parser on a video, save report to output_dir_full_path
    """
    logging.info("run bitstream parser for {}".format(video_segment_file))
    report_file_name = os.path.join(
        output_dir_full_path,
        os.path.splitext(os.path.basename(video_segment_file))[0] + ".json.bz2"
    )
    if skipexisting and os.path.isfile(report_file_name):
        return report_file_name

    parser_script = os.path.join(
        __video_parser_dir(),
        "parser.sh"
    )

    cmd = f"""{parser_script} "{video_segment_file}" --output "{report_file_name}" """
    ret = os.system(cmd)
    if ret != 0:
        logging.error(f"there was something wrong with {video_segment_file}")
        logging.error(f"please check the following command: \n {cmd}")
        return ""
    return report_file_name


def check_or_install_videoparser():
    """
    Check if videoparser is installed, otherwise install it
    """
    logging.info("check or install video parser")
    videoparser_directory = __video_parser_dir()

    if os.path.isdir(videoparser_directory):
        logging.info("video parser is checked out")
        # perform update for "main part", TODO: think about a better handling, in case we change c++ parts of the parser, maybe as a separate python module?
        #os.system(f"cd {videoparser_directory} && git pull origin master")
        if os.path.isfile(
            os.path.join(
                videoparser_directory,
                "VideoParser",
                "libvideoparser.so"
                )
            ):
            logging.info("video parser is build")
            return
        logging.error("video parser is not build correctly, please check")
        return

    logging.info("clone and build video parser, this will take some time")
    os.system(f"git clone {VIDEOPARSER_REPO} {videoparser_directory}")
    os.system(os.path.join(videoparser_directory, "build.sh"))

