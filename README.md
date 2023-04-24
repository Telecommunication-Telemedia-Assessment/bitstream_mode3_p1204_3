# ITU-T P.1204.3 Reference Implementation

ITU-T P.1204.3 is a short term video quality prediction model that uses full bitstream data to estimate video quality scores on a segment level.

If you use this model in any of your research work, please cite the following paper:

```bibtex
@inproceedings{rao2020p1204,
  author={Rakesh Rao {Ramachandra Rao} and Steve G\"oring and Werner Robitza and Alexander Raake and Bernhard Feiten and Peter List and Ulf Wüstenhagen},
  title={Bitstream-based Model Standard for 4K/UHD: ITU-T P.1204.3 -- Model Details, Evaluation, Analysis and Open Source Implementation},
  BOOKTITLE={2020 Twelfth International Conference on Quality of Multimedia Experience (QoMEX)},
  address="Athlone, Ireland",
  days=26,
  month=May,
  year=2020,
}
```

Moreover a full description of the models internal structure is provided in the paper.

This model has further been extended to different application scopes depending on the available input information. This extension consists of a Mode 0 model (uses only metadata such as codec type, framerate, resoution and bitrate as input), a Mode 1 model (uses Mode 0 information and frame-type and -size information as input), and a Hybrid Mode 0 model (based on Mode 0 metadata and the decoded video pixel information). These models along with ITU-T Rec. P.1204.3 together form a family of models called [_AVQBits_](https://ieeexplore.ieee.org/document/9846967). An open source implementation of these extensions can be found [here](https://github.com/Telecommunication-Telemedia-Assessment/p1204_3_extensions).

Contents:

- [Requirements](#requirements)
- [Input Data and Scope](#input-data-and-scope)
- [Usage](#usage)
  - [Detailed Options](#detailed-options)
- [Docker Usage](#docker-usage)
- [License](#license)
- [Authors](#authors)

## Requirements

To be able to run the model you need to install some software. In addition, we suggest to have high enough free memory available – for a 10 second UHD-1 video sequence, 4 GB of memory should be sufficient.

* Linux 64-bit (Currently the model is only tested on Ubuntu >= 18.04, i.e. 18.04, 20.04, 22.04)
* git
* Python 3 (`python3`, `python3-pip`, `python3-venv`)
* `poetry` (e.g. `pip3 install poetry`)
* `ffmpeg`
* [bitstream_mode3_videoparser](https://github.com/Telecommunication-Telemedia-Assessment/bitstream_mode3_videoparser)
    * all dependencies for the bitstream_mode3_videoparser are required, so please 
    * the software itself will be installed automatically

First, clone the repository:

```bash
git clone https://github.com/Telecommunication-Telemedia-Assessment/bitstream_mode3_p1204_3
cd bitstream_mode3_p1204_3
```

Install all requirements under Ubuntu:

```bash
sudo apt-get update -qq
sudo apt-get install -y -qq python3 python3-venv python3-pip git scons ffmpeg
# ffmpeg/videoparser specific
sudo apt-get -y install autoconf automake build-essential libass-dev libfreetype6-dev libsdl2-dev libtheora-dev libtool libva-dev libvdpau-dev libvorbis-dev libxcb1-dev libxcb-shm0-dev libxcb-xfixes0-dev pkg-config texinfo wget zlib1g-dev yasm
```

Run the following command to install the Python requirements:

```bash
poetry install
```

If you have problems with pip and poetry, run `pip3 install --user -U pip`.

## Input Data and Scope

The following inputs are within the scope of the P.1204.3 recommendation, see also Table 3 of ITU-T Rec. P.1204:

- Format/Codec: H.264, H.265, VP9, wrapped in a container that ffmpeg can read (e.g., `.mkv`)
- Duration: 7–9 seconds. Optimal performance for roughly 8 seconds. Models are assumed to provide valid overall video-quality estimations for 5–10 s long sequences.
- Bit depth: 8 or 10 bit
- Chroma subsampling: YUV 4:2:0 and YUV 4:2:2
- Coded resolution: Video sequences of up to 2160p resolution (4K/UHD-1)
- Display resolution and framerate:
  - PC/TV: 2160p, up to 60 frames/s
  - Mobile/Tablet: 1440p, up to 60 frames/s.
- Viewing distances:
  - PC/TV: 1.5H to 3H (H: Screen height)
  - Mobile/Tablet: 4H to 6H

Check out the `test_videos` folder for some examples.

For example, the [AVT-VQDB-UHD-1](https://github.com/Telecommunication-Telemedia-Assessment/AVT-VQDB-UHD-1) can be used to validate the model performance, as it is shown in the paper `rao2020p1204`.

## Usage

Run the built-in Python tool on a test video:

```bash
poetry run p1204_3 test_videos/test_video_h264.mkv
```

The output will include log message printed on stderr and output scores printed on stdout.

The resulting video quality metrics will be printed in a JSON-formatted array, where each entry corresponds to one input file. For example, to only get the metrics printed in JSON format, run:

```bash
poetry run p1204_3 test_videos/test_video_h264.mkv -q
```

The output will look as follows:

```json
[
    {
        "date": "2020-08-28 10:37:48.721183",
        "debug": {
            "baseline": 4.16292374098929,
            "coding_deg": 32.43006645212775,
            "rf_pred": 4.010545689643026,
            "temporal_deg": 0.0,
            "upscaling_deg": 0.0
        },
        "per_second": [
            4.132547886568417,
            3.931621503558015,
            4.328687969986304,
            4.3002566462931,
            4.1819097998511054,
            3.9471693619756834,
            3.935126424508243,
            3.9407565516571026,
            3.955412313745017,
            3.991729591232866
        ],
        "per_sequence": 4.086734715316158,
        "video_basename": "test_video_h264.mkv",
        "video_full_path": "test_videos/test_video_h264.mkv"
    }
]
```

Here, the most relevant output is the `per_sequence` value, which gives the quality of the video sequence on a mean opinion score (MOS) scale between 1 and 5, where 1 corresponds to bad and 5 corresponds to excellent.

The `per_second` values are MOS values per each second of input.

The `debug` values are provided for internal testing and diagnostics.


## Usage globally
If you want to use this model globally in your system, you can also install everything with 

```bash
pip3 install .  # you must be in the repository folder
```
and then the `p1204_3` command line tool is installed.
For this it is recommended to perform the installation in a virtual environment, due to the may be older dependencies. (thus the virtual environment must be activated to access the command line tool).
It is further recommended to check the installation before using the `Usage` part, and this installation will also redo the `video_parser` compilation. 




### Detailed Options

Otherwise check the included help, `poetry run p1204_3 --help`:

```
usage: p1204_3 [-h] [--result_folder RESULT_FOLDER] [--model MODEL] [--cpu_count CPU_COUNT] [--device_type {pc,tv,tablet,mobile}]
               [--device_resolution {3840x2160,2560x1440}] [--viewing_distance {1.5xH,4xH,6xH}] [--display_size {10,32,37,5.1,5.5,5.8,55,65,75}] [--tmp TMP]
               [-d] [-nocached_features] [-q]
               video [video ...]

ITU-T P.1204.3 video quality model reference implementation

positional arguments:
  video                 input video to estimate quality

optional arguments:
  -h, --help            show this help message and exit
  --result_folder RESULT_FOLDER
                        folder to store video quality results (default: reports)
  --model MODEL         model config file to be used for prediction (default:
                        ./p1204_3/models/p1204_3/config.json)
  --cpu_count CPU_COUNT
                        thread/cpu count (default: 8)
  --device_type {pc,tv,tablet,mobile}
                        device that is used for playout (default: pc)
  --device_resolution {3840x2160,2560x1440}
                        resolution of the output device (width x height) (default: 3840x2160)
  --viewing_distance {1.5xH,4xH,6xH}
                        viewing distance relative to the display height (not used for model prediction) (default: 1.5xH)
  --display_size {10,32,37,5.1,5.5,5.8,55,65,75}
                        display diagonal size in inches (not used for model prediction) (default: 55)
  --tmp TMP             temporary folder to store bitstream stats and other intermediate results (default: ./tmp)
  -d, --debug           show debug output (default: False)
  -nocached_features    no caching of features (default: False)
  -q, --quiet           not print any output except errors (default: False)

stg7, rrao 2020
```

Most parameter default settings are for the PC/TV use case, change to different use cases based on the scope of the recommendation.

**Important caveats:**

- In contrast to the official ITU-T P.1204.3 description we provided here the random forest part as a serialized output of `scikit-learn`. A generated Python script including the estimated trees can be found on the [ITU-T P.1204.3 page](https://www.itu.int/rec/T-REC-P.1204.3/en).
- The parameters `viewing_distance` and `display_size` are not used for the prediction (changes will have no effect), however they are formally specified as input parameters for P.1204.3.
- The `device_type` and `device_resolution` parameters are dependent on each other. The model is not trained on combinations not part of the standard, e.g. testing TV/PC with `2560x1440` as resolution is not valid, as this resolution is only suitable for tablet and mobile.

## Docker Usage

To build a Docker image, and run the test videos, call:

```bash
./docker_build_run.sh
```

Check out the script to see how the temporary folders are mapped into the Docker container.

## License

Copyright 2017-2022 Technische Universität Ilmenau, Deutsche Telekom AG

Permission is hereby granted, free of charge, to use the software for non-commercial research purposes.

Any other use of the software, including commercial use, merging, publishing, distributing, sublicensing, and/or selling copies of the Software, is forbidden.

For a commercial license, you must contact the respective rights holders of the standards ITU-T Rec. P.1204 and ITU-T Rec. P.1204.3 See https://www.itu.int/en/ITU-T/ipr/Pages/default.aspx for more information.

NO EXPRESS OR IMPLIED LICENSES TO ANY PARTY'S PATENT RIGHTS ARE GRANTED BY THIS LICENSE. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Authors

Main developers:
* Steve Göring - Technische Universität Ilmenau
* Rakesh Rao Ramachandra Rao - Technische Universität Ilmenau

Contributors:
* Alexander Raake - Technische Universität Ilmenau
* Bernhard Feiten - Deutsche Telekom AG
* Peter List - Deutsche Telekom AG
* Ulf Wüstenhagen - Deutsche Telekom AG
* Werner Robitza - Technische Universität Ilmenau
