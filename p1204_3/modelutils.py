#!/usr/bin/env python3
import os
import json
import logging
import inspect

import pandas as pd
import numpy as np
import scipy.stats

from p1204_3.sklearn_tree_deserializing import deserialize_random_forest_regressor_json

from p1204_3.utils import json_load

# deactivate black formatter for lookup tables
# fmt: off
MOS_MAX = 4.9
MOS_MIN = 1.05
R_FROM_MOS_KEYS = [1.05, 1.050214703125, 1.051169875, 1.052255859375, 1.0534720000000002, 1.054817640625, 1.0562921250000001, 1.0578947968749999, 1.059625, 1.061482078125, 1.0634653750000003, 1.065574234375, 1.067808, 1.0701660156250001, 1.072647625, 1.075252171875, 1.077979, 1.0808274531250002, 1.083796875, 1.086886609375, 1.0900960000000002, 1.093424390625, 1.096871125, 1.100435546875, 1.104117, 1.1079148281250002, 1.111828375, 1.1158569843750001, 1.12, 1.124256765625, 1.128626625, 1.1331089218750001, 1.1377030000000001, 1.1424082031250002, 1.147223875, 1.152149359375, 1.157184, 1.1623271406250002, 1.167578125, 1.1729362968750001, 1.178401, 1.1839715781250002, 1.189647375, 1.1954277343750002, 1.201312, 1.2072995156250002, 1.2133896250000002, 1.219581671875, 1.2258750000000003, 1.2322689531250002, 1.2387628750000002, 1.2453561093750003, 1.2520480000000003, 1.2588378906250002, 1.2657251250000001, 1.2727090468750002, 1.279789, 1.286964328125, 1.2942343750000003, 1.3015984843750001, 1.309056, 1.3166062656250002, 1.324248625, 1.331982421875, 1.339807, 1.347721703125, 1.3557258750000003, 1.363818859375, 1.3720000000000003, 1.380268640625, 1.3886241250000002, 1.3970657968750002, 1.4055930000000003, 1.414205078125, 1.4229013750000004, 1.431681234375, 1.4405440000000003, 1.449489015625, 1.4585156250000002, 1.4676231718750001, 1.476811, 1.4860784531250002, 1.4954248750000003, 1.5048496093750003, 1.5143520000000001, 1.5239313906250003, 1.5335871250000002, 1.5433185468750004, 1.553125, 1.5630058281250003, 1.572960375, 1.5829879843750003, 1.5930880000000003, 1.6032597656249998, 1.6135026250000002, 1.6238159218750003, 1.6341990000000002, 1.644651203125, 1.6551718750000002, 1.6657603593750003, 1.6764160000000001, 1.687138140625, 1.6979261250000002, 1.7087792968750004, 1.719697, 1.7306785781249998, 1.7417233750000005, 1.7528307343750003, 1.764, 1.7752305156250003, 1.786521625, 1.7978726718750002, 1.809283, 1.8207519531250003, 1.8322788750000005, 1.8438631093750002, 1.855504, 1.8672008906250004, 1.8789531250000004, 1.8907600468750003, 1.902621, 1.9145353281250002, 1.9265023750000005, 1.9385214843750003, 1.9505919999999999, 1.9627132656250001, 1.9748846250000005, 1.9871054218750002, 1.9993750000000003, 2.011692703125, 2.0240578750000005, 2.0364698593750004, 2.048928, 2.061431640625001, 2.0739801250000003, 2.086572796875, 2.099209, 2.1118880781250007, 2.1246093750000004, 2.1373722343750003, 2.150176, 2.1630200156250003, 2.175903625, 2.188826171875, 2.2017870000000004, 2.214785453125, 2.2278208750000004, 2.240892609375, 2.2540000000000004, 2.2671423906250006, 2.280319125, 2.293529546875, 2.306773, 2.3200488281250005, 2.333356375, 2.346694984375, 2.3600640000000004, 2.3734627656250007, 2.3868906250000004, 2.4003469218750006, 2.413831, 2.4273422031250007, 2.4408798750000003, 2.454443359375, 2.468032000000001, 2.4816451406250004, 2.495282125, 2.508942296875, 2.5226250000000006, 2.5363295781250006, 2.5500553750000003, 2.563801734375, 2.5775680000000003, 2.5913535156250003, 2.6051576250000004, 2.618979671875, 2.632819, 2.6466749531250002, 2.660546875, 2.6744341093750004, 2.688336, 2.7022518906250004, 2.7161811250000003, 2.730123046875, 2.7440770000000008, 2.758042328125, 2.772018375, 2.7860044843750003, 2.8000000000000007, 2.8140042656250004, 2.8280166250000005, 2.8420364218750005, 2.8560630000000007, 2.870095703125, 2.884133875, 2.898176859375001, 2.9122240000000006, 2.9262746406250004, 2.940328125, 2.9543837968750006, 2.9684410000000003, 2.982499078125, 2.996557375, 3.010615234375001, 3.0246720000000002, 3.038727015625, 3.052779625, 3.0668291718750007, 3.0808750000000003, 3.094916453125, 3.108952875000001, 3.1229836093750007, 3.1370080000000002, 3.151025390625, 3.165035125, 3.179036546875001, 3.1930290000000006, 3.207011828125, 3.220984375, 3.234945984375001, 3.2488960000000002, 3.262833765625, 3.276758625, 3.2906699218750006, 3.3045670000000005, 3.318449203125, 3.332315875000001, 3.3461663593750006, 3.3600000000000003, 3.3738161406250002, 3.3876141250000007, 3.4013932968750007, 3.415153, 3.428892578125, 3.4426113750000007, 3.4563087343750003, 3.469984, 3.483636515625, 3.4972656250000007, 3.5108706718750007, 3.5244510000000004, 3.5380059531250008, 3.5515348750000006, 3.5650371093750004, 3.5785120000000004, 3.591958890625, 3.605377125000001, 3.6187660468750003, 3.6321250000000003, 3.645453328125, 3.6587503750000008, 3.6720154843750006, 3.685248, 3.698447265625, 3.7116126250000008, 3.7247434218750004, 3.737839, 3.750898703125, 3.7639218750000007, 3.7769078593750005, 3.7898560000000003, 3.802765640625001, 3.8156361250000006, 3.8284667968750004, 3.841257, 3.854006078125, 3.8667133750000007, 3.8793782343750003, 3.892000000000001, 3.9045780156250007, 3.9171116250000004, 3.929600171875, 3.942043, 3.954439453125001, 3.9667888750000007, 3.9790906093750005, 3.9913440000000002, 4.003548390625, 4.015703125000001, 4.0278075468750005, 4.039861, 4.051862828125, 4.063812375, 4.075708984375, 4.087552, 4.099340765625, 4.1110746250000005, 4.1227529218750005, 4.134375000000001, 4.145940203125001, 4.157447875000001, 4.168897359375, 4.180288, 4.191619140625001, 4.202890125000001, 4.214100296875001, 4.225249000000001, 4.236335578125001, 4.247359375, 4.258319734375, 4.269216000000001, 4.280047515625, 4.290813625, 4.301513671875001, 4.312147, 4.322712953125, 4.333210875000001, 4.343640109375, 4.354000000000001, 4.364289890625001, 4.374509125, 4.384657046875, 4.394733, 4.404736328125001, 4.414666375, 4.424522484375001, 4.434304000000001, 4.444010265625001, 4.453640625, 4.463194421875, 4.472671000000001, 4.482069703125, 4.491389875, 4.500630859375001, 4.509792000000001, 4.518872640625, 4.527872125, 4.536789796875, 4.545625, 4.554377078125, 4.5630453750000015, 4.571629234375001, 4.580128, 4.588541015625, 4.596867625, 4.605107171875001, 4.613259, 4.621322453125001, 4.6292968750000005, 4.637181609375, 4.644976000000001, 4.652679390625001, 4.6602911250000005, 4.667810546875001, 4.675237000000001, 4.6825698281250006, 4.689808375, 4.696951984375, 4.704000000000001, 4.710951765625, 4.717806625000001, 4.724563921875001, 4.731223000000001, 4.737783203125001, 4.744243875, 4.750604359375001, 4.756864, 4.763022140625, 4.769078125000001, 4.775031296875, 4.780881000000001, 4.786626578125, 4.792267375, 4.797802734375001, 4.803232, 4.808554515625001, 4.813769625000001, 4.8188766718750005, 4.823875, 4.828763953125001, 4.833542875000001, 4.838211109375001, 4.842768, 4.847212890625, 4.851545125, 4.8557640468750005, 4.859869000000001, 4.863859328125001, 4.867734375000001, 4.871493484375001, 4.875136, 4.878661265625, 4.8820686250000005, 4.885357421875001, 4.888527000000001, 4.891576703125001, 4.894505875000001, 4.897313859375001, 4.9,]
R_FROM_MOS_VALUES = [0, 3.25, 3.5, 3.75, 4.0, 4.25, 4.5, 4.75, 5.0, 5.25, 5.5, 5.75, 6.0, 6.25, 6.5, 6.75, 7.0, 7.25, 7.5, 7.75, 8.0, 8.25, 8.5, 8.75, 9.0, 9.25, 9.5, 9.75, 10.0, 10.25, 10.5, 10.75, 11.0, 11.25, 11.5, 11.75, 12.0, 12.25, 12.5, 12.75, 13.0, 13.25, 13.5, 13.75, 14.0, 14.25, 14.5, 14.75, 15.0, 15.25, 15.5, 15.75, 16.0, 16.25, 16.5, 16.75, 17.0, 17.25, 17.5, 17.75, 18.0, 18.25, 18.5, 18.75, 19.0, 19.25, 19.5, 19.75, 20.0, 20.25, 20.5, 20.75, 21.0, 21.25, 21.5, 21.75, 22.0, 22.25, 22.5, 22.75, 23.0, 23.25, 23.5, 23.75, 24.0, 24.25, 24.5, 24.75, 25.0, 25.25, 25.5, 25.75, 26.0, 26.25, 26.5, 26.75, 27.0, 27.25, 27.5, 27.75, 28.0, 28.25, 28.5, 28.75, 29.0, 29.25, 29.5, 29.75, 30.0, 30.25, 30.5, 30.75, 31.0, 31.25, 31.5, 31.75, 32.0, 32.25, 32.5, 32.75, 33.0, 33.25, 33.5, 33.75, 34.0, 34.25, 34.5, 34.75, 35.0, 35.25, 35.5, 35.75, 36.0, 36.25, 36.5, 36.75, 37.0, 37.25, 37.5, 37.75, 38.0, 38.25, 38.5, 38.75, 39.0, 39.25, 39.5, 39.75, 40.0, 40.25, 40.5, 40.75, 41.0, 41.25, 41.5, 41.75, 42.0, 42.25, 42.5, 42.75, 43.0, 43.25, 43.5, 43.75, 44.0, 44.25, 44.5, 44.75, 45.0, 45.25, 45.5, 45.75, 46.0, 46.25, 46.5, 46.75, 47.0, 47.25, 47.5, 47.75, 48.0, 48.25, 48.5, 48.75, 49.0, 49.25, 49.5, 49.75, 50.0, 50.25, 50.5, 50.75, 51.0, 51.25, 51.5, 51.75, 52.0, 52.25, 52.5, 52.75, 53.0, 53.25, 53.5, 53.75, 54.0, 54.25, 54.5, 54.75, 55.0, 55.25, 55.5, 55.75, 56.0, 56.25, 56.5, 56.75, 57.0, 57.25, 57.5, 57.75, 58.0, 58.25, 58.5, 58.75, 59.0, 59.25, 59.5, 59.75, 60.0, 60.25, 60.5, 60.75, 61.0, 61.25, 61.5, 61.75, 62.0, 62.25, 62.5, 62.75, 63.0, 63.25, 63.5, 63.75, 64.0, 64.25, 64.5, 64.75, 65.0, 65.25, 65.5, 65.75, 66.0, 66.25, 66.5, 66.75, 67.0, 67.25, 67.5, 67.75, 68.0, 68.25, 68.5, 68.75, 69.0, 69.25, 69.5, 69.75, 70.0, 70.25, 70.5, 70.75, 71.0, 71.25, 71.5, 71.75, 72.0, 72.25, 72.5, 72.75, 73.0, 73.25, 73.5, 73.75, 74.0, 74.25, 74.5, 74.75, 75.0, 75.25, 75.5, 75.75, 76.0, 76.25, 76.5, 76.75, 77.0, 77.25, 77.5, 77.75, 78.0, 78.25, 78.5, 78.75, 79.0, 79.25, 79.5, 79.75, 80.0, 80.25, 80.5, 80.75, 81.0, 81.25, 81.5, 81.75, 82.0, 82.25, 82.5, 82.75, 83.0, 83.25, 83.5, 83.75, 84.0, 84.25, 84.5, 84.75, 85.0, 85.25, 85.5, 85.75, 86.0, 86.25, 86.5, 86.75, 87.0, 87.25, 87.5, 87.75, 88.0, 88.25, 88.5, 88.75, 89.0, 89.25, 89.5, 89.75, 90.0, 90.25, 90.5, 90.75, 91.0, 91.25, 91.5, 91.75, 92.0, 92.25, 92.5, 92.75, 93.0, 93.25, 93.5, 93.75, 94.0, 94.25, 94.5, 94.75, 95.0, 95.25, 95.5, 95.75, 96.0, 96.25, 96.5, 96.75, 97.0, 97.25, 97.5, 97.75, 98.0, 98.25, 98.5, 98.75, 99.0, 99.25, 99.5, 99.75, 100.0,]
# fmt: on


