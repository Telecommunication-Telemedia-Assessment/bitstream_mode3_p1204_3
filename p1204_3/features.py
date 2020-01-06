#!/usr/bin/env python3
import numpy as np
import pandas as pd
from p1204_3.utils import assert_msg

# ffprobe related features

class Bitrate:
    """
    Average video bitrate
    """
    def calculate(self, processed_video_sequence):
        if hasattr(processed_video_sequence, "_ffprobe_result"):
            bitrate = processed_video_sequence._ffprobe_result["bitrate"]
            return float(bitrate)  # TODO: check UNIT of this value!!
        assert_msg(False, "this should not happen")

class Framerate:
    """
    video framerate
    """
    def calculate(self, processed_video_sequence):
        if hasattr(processed_video_sequence, "_ffprobe_result"):
            fps = processed_video_sequence._ffprobe_result["avg_frame_rate"]
            if fps != "unknown":
                return float(fps)
            return 60.0
        assert_msg(False, "this should not happen")


class Resolution:
    """
    Average resolution in pixels (width * height)
    # FIXME: check
    """
    def calculate(self, processed_video_sequence):
        if hasattr(processed_video_sequence, "_ffprobe_result"):
            height = processed_video_sequence._ffprobe_result["height"]
            width = processed_video_sequence._ffprobe_result["width"]
            return width * height
        assert_msg(False, "this should not happen")


class Codec:
    """
    Video codec used, either h264, h265, vp9.
    This assumes that the codec will not change over the sequence.
    """
    def calculate(self, processed_video_sequence):
        if hasattr(processed_video_sequence, "_ffprobe_result"):
            codec = processed_video_sequence._ffprobe_result["codec"]
            return codec
        assert_msg(False, "this should not happen")


class Duration:
    """
    Average video duration over all segments in s
    """
    def calculate(self, processed_video_sequence):
        if hasattr(processed_video_sequence, "_ffprobe_result"):
            duration = processed_video_sequence._ffprobe_result["duration"]
            return duration
        assert_msg(False, "this should not happen")


# bitstream parser related features
def by_gop(processed_video_sequence, columns=[], select_element=None):
    """
    a gop iterator for bitstreamstats,
    only select the specified columns,
    if select_element != None then for ALL columns (that are vector values) only the `select_element` is handled

    one bitstream frame has the follwing keys:
    dict_keys(['FirstFrame',
     'SKIP_mb_ratio',
     'Av_MotionX',
     'PredFrm_Intra',
     'NumFrames',
     'StdDev_MotionY',
     'IsIDR',
     'DTS',
     'StdDev_MotionDif',
     'Av_QP',
     'FrameSize',
     'Av_Coefs',
     'StdDev_Coefs',
     'Av_MotionDif',
     'HF_LF_ratio',
     'TrShapes',
     'StdDev_QPBB',
     'FrameCnt',
     'max_QP',
     'InitialQP',
     'Av_Motion',
     'min_QP',
     'SpatialComplexety',
     'StdDev_Motion',
     'StdDev_QP',
     'PTS',
     'FrameType',
     'Av_MotionY',
     'Av_QPBB',
     'Seq',
     'AnalyzedMBs',
     'FarFWDRef',
     'TemporalComplexety',
     'CurrPOC',
     'FrameIdx',
     'StdDev_MotionX',
     'BlackBorder',
     'MbQPs',
     'BlkShapes',
     'MbTypes'])
    """
    gop = []
    for f in processed_video_sequence.get_frames_from_bitstream_stats():
        if f["IsIDR"] == 1 and gop != []:
            yield gop
            gop = []
        # filter out the selected columns
        if columns != []:
            if select_element is None:
                f = {x: f[x] for x in list(set(columns) & set(f.keys()))}
            else:
                f = {x: f[x][select_element] if type(f[x]) == list else f[x] for x in list(set(columns) & set(f.keys()))}
        gop.append(f)
    yield gop




