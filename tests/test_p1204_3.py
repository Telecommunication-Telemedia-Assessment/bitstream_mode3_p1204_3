import os
from p1204_3 import predict_quality
from p1204_3.utils import json_load


def test_model_prediction_h264():
    root_dir = os.path.join(os.path.dirname(__file__), "..")
    test_videos_dir = os.path.join(root_dir, "test_videos")
    test_video = os.path.join(test_videos_dir, "test_video_h264.mkv")

    model_config_filename = os.path.join(root_dir, "p1204_3", "models", "p1204_3", "config.json")

    res = predict_quality(
        test_video,
        model_config_filename=model_config_filename,
        device_type="pc",
        device_resolution="3840x2160",
        viewing_distance="1.5xH",
        display_size=55,
        temporary_folder=os.path.join(test_videos_dir, "parsed"),
    )

    ref_report = os.path.join(test_videos_dir, "reports", "test_video_h264.json")
    ref_res = json_load(ref_report)
    for k in set(list(res.keys()) + list(ref_res.keys())) - set(["date", "video_full_path"]):
        assert k in ref_res and k in res
        assert ref_res[k] == res[k]