def mos_from_r(Q):
    if Q <= 0:
        return MOS_MIN
    if Q >= 100:
        return MOS_MAX
    MOS = (
        MOS_MIN + float(MOS_MAX - MOS_MIN) * float(Q) / 100.0 + float(Q) * float(Q - 60.0) * float(100.0 - Q) * 0.000007
    )
    return MOS


def r_from_mos(MOS):
    if MOS < MOS_MIN:
        MOS = MOS_MIN
    if MOS > MOS_MAX:
        MOS = MOS_MAX

    if MOS in R_FROM_MOS_KEYS:
        Q = R_FROM_MOS_VALUES[R_FROM_MOS_KEYS.index(MOS)]
    else:
        Q = np.interp(MOS, R_FROM_MOS_KEYS, R_FROM_MOS_VALUES)
    return Q


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
    feature_selection_filename = filename_with_path.replace("_reg.json", "_fs.json")
    feature_selection = None
    if os.path.isfile(feature_selection_filename):
        feature_selection = json_load(feature_selection_filename)

    regressor = deserialize_random_forest_regressor_json(filename_with_path)  # skljson.from_json()
    # override n_jobs to prevent warning, model should be fast enough
    # n_jobs helps during training
    regressor.n_jobs = 1

    class Model:
        """ wrapper to the serialized scikit learn model,
        that uses feature selection in the first step
        """

        def __init__(self, regressor, fs=None):
            self._regressor = regressor
            self._fs = fs

        def feature_select(self, X):
            fs = np.array(self._fs)
            X = np.array(X)
            _X = []
            # perform selection for each input row
            for x in X:
                _X.append(x[fs])
            return _X

        def predict(self, X):
            if self._fs:
                X = self.feature_select(X)
            return self._regressor.predict(X)

    return Model(regressor, feature_selection)