class QPValuesStatsPerGop:
    """
    Calculate several features based on QPValues
        per GOP
    """
    def calculate(self, processed_video_sequence):
        logger.debug("calculate average qp gop based for {}".format(processed_video_sequence))
        needed = ["Av_QP", "Av_QPBB", "max_QP", "min_QP"]
        results = []
        for gop in by_gop(processed_video_sequence, columns=needed + ["FrameType"]):
            df = pd.DataFrame(gop)
            gop_res = {}
            for x in needed:
                gop_res["mean_" + x] = df[x].mean()
                gop_res["median_" + x] = df[x].median()
                gop_res["std_" + x] = df[x].std()
                gop_res["skew_" + x] = float(scipy.stats.skew(df[x]))
                gop_res["kurtosis_" + x] = float(scipy.stats.kurtosis(df[x]))
                gop_res["iqr_" + x] = float(scipy.stats.iqr(df[x]))

                for i in range(11):
                    quantile = round(0.1 * i, 1)
                    gop_res["{}_quantil_{}".format(quantile,x)] = float(df[x].quantile(quantile))
            # select non-iframes
            df = df[df["FrameType"] != 1]
            for x in needed:
                gop_res["mean_" + x + "_non-i"] = df[x].mean()
                gop_res["median_" + x + "_non-i"] = df[x].median()
                gop_res["std_" + x + "_non-i"] = df[x].std()
                gop_res["skew_" + x + "_non-i"] = float(scipy.stats.skew(df[x]))
                gop_res["kurtosis_" + x + "_non-i"] = float(scipy.stats.kurtosis(df[x]))
                gop_res["iqr_" + x + "_non-i"] = float(scipy.stats.iqr(df[x]))

                for i in range(11):
                    quantile = round(0.1 * i, 1)
                    gop_res["{}_quantil_{}_non-i".format(quantile,x)] = float(df[x].quantile(quantile))

            results.append(gop_res)
        df = pd.DataFrame(results)
        result = df.mean().to_dict()
        logger.debug("estimated qp feature values: {}".format(result))
        return result




class BitDepth:
    """ extracts bitdepth for a given video
    """
    def calculate(self, processed_video_sequence):
        for frame in processed_video_sequence.get_frames_from_bitstream_stats():
            bitdepth = frame["Seq"]["BitDepth"]
            break
        tmp = processed_video_sequence.get_segments_from_qchanges()[0]
        codec = tmp["video_codec"]
        if codec == "vp9" and bitdepth == 0:
            # TODO: fix to recognize correct BitDepth of vp9
            bitdepth = 8 if tmp["video_profile"] < 2 else 10
        return bitdepth



class QPstatspersecond:
    """
        Calculate several features based on SpatialComplexety
        per GOP
    """
    def calculate(self, processed_video_sequence):
        logger.debug("calculate Blockiness based for {}".format(processed_video_sequence))
        needed = ["Av_QPBB"]
        results = []
        gop_res = {}
        qp_list = []
        qp_list_non_i = []
        fr_type_list = []

        segments = processed_video_sequence.get_segments_from_qchanges()
        framerate =  np.mean([s["video_frame_rate"] for s in segments])

        #print(framerate)

        for frame in processed_video_sequence.get_frames_from_bitstream_stats():
            f = frame["Av_QPBB"]
            fr_type = frame["FrameType"]

            # print(fr_type)

            qp_list.append(f)
            fr_type_list.append(fr_type)

            if fr_type != 1:
                qp_list_non_i.append(f)

        # print(len(qp_list))
        frames_per_sec = np.arange(0, len(qp_list)+1, framerate)
        frames_per_sec = list(frames_per_sec)
        # frames_per_sec.append(len(qp_list) - 1)
        # print(framerate)
        # print(len(qp_list))
        # print(frames_per_sec)

        for i in range(0, len(frames_per_sec) - 1):
            # print("i = {}".format(i))
            # print(frames_per_sec[i+1])
            start = np.int(frames_per_sec[i])
            end = np.int(frames_per_sec[i+1])
            qp_per_sec = qp_list[start:end]
            fr_type_per_frame = fr_type_list[start:end]
            qp_per_sec_non_i = qp_per_sec.copy()

            if (1 in fr_type_per_frame):
                i_frame_indices = fr_type_per_frame.index(1)
            else:
                i_frame_indices = -1

            # print("i frame index = {}".format(i_frame_indices))

            if i_frame_indices >= 0:
                # print("There is an i frame in this second")
                # remove_val = qp_per_sec_non_i[i_frame_indices]
                value = qp_per_sec_non_i.pop(i_frame_indices)
                # print("remove value = {}".format(value))
            else:
                qp_per_sec_non_i = qp_per_sec_non_i


            # print("all frames per sec : {}".format(qp_per_sec))
            # print("len of frames per sec {}".format(len(qp_per_sec)))
            # print("only non-i frames per sec: {}".format(qp_per_sec_non_i))
            # print("len of frames per sec {}".format(len(qp_per_sec_non_i)))
            # print(fr_type_per_frame)

            gop_res["mean_qpbb_non_i_" + str(i) + "_sec"] = np.mean(qp_per_sec_non_i)
            gop_res["mean_qpbb_all_frames_" + str(i) + "_sec"] = np.mean(qp_per_sec)

            gop_res["median_qpbb_non_i_" + str(i) + "_sec"] = np.median(qp_per_sec_non_i)
            gop_res["median_qpbb_all_frames_" + str(i) + "_sec"] = np.median(qp_per_sec)

            gop_res["std_qpbb_non_i_" + str(i) + "_sec"] = np.std(qp_per_sec_non_i)
            gop_res["std_qpbb_all_frames_" + str(i) + "_sec"] = np.std(qp_per_sec)

            gop_res["iqr_qpbb_non_i_" + str(i) + "_sec"] = scipy.stats.iqr(qp_per_sec_non_i)
            gop_res["iqr_qpbb_all_frames_" + str(i) + "_sec"] = scipy.stats.iqr(qp_per_sec)

            gop_res["kurtosis_qpbb_non_i_" + str(i) + "_sec"] = scipy.stats.kurtosis(qp_per_sec_non_i)
            gop_res["kurtosis_qpbb_all_frames_" + str(i) + "_sec"] = scipy.stats.kurtosis(qp_per_sec)

            gop_res["skew_qpbb_non_i_" + str(i) + "_sec"] = scipy.stats.skew(qp_per_sec_non_i)
            gop_res["skew_qpbb_all_frames_" + str(i) + "_sec"] = scipy.stats.skew(qp_per_sec)

            for i in range(11):
                percentile = round(10 * i, 1)
                dct_key_non_i = str(percentile) + "_qpbb_non_i_" + str(i) + "_sec"
                gop_res[dct_key_non_i] = np.percentile(qp_per_sec_non_i, percentile, axis=0)
                dct_key_all_frames = str(percentile) + "_qpbb_all_frames_" + str(i) + "_sec"
                gop_res[dct_key_all_frames] = np.percentile(qp_per_sec, percentile, axis=0)

        results.append(gop_res)
        # print(gop_res)
        # print(len(blockiness_linear_list))
        df = pd.DataFrame(results)
        # print(df)
        result = gop_res    # df.to_dict() # results # df.to_dict() # df.mean().to_dict()
        # print(result)
        logger.debug("estimated qp stats per second feature values: {}".format(result))
        return result




