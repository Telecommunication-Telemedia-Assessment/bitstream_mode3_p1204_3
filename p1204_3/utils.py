#!/usr/bin/env python3
import os
import sys
import logging
import shutil
import subprocess
import json
import bz2
import gzip


color_codes = {
    "black": "\033[1;30m",
    "red": "\033[1;31m",
    "green": "\033[1;32m",
    "yellow": "\033[1;33m",
    "blue": "\033[1;34m",
    "magenta": "\033[1;35m",
    "cyan": "\033[1;36m",
    "white": "\033[1;37m",
    "end_code": "\033[1;0m",
}


logging.addLevelName(
    logging.CRITICAL, color_codes["red"] + logging.getLevelName(logging.CRITICAL) + color_codes["end_code"]
)
logging.addLevelName(logging.ERROR, color_codes["red"] + logging.getLevelName(logging.ERROR) + color_codes["end_code"])
logging.addLevelName(
    logging.WARNING, color_codes["yellow"] + logging.getLevelName(logging.WARNING) + color_codes["end_code"]
)
logging.addLevelName(logging.INFO, color_codes["green"] + logging.getLevelName(logging.INFO) + color_codes["end_code"])
logging.addLevelName(logging.DEBUG, color_codes["blue"] + logging.getLevelName(logging.DEBUG) + color_codes["end_code"])


def shell_call(call):
    """
    Run a program via system call and return stdout + stderr.
    @param call programm and command line parameter list, e.g shell_call("ls /")
    @return stdout and stderr of programm call
    """
    try:
        output = subprocess.check_output(call, universal_newlines=True, shell=True)
    except Exception as e:
        output = str(e.output)
    return output


def assert_msg(check, fail_message):
    if not check:
        logging.error(fail_message)
        sys.exit(0)


def assert_file(filename, fail_message):
    assert_msg(os.path.isfile(filename), fail_message)


def file_open(filename, mode="r"):
    """ Open a file, and if you add bz2 to filename a compressed file will be opened
    """
    if "bz2" in filename:
        return bz2.open(filename, mode + "t")
    if "gz" in filename:
        return gzip.open(filename, mode + "t")
    return open(filename, mode)


def ffprobe(filename):
    """ run ffprobe to get some information of a given video file
    """
    if shutil.which("ffprobe") is None:
        raise Exception("you need to have ffprobe installed, please read README.md.")

    if not os.path.isfile(filename):
        raise Exception("{} is not a valid file".format(filename))

    cmd = "ffprobe -show_format -select_streams v:0 -show_streams -of json '{filename}' 2>/dev/null".format(
        filename=filename
    )

    res = shell_call(cmd).strip()

    if len(res) == 0:
        raise Exception("{} is somehow not valid, so ffprobe could not extract anything".format(filename))

    res = json.loads(res)

    needed = {
        "pix_fmt": "unknown",
        "bits_per_raw_sample": "unknown",
        "width": "unknown",
        "height": "unknown",
        "avg_frame_rate": "unknown",
        "codec_name": "unknown",
        "profile": "unknown",
    }
    for stream in res["streams"]:
        for n in needed:
            if n in stream:
                needed[n] = stream[n]
                if n == "avg_frame_rate":  # convert framerate to numeric integer value
                    needed[n] = round(eval(needed[n]))
    needed["bitrate"] = res.get("format", {}).get("bit_rate", -1)
    needed["codec"] = needed["codec_name"]
    needed["duration"] = res.get("format", {}).get("duration", 0)
    needed["video_profile"] = needed["profile"]
    return needed


def json_store(outputfile, jsonobject):
    with open(outputfile, "w") as ofp:
        json.dump(jsonobject, ofp, indent=4, sort_keys=True)


def json_load(jsonfile):
    with open(jsonfile) as jfp:
        return json.load(jfp)
