import os
from p1204_3 import __version__
from p1204_3 import predict_quality


def test_version():
    assert __version__ == '0.1.0'


def test_model_prediction():
    test_video = os.path.join(
        os.path.dirname(__file__),
        "..",
        "test_videos",
        "test_video_h264.mkv"
    )
    model_config_filename = os.path.join(
        os.path.dirname(__file__),
        "..",
        "p1204_3",
        "models",
        "p1204_3",
        "config.json"
    )

    res = predict_quality(
        test_video,
        model_config_filename=model_config_filename,
        device_type="pc",
        device_resolution="3840x2160",
        viewing_distance="1.5xH",
        display_size=55,
        temporary_folder="tmp"
    )
    print(res)