class BitstreamStatFeatures:
    """
    Calculate several features based on QPValues
        per GOP
    """
    def calculate(self, processed_video_sequence):
        logger.debug("several bitstream features{}".format(processed_video_sequence))

        needed = [
            'AnalyzedMBs',
            'Av_Motion',
            'Av_MotionDif',
            'Av_MotionX',
            'Av_MotionY',
            'Av_QP',
            'Av_QPBB',
            'BlackBorder',
            'FrameSize',
            'FrameType',
            'InitialQP',
            'SKIP_mb_ratio',
            'StdDev_Motion',
            'StdDev_MotionDif',
            'StdDev_MotionX',
            'StdDev_MotionY',
            'StdDev_QP',
            'StdDev_QPBB',
            'max_QP',
            'min_QP',
            'IsIDR',
            'TI_910',
            'SI_910'
        ]
        # additional values needs to be normalized and are array values
        additional = ["MbTypes", "BlkShapes", "TrShapes"]
        """
        double   MbTypes[7] ; // Count for 0=Skipped   1=Forward (L0)   2=Backward (L1)   3=Bidirect    4=Direct    5=Intra(directional)
                              // 6=Intra(planar)  ( H.264:  [5]=always 4x4   /  [6]=always 16x16 )

        double   BlkShapes[9] ; // count for Shapes: 8=64x64    7=64x32,32x64  6=32x32  5=16x32,32x16   4=16x16  3=16x8,8x16  2=8x8
                               // 1=8x4,4x8  0=4x4    (H.264: only 0,1,2,3,4 )
        double   TrShapes[7] ;
        """

        # some other vector values, where normalized is not needed
        # more = ['SpatialComplexety', 'TemporalComplexety', 'TI_Mot', 'Blockiness']
        more = ['SpatialComplexety', 'TemporalComplexety', 'TI_Mot']

        results = []
        for frame in processed_video_sequence.get_frames_from_bitstream_stats():
            f = {x: frame[x] for x in list(set(needed) & set(frame.keys()))}
            for x in additional:
                for i, v in enumerate(frame[x]):
                    f[x + "_" + str(i)] = v / max(1, sum(frame[x]))
            for m in more:
                for i, v in enumerate(frame[m]):
                    f[m + "_" + str(i)] = v
            results.append(f)
        df = pd.DataFrame(results)
        result = {}
        for col in df.columns:
            result = dict(result, **calc_statistical_values(df[col].values, prefix=col + "_"))

        logger.debug("estimated bistream feature values: {}, {} values".format(result, len(result)))
        return result




