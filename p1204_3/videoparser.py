#!/usr/bin/env python3
import logging
import os
import sys

from p1204_3.generic import VIDEOPARSER_REPO
from p1204_3.utils import shell_call


def __video_parser_dir():
    this_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(
        this_path,
        "bitstream_mode3_videoparser",
    )


def run_videoparser(
    video_segment_file, temporary_folder, skipexisting=True, use_docker=False
):
    """
    Run video parser on a video, save report to temporary_folder
    """
    logging.info(
        "run bitstream parser for {}, using docker? {}".format(
            video_segment_file, use_docker
        )
    )
    report_file_name = os.path.join(
        temporary_folder,
        os.path.splitext(os.path.basename(video_segment_file))[0] + ".json.bz2",
    )
    if skipexisting and os.path.isfile(report_file_name):
        return report_file_name

    if use_docker:
        video_segment_file_dir = os.path.abspath(os.path.dirname(video_segment_file))
        report_file_name_dir = os.path.abspath(os.path.dirname(report_file_name))
        cmd = f"""docker run --rm -v {video_segment_file_dir}:/tmp -v {report_file_name_dir}:/reports videoparser /tmp/{os.path.basename(video_segment_file)} --output /reports/{os.path.basename(report_file_name)}"""
        ret = shell_call(cmd, stream_output=True)
        if "error" in ret.lower():
            logging.error(f"there was something wrong with {video_segment_file}")
            logging.error(f"please check the following command: \n {cmd}")
            return ""
    else:
        parser_script = os.path.join(__video_parser_dir(), "parser.sh")
        cmd = (
            f"""{parser_script} "{video_segment_file}" --output "{report_file_name}" """
        )
        ret = os.system(cmd)
        if ret != 0:
            logging.error(f"there was something wrong with {video_segment_file}")
            logging.error(f"please check the following command: \n {cmd}")
            return ""
    return report_file_name


def check_or_install_videoparser(use_docker=False):
    """
    Check if videoparser is installed, otherwise install it
    """
    if use_docker:
        logging.info("Checking for videoparser Docker image")
        cmd = "docker image inspect videoparser >/dev/null 2>&1"
        ret = os.system(cmd)
        if ret != 0:
            logging.error(
                "videoparser Docker image not found. Please build or pull the image. "
                "See the README in https://github.com/Telecommunication-Telemedia-Assessment/bitstream_mode3_videoparser for more details."
            )
            sys.exit(1)
        logging.info("'videoparser' Docker image found")
        return

    logging.info("check or install video parser")
    videoparser_directory = __video_parser_dir()

    if os.path.isdir(videoparser_directory):
        logging.info("video parser is checked out")
        # perform update for "main part", TODO: think about a better handling, in case we change c++ parts of the parser, maybe as a separate python module?
        # os.system(f"cd {videoparser_directory} && git pull origin master")
        if os.path.isfile(
            os.path.join(videoparser_directory, "VideoParser", "libvideoparser.so")
        ):
            logging.info("video parser is build")
            return
        logging.error("video parser is not build correctly, please check")
        return

    logging.info("clone and build video parser, this will take some time")
    os.system(f"git clone {VIDEOPARSER_REPO} {videoparser_directory}")
    os.system(os.path.join(videoparser_directory, "build.sh"))
