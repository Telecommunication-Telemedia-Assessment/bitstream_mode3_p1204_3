#!/usr/bin/env python3
import logging
import json
import os
import datetime

from p1204_3.utils import assert_file
from p1204_3.utils import assert_msg
from p1204_3.utils import ffprobe
from p1204_3.utils import json_load
from p1204_3.modelutils import map_to_45
from p1204_3.modelutils import map_to_5
from p1204_3.modelutils import r_from_mos
from p1204_3.modelutils import mos_from_r
from p1204_3.modelutils import load_serialized
from p1204_3.modelutils import binarize_column
from p1204_3.modelutils import load_dict_values
from p1204_3.modelutils import per_sample_interval_function
from p1204_3.generic import *
from p1204_3.videoparser import *

import p1204_3.features as features
from p1204_3.features import *


class P1204BitstreamMode3:
    """
    ITU-T P.1204.3 short term video quality prediction model
    """

    def __init__(self):
        self.display_res = 3840 * 2160

    def _calculate(self, prediction_features, params, rf_model, display_res, device_type):
        def mos_q_baseline_pc(features, a, b, c, d):
            quant = features["quant"]
            mos_q = a + b * np.exp(c * quant + d)
            mos_q = np.clip(mos_q, 1, 5)
            mos_q = np.vectorize(r_from_mos)(mos_q)
            cod_deg = 100 - mos_q
            cod_deg = np.clip(cod_deg, 0, 100)
            return cod_deg

        prediction_features = prediction_features.copy()

        prediction_features = load_dict_values(prediction_features, "QPValuesStatsPerGop")
        prediction_features = load_dict_values(prediction_features, "QPstatspersecond")
        prediction_features = load_dict_values(prediction_features, "BitstreamStatFeatures")
        prediction_features = load_dict_values(prediction_features, "FramesizeStatsPerGop")
        prediction_features = load_dict_values(prediction_features, "AvMotionStatsPerGop")

        prediction_features["quant"] = prediction_features["QPValuesStatsPerGop_mean_Av_QPBB_non-i"]

        def video_codec_extension(row):
            if row["Codec"] == "h264" and row["BitDepth"] == 10:
                return "h264_10bit"
            if row["Codec"] == "hevc" and row["BitDepth"] == 10:
                return "hevc_10bit"
            return row["Codec"]

        prediction_features["video_codec"] = prediction_features.apply(video_codec_extension, axis=1)

        def norm_qp(row):
            qp_norm_coeffs = {"h264": 51, "h264_10bit": 63, "hevc": 51, "hevc_10bit": 63, "vp9": 255}
            if not row["video_codec"] in qp_norm_coeffs:
                return -1
            return row["QPValuesStatsPerGop_mean_Av_QPBB_non-i"] / qp_norm_coeffs[row["video_codec"]]

        prediction_features["quant"] = prediction_features[
            ["video_codec", "QPValuesStatsPerGop_mean_Av_QPBB_non-i"]
        ].apply(norm_qp, axis=1)

        prediction_features = binarize_column(prediction_features, "video_codec")

        codecs = prediction_features["video_codec"].unique()

        cod_deg = sum(
            [
                prediction_features[c]
                * mos_q_baseline_pc(
                    prediction_features, params[c + "_a"], params[c + "_b"], params[c + "_c"], params[c + "_d"]
                )
                for c in codecs
            ]
        )

        # upscaling degradation
        resolution = params["x"] * np.log(params["y"] * (prediction_features["Resolution"] / display_res))
        resolution = np.clip(resolution, 0, 100)

        # temporal degradation
        framerate = params["z"] * np.log(params["k"] * prediction_features["Framerate"] / 60)
        framerate = np.clip(framerate, 0, 100)

        # parametric part - core model
        pred = 100 - (cod_deg + resolution + framerate)
        pred = np.vectorize(mos_from_r)(pred)
        pred = np.clip(pred, 1, 5)
        initial_predicted_score = np.vectorize(map_to_5)(pred)
        prediction_features["predicted_mos_mode3_baseline"] = initial_predicted_score

        # now the RF model will be loaded and features are prepared
        residual_rf_model = load_serialized(rf_model)

        prediction_features_rf = prediction_features.copy()

        possible_codecs = ["h264", "h264_10bit", "hevc", "hevc_10bit", "vp9"]
        for codec in possible_codecs:
            prediction_features_rf[codec] = prediction_features_rf["video_codec"].apply(
                lambda x: 1 if x == codec else 0
            )

        prediction_features_rf = prediction_features_rf.rename(
            columns={
                "FramesizeStatsPerGop_1.0_quantil_FrameSize": "1.0_quantil_FrameSize",
                "FramesizeStatsPerGop_std_FrameSize_non-i": "std_FrameSize_non-i",
                "FramesizeStatsPerGop_kurtosis_FrameSize_non-i": "kurtosis_FrameSize_non-i",
                "QPValuesStatsPerGop_mean_Av_QPBB_non-i": "mean_Av_QPBB_non_i",
                "QPValuesStatsPerGop_iqr_Av_QPBB_non-i": "iqr_Av_QPBB_non-i",
                "QPValuesStatsPerGop_kurtosis_Av_QPBB_non-i": "kurtosis_Av_QPBB_non-i",
                "QPValuesStatsPerGop_iqr_min_QP": "iqr_min_QP",
                "QPValuesStatsPerGop_std_max_QP_non-i": "std_max_QP_non-i",
                "AvMotionStatsPerGop_kurtosis_Av_Motion": "kurtosis_Av_Motion",
                "AvMotionStatsPerGop_0.0_quantil_StdDev_MotionX_non-i": "0.0_quantil_StdDev_MotionX_non-i",
            }
        )

        feature_columns = list(
            set(
                [
                    "Bitrate",
                    "Resolution",
                    "Framerate",
                    "mean_Av_QPBB_non_i",
                    "predicted_mos_mode3_baseline",
                    "quant",
                    "1.0_quantil_FrameSize",
                    "kurtosis_Av_Motion",
                    "iqr_Av_QPBB_non-i",
                    "kurtosis_FrameSize_non-i",
                    "std_FrameSize_non-i",
                    "kurtosis_Av_QPBB_non-i",
                    "iqr_min_QP",
                    "0.0_quantil_StdDev_MotionX_non-i",
                    "std_max_QP_non-i",
                ]
                + possible_codecs
            )
        )
        feature_columns = sorted(feature_columns)

        prediction_features_rf = prediction_features_rf[feature_columns]
        prediction_features_rf = prediction_features_rf.fillna(0)
        residual_mos = residual_rf_model.predict(prediction_features_rf)

        predicted_score = np.vectorize(map_to_5)(pred)
        predicted_score = predicted_score + residual_mos
        predicted_score = np.clip(predicted_score, 1, 5)
        prediction_features_rf["rf_pred"] = predicted_score

        w = 0.5
        final_pred = (
            w * prediction_features_rf["predicted_mos_mode3_baseline"] + (1 - w) * prediction_features_rf["rf_pred"]
        )
        return {
            "final_pred": final_pred,
            "baseline": prediction_features_rf["predicted_mos_mode3_baseline"],
            "coding_deg": cod_deg,
            "upscaling_deg": resolution,
            "temporal_deg": framerate,
            "rf_pred": prediction_features_rf["rf_pred"],
        }

    def features_used(self):
        return [
            features.Bitrate,
            features.Framerate,
            features.Resolution,
            features.Codec,
            features.QPValuesStatsPerGop,
            features.BitDepth,
            features.QPstatspersecond,
            features.FramesizeStatsPerGop,
            features.AvMotionStatsPerGop,
        ]

    def predict_quality(
        self,
        videofilename,
        model_config_filename,
        device_type="pc",
        device_resolution="3840x2160",
        viewing_distance="1.5xH",
        display_size=55,
        temporary_folder="tmp",
    ):

        assert_file(videofilename, f"{videofilename} does not exist, please check")
        assert_file(model_config_filename, f"{model_config_filename} does not exist, please check")

        device_type = device_type.lower()
        assert_msg(
            device_type in DEVICE_TYPES,
            f"specified device_type '{device_type}' is not supported, only {DEVICE_TYPES} possible",
        )
        assert_msg(
            device_resolution in DEVICE_RESOLUTIONS,
            f"specified device_resolution '{device_resolution}' is not supported, only {DEVICE_RESOLUTIONS} possible",
        )
        assert_msg(
            viewing_distance in VIEWING_DISTANCES,
            f"specified viewing_distance '{viewing_distance}' is not supported, only {VIEWING_DISTANCES} possible",
        )
        assert_msg(
            display_size in DISPLAY_SIZES,
            f"specified display_size '{display_size}' is not supported, only {DISPLAY_SIZES} possible",
        )

        ffprobe_result = ffprobe(videofilename)
        assert_msg(
            ffprobe_result["codec"] in CODECS_SUPPORTED,
            f"your video codec is not supported by the model: {ffprobe_result['codec']}",
        )

        model_config = json_load(model_config_filename)

        device_type = "pc" if device_type in ["pc", "tv"] else "mobile"

        # select only the required config for the device type
        model_config = model_config[device_type]

        # assume the RF model part is locally stored in the path of model_config_filename
        rf_model = os.path.join(os.path.dirname(model_config_filename), model_config["rf"])

        # load parametetric model coefficients
        model_coefficients = model_config["params"]

        display_res = float(device_resolution.split("x")[0]) * float(device_resolution.split("x")[1])

        self.display_res = display_res

        check_or_install_videoparser()
        os.makedirs(temporary_folder, exist_ok=True)

        feature_cache = os.path.join(
            temporary_folder, os.path.splitext(os.path.basename(videofilename))[0] + "_feat.pkl"
        )
        logging.info(f"use feature cache file {feature_cache}")
        if not os.path.isfile(feature_cache):
            # run bitstream parser
            bitstream_parser_result_file = run_videoparser(videofilename, temporary_folder)
            if bitstream_parser_result_file == "":
                logging.error(f"no bitstream stats file for {videofilename}")
                return {}

            # calculate features
            features = pd.DataFrame(
                [extract_features(videofilename, self.features_used(), ffprobe_result, bitstream_parser_result_file)]
            )
            features.to_pickle(feature_cache)
        else:
            logging.info("features are already cached, extraction skipped")
            features = pd.read_pickle(feature_cache)

        logging.info("features extracted")

        per_sequence = self._calculate(features, model_coefficients, rf_model, display_res, device_type)

        per_second = per_sample_interval_function(per_sequence["final_pred"], features)
        return {
            "video_full_path": videofilename,
            "video_basename": os.path.basename(videofilename),
            "per_second": [float(x) for x in per_second],
            "per_sequence": float(per_sequence["final_pred"].values[0]),
            "debug": {
                "baseline": float(per_sequence["baseline"].values[0]),
                "coding_deg": float(per_sequence["coding_deg"].values[0]),
                "upscaling_deg": float(per_sequence["upscaling_deg"].values[0]),
                "temporal_deg": float(per_sequence["temporal_deg"].values[0]),
                "rf_pred": float(per_sequence["rf_pred"].values[0]),
            },
            "date": str(datetime.datetime.now()),
        }