class FramesizeStatsPerGop:
    """
    Calculate several features based on QPValues
        per GOP
    """
    def calculate(self, processed_video_sequence):
        logger.debug("calculate framesize gop based for {}".format(processed_video_sequence))
        needed = ["FrameSize"]
        results = []
        for gop in by_gop(processed_video_sequence, columns=needed + ["FrameType"]):
            df = pd.DataFrame(gop)
            gop_res = {}
            for x in needed:
                gop_res["mean_" + x] = df[x].mean()
                gop_res["median_" + x] = df[x].median()
                gop_res["std_" + x] = df[x].std()
                gop_res["skew_" + x] = float(scipy.stats.skew(df[x]))
                gop_res["kurtosis_" + x] = float(scipy.stats.kurtosis(df[x]))
                gop_res["iqr_" + x] = float(scipy.stats.iqr(df[x]))

                for i in range(11):
                    quantile = round(0.1 * i, 1)
                    gop_res["{}_quantil_{}".format(quantile,x)] = float(df[x].quantile(quantile))
            # select non-iframes
            df = df[df["FrameType"] != 1]
            for x in needed:
                gop_res["mean_" + x + "_non-i"] = df[x].mean()
                gop_res["median_" + x + "_non-i"] = df[x].median()
                gop_res["std_" + x + "_non-i"] = df[x].std()
                gop_res["skew_" + x + "_non-i"] = float(scipy.stats.skew(df[x]))
                gop_res["kurtosis_" + x + "_non-i"] = float(scipy.stats.kurtosis(df[x]))
                gop_res["iqr_" + x + "_non-i"] = float(scipy.stats.iqr(df[x]))

                for i in range(11):
                    quantile = round(0.1 * i, 1)
                    gop_res["{}_quantil_{}_non-i".format(quantile,x)] = float(df[x].quantile(quantile))

            results.append(gop_res)
        df = pd.DataFrame(results)
        result = df.mean().to_dict()
        logger.debug("estimated framesize feature values: {}".format(result))
        return result




class AvMotionStatsPerGop:
    """
    Calculate several features based on QPValues
        per GOP
    """
    def calculate(self, processed_video_sequence):
        logger.debug("calculate average motion gop based for {}".format(processed_video_sequence))
        needed = ['Av_Motion', 'Av_MotionDif', 'Av_MotionX', 'Av_MotionY', 'StdDev_Motion', 'StdDev_MotionDif', 'StdDev_MotionX', 'StdDev_MotionY']
        results = []
        for gop in by_gop(processed_video_sequence, columns=needed + ["FrameType"]):
            df = pd.DataFrame(gop)
            gop_res = {}
            for x in needed:
                gop_res["mean_" + x] = df[x].mean()
                gop_res["median_" + x] = df[x].median()
                gop_res["std_" + x] = df[x].std()
                gop_res["skew_" + x] = float(scipy.stats.skew(df[x]))
                gop_res["kurtosis_" + x] = float(scipy.stats.kurtosis(df[x]))
                gop_res["iqr_" + x] = float(scipy.stats.iqr(df[x]))

                for i in range(11):
                    quantile = round(0.1 * i, 1)
                    gop_res["{}_quantil_{}".format(quantile,x)] = float(df[x].quantile(quantile))
            # select non-iframes
            df = df[df["FrameType"] != 1]
            for x in needed:
                gop_res["mean_" + x + "_non-i"] = df[x].mean()
                gop_res["median_" + x + "_non-i"] = df[x].median()
                gop_res["std_" + x + "_non-i"] = df[x].std()
                gop_res["skew_" + x + "_non-i"] = float(scipy.stats.skew(df[x]))
                gop_res["kurtosis_" + x + "_non-i"] = float(scipy.stats.kurtosis(df[x]))
                gop_res["iqr_" + x + "_non-i"] = float(scipy.stats.iqr(df[x]))

                for i in range(11):
                    quantile = round(0.1 * i, 1)
                    gop_res["{}_quantil_{}_non-i".format(quantile,x)] = float(df[x].quantile(quantile))

            results.append(gop_res)
        df = pd.DataFrame(results)
        result = df.mean().to_dict()
        logger.debug("estimated motion feature values: {}".format(result))
        return result

