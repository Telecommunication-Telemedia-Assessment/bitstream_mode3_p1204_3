# ITU-T P.1204.3 Reference Implementation
ITU-T P.1204.3 is a short term video quality prediction model that uses full bitstream data to estimate video quality scores on a segment level.

If you use this model in any of your research work, please cite the following paper:

```
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

## Requirements
To be able to run the model you need to install some software.
Currently the model is only tested on Ubuntu >= 18.04.

* git
* python3, python3-pip, python3-venv
* poetry (e.g. pip3 install poetry)
* ffmpeg
* [bitstream_mode3_videoparser](https://github.com/Telecommunication-Telemedia-Assessment/bitstream_mode3_videoparser), will be installed automatically
    * all dependencies for the bitstream_mode3_videoparser are required

To install all requirements under Ubuntu please run the following commands:

```bash
sudo apt-get update -qq
sudo apt-get install -y -qq python3 python3-venv python3-numpy python3-pip git scons ffmpeg
pip3 install --user poetry
# ffmpeg/videoparser specific
sudo apt-get -y install autoconf automake build-essential libass-dev libfreetype6-dev libsdl2-dev libtheora-dev libtool libva-dev libvdpau-dev libvorbis-dev libxcb1-dev libxcb-shm0-dev libxcb-xfixes0-dev pkg-config texinfo wget zlib1g-dev yasm
```

After cloning this repository and installation of all requirements, run the following command:

```bash
poetry install
```

If you have problems with pip and poetry, run `pip3 install --user -U pip`.

## Input Data and Scope

As input to the model you need an encoded video sequence of short duration, e.g. 8-10s (based on the ITU-T P.1204 documentation), e.g. checkout the `test_videos` folder.
H.264, H.265 or VP9 are supported video codecs of the input video sequence.
For example the [AVT-VQDB-UHD-1](https://github.com/Telecommunication-Telemedia-Assessment/AVT-VQDB-UHD-1) can be used to validate the model performance, as it is shown in the paper `rao2020p1204`.

## Usage
To use the provided tool, e.g. run
```bash
poetry run p1204_3 test_videos/test_video_h264.mkv
```

Otherwise check the included help, `poetry run p1204_3 --help`:
```
usage: p1204_3 [-h] [--result_folder RESULT_FOLDER] [--model MODEL]
               [--cpu_count CPU_COUNT] [--device_type {pc,tv,tablet,mobile}]
               [--device_resolution {3840x2160,2560x1440}]
               [--viewing_distance {1.5xH,4xH,6xH}]
               [--display_size {10,32,37,5.1,5.5,5.8,55,65,75}] [--tmp TMP]
               video [video ...]

ITU-T P.1204.3 video quality model reference implementation

positional arguments:
  video                 input video to estimate quality

optional arguments:
  -h, --help            show this help message and exit
  --result_folder RESULT_FOLDER
                        folder to store video quality results (default:
                        reports)
  --model MODEL         model config file to be used for prediction (default:
                        ./p1204_3/models/p1204_3/config.json)
  --cpu_count CPU_COUNT
                        thread/cpu count (default: 8)
  --device_type {pc,tv,tablet,mobile}
                        device that is used for playout (default: pc)
  --device_resolution {3840x2160,2560x1440}
                        resolution of the output device (width x height)
                        (default: 3840x2160)
  --viewing_distance {1.5xH,4xH,6xH}
                        viewing distance relative to the display height
                        (default: 1.5xH)
  --display_size {10,32,37,5.1,5.5,5.8,55,65,75}
                        display diagonal size in inches (default: 55)
  --tmp TMP             temporary folder to store bitstream stats and other
                        intermediate results (default: ./tmp)

stg7, rrao 2019

```

Most parameter default settings are for the PC/TV use case, change to different use cases based on the scope of the recommendation.
*Important:* in contrast to the official ITU-T P.1204.3 description we provided here the random forest part as a serialized output of scikit-learn, a generated python script including the estimated trees can be found on the [ITU-T P.1204.3 page](https://www.itu.int/rec/T-REC-P.1204.3/en).

## License
Copyright 2017-2020 Technische Universität Ilmenau, Deutsche Telekom AG

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
