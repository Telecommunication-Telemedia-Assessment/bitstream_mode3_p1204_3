#!/usr/bin/env python3
import logging
import json

import numpy as np
import pandas as pd
import scipy.stats

from p1204_3.utils import assert_msg
from p1204_3.utils import file_open
from p1204_3.modelutils import stats_per_gop


def extract_features(videofilename, used_features, ffprobe_result, bitstream_parser_result_file):
    """ extract all specified features for a given video file """
    features = {}
    pvs = PVS(videofilename, ffprobe_result, bitstream_parser_result_file)
    for f in used_features:
        features[str(f.__name__)] = f().calculate(pvs)
    features["duration"] = Duration().calculate(pvs)
    features["videofilename"] = videofilename
    return features


class PVS:
    """ Wrapper to access ffprobe / bitstream statistics internally """

    def __init__(self, videofilename, ffprobe_result, bitstream_parser_result_file):
        self._videofilename = videofilename
        self._ffprobe_result = ffprobe_result
        self._bitstream_parser_result_file = bitstream_parser_result_file

    def get_frames_from_bitstream_stats(self):
        bitstream_stats = {}
        with file_open(self._bitstream_parser_result_file) as bitstat:
            bitstream_stats = json.load(bitstat)

        return bitstream_stats

    def __str__(self):
        return self._videofilename


class Bitrate:
    """
    Average video bitrate
    """

    def calculate(self, processed_video_sequence):
        bitrate = processed_video_sequence._ffprobe_result["bitrate"]
        return float(bitrate) / 1024


class Framerate:
    """
    Video framerate
    """

    def calculate(self, processed_video_sequence):
        fps = processed_video_sequence._ffprobe_result["avg_frame_rate"]
        if fps != "unknown":
            return float(fps)
        return 60.0


class Resolution:
    """
    Resolution in pixels (width * height)
    """

    def calculate(self, processed_video_sequence):
        height = processed_video_sequence._ffprobe_result["height"]
        width = processed_video_sequence._ffprobe_result["width"]
        return width * height


class Codec:
    """
    Video codec used, either h264, hevc, vp9.
    """

    def calculate(self, processed_video_sequence):
        codec = processed_video_sequence._ffprobe_result["codec"]
        return codec


class Duration:
    """
    Video duration in seconds.
    """

    def calculate(self, processed_video_sequence):
        duration = processed_video_sequence._ffprobe_result["duration"]
        return float(duration)


class BitDepth:
    """ Extracts bitdepth for a given video
    """

    def calculate(self, processed_video_sequence):
        # TODO: maybe simpler possible?
        bitdepth = 8  # fallback
        for frame in processed_video_sequence.get_frames_from_bitstream_stats():
            bitdepth = frame["Seq"]["BitDepth"]
            break
        return bitdepth


class FramesizeStatsPerGop:
    """
    Calculate Framesize statistics per GOP
    """

    def calculate(self, processed_video_sequence):
        needed = ["FrameSize"]
        return stats_per_gop(processed_video_sequence, needed)


class QPValuesStatsPerGop:
    """
    Calculate several features based on QPValues per GOP
    """

    def calculate(self, processed_video_sequence):
        needed = ["Av_QP", "Av_QPBB", "max_QP", "min_QP"]
        return stats_per_gop(processed_video_sequence, needed)


class AvMotionStatsPerGop:
    """
    Calculate motion statistics per GOP
    """

    def calculate(self, processed_video_sequence):
        needed = [
            "Av_Motion",
            "Av_MotionDif",
            "Av_MotionX",
            "Av_MotionY",
            "StdDev_Motion",
            "StdDev_MotionDif",
            "StdDev_MotionX",
            "StdDev_MotionY",
        ]
        return stats_per_gop(processed_video_sequence, needed)


class QPstatspersecond:
    """
        Calculate qp values per video second
    """

    def calculate(self, processed_video_sequence):
        logging.debug("calculate QPstatspersecond based for {}".format(processed_video_sequence))
        results = []
        gop_res = {}
        qp_list = []
        qp_list_non_i = []
        fr_type_list = []

        framerate = Framerate().calculate(processed_video_sequence)

        # print(framerate)

        for frame in processed_video_sequence.get_frames_from_bitstream_stats():
            f = frame["Av_QPBB"]
            fr_type = frame["FrameType"]

            # print(fr_type)

            qp_list.append(f)
            fr_type_list.append(fr_type)

            if fr_type != 1:
                qp_list_non_i.append(f)

        frames_per_sec = np.arange(0, len(qp_list) + 1, framerate)
        frames_per_sec = list(frames_per_sec)

        for i in range(0, len(frames_per_sec) - 1):
            start = np.int(frames_per_sec[i])
            end = np.int(frames_per_sec[i + 1])
            qp_per_sec = qp_list[start:end]
            fr_type_per_frame = fr_type_list[start:end]
            qp_per_sec_non_i = qp_per_sec.copy()

            if 1 in fr_type_per_frame:
                i_frame_indices = fr_type_per_frame.index(1)
            else:
                i_frame_indices = -1

            if i_frame_indices >= 0:
                # print("There is an i frame in this second")
                value = qp_per_sec_non_i.pop(i_frame_indices)
            else:
                qp_per_sec_non_i = qp_per_sec_non_i

            gop_res["mean_qpbb_non_i_" + str(i) + "_sec"] = np.mean(qp_per_sec_non_i)

        results.append(gop_res)
        df = pd.DataFrame(results)
        result = gop_res
        logging.debug("estimated qp stats per second feature values: {}".format(result))
        return result