def binarize_column(dataframe, column, prefix=""):
    """
    add separate binarized columns to a given dataframe for each uniqe value of column
    """
    values = dataframe[column].unique()
    for value in values:
        dataframe[prefix + value] = dataframe[column].map(lambda x: 1 if x == value else 0)
    return dataframe

def load_dict_values(dataframe, column):
    """
    load values that are nested as a dictionary for a specific column
    """
    if column not in dataframe.columns:
        return dataframe
    _values = list(dataframe[column].apply(lambda x: json.loads(x) if type(x) == str else x).values)
    _values = pd.DataFrame(_values).add_prefix(column + "_")

    dataframe = pd.concat((dataframe, _values), axis=1)

    return dataframe


def per_sample_interval_function(mos_O27, prediction_features, intervall=1):
    prediction_features = load_dict_values(prediction_features, "QPstatspersecond")
    prediction_features = load_dict_values(prediction_features, "QPValuesStatsPerGop")
    mos_O22 = []
    for i in range(0, int(prediction_features["duration"].values[0])):
        mean_qp_non_i = float(prediction_features["QPValuesStatsPerGop_mean_Av_QPBB_non-i"])
        if "QPstatspersecond_mean_qpbb_non_i_" + str(i) + "_sec" in prediction_features:
            mean_qp_per_sec = float(prediction_features["QPstatspersecond_mean_qpbb_non_i_" + str(i) + "_sec"])
        else:
            mean_qp_per_sec = mean_qp_non_i
        if mean_qp_per_sec != 0 and not(np.isnan(mean_qp_per_sec)):
            mos_per_sec = (mean_qp_non_i / mean_qp_per_sec) * mos_O27
        else:
            mos_per_sec = mos_O27
        mos_per_sec = np.clip(mos_per_sec, 1, 5)
        mos_O22.append(mos_per_sec)
    return mos_O22


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
                f = {
                    x: f[x][select_element] if type(f[x]) == list else f[x] for x in list(set(columns) & set(f.keys()))
                }
        gop.append(f)
    yield gop


def stats_per_gop(processed_video_sequence, needed=[]):
    """
    general helper to extract statistics on a per gop basis
    """
    logging.debug(f"calculate {needed} gop based for {processed_video_sequence}")
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
                gop_res["{}_quantil_{}".format(quantile, x)] = float(df[x].quantile(quantile))
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
                gop_res["{}_quantil_{}_non-i".format(quantile, x)] = float(df[x].quantile(quantile))

        results.append(gop_res)
    df = pd.DataFrame(results)
    result = df.mean().to_dict()
    logging.debug(f"estimated {needed} feature values: {result}")
    return result
