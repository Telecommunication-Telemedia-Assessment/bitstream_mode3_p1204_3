#!/usr/bin/env python3
import os
import sys
import logging
import shutil
import subprocess
import json

from sklearn.externals import joblib


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
    logging.CRITICAL,
    color_codes["red"]
    + logging.getLevelName(logging.CRITICAL)
    + color_codes["end_code"],
)
logging.addLevelName(
    logging.ERROR,
    color_codes["red"] + logging.getLevelName(logging.ERROR) + color_codes["end_code"],
)
logging.addLevelName(
    logging.WARNING,
    color_codes["yellow"]
    + logging.getLevelName(logging.WARNING)
    + color_codes["end_code"],
)
logging.addLevelName(
    logging.INFO,
    color_codes["green"] + logging.getLevelName(logging.INFO) + color_codes["end_code"],
)
logging.addLevelName(
    logging.DEBUG,
    color_codes["blue"] + logging.getLevelName(logging.DEBUG) + color_codes["end_code"],
)


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


def ffprobe(filename):
    """ run ffprobe to get some information of a given video file
    """
    if shutil.which("ffprobe") is None:
        raise Exception("you need to have ffprobe installed, please read README.md.")

    if not os.path.isfile(filename):
        raise Exception("{} is not a valid file".format(filename))

    cmd = "ffprobe -show_format -select_streams v:0 -show_streams -of json '{filename}' 2>/dev/null".format(filename=filename)

    res = shell_call(cmd).strip()

    if len(res) == 0:
        raise Exception("{} is somehow not valid, so ffprobe could not extract anything".format(filename))

    res = json.loads(res)

    needed = {"pix_fmt": "unknown",
              "bits_per_raw_sample": "unknown",
              "width": "unknown",
              "height": "unknown",
              "avg_frame_rate": "unknown",
              "codec_name": "unknown"
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

    return needed


def map_to_45(x):
    """
    (y-y1)/(x-x1) = (y2-y1)/(x2-x1) ---> x1 = 1, x2 = 5, y1 = 1, y2 = 4.5

    output = output_start + ((output_end - output_start) / (input_end - input_start)) * (input - input_start)

    """

    input_start = 1
    input_end = 5
    output_start = 1
    output_end = 4.5

    if x >= 5:
        return 4.5

    return output_start + ((output_end - output_start) / (input_end - input_start)) * (x - input_start)

def map_to_5(x):
    """
    (y-y1)/(x-x1) = (y2-y1)/(x2-x1) ---> x1 = 1, x2 = 4.5, y1 = 1, y2 = 5

    output = output_start + ((output_end - output_start) / (input_end - input_start)) * (input - input_start)

    """

    input_start = 1
    input_end = 4.5
    output_start = 1
    output_end = 5

    if x >= 4.5:
        return 5

    return output_start + ((output_end - output_start) / (input_end - input_start)) * (x - input_start)


def load_serialized(filename_with_path):
    """ load a serialized model """
    if not os.path.isfile(filename_with_path):
        print("{} is not a valid file, please check".format(filename_with_path))
        return
    return joblib.load(filename_with_path)


def binarize_column(dataframe, column, prefix=""):
    """
    add separate binarized columns to a given dataframe for each uniqe value of column
    """
    values = dataframe[column].unique()
    for value in values:
        dataframe[prefix + value] = dataframe[column].map(lambda x: 1 if  x == value else 0)
    return dataframe


def load_dict_values(dataframe, column):
    """
    load values that are nested as a dictionary for a specific column
    """
    if column not in dataframe.columns:
        return dataframe
    _values = list(dataframe[column].apply(lambda x: json.loads(x) if type(x) == str else x).values)
    _values = pd.DataFrame(_values)

    for x in _values.columns:
        dataframe[column + "_" + x] = _values[x].values

    return dataframe
