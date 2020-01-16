# ITU-T P.1204.3 Reference Implementation
ITU-T P.1204.3 is a short term video quality prediction model that uses full bitstream data to estimate video quality scores.

## Requirements

* python3, python3-pip, python3-venv
* poetry (e.g. pip3 install poetry)
* ffmpeg
* videoparser (see XYZ), will be installed automatically
    * all dependencies for the videoparser are required
* git

Run the following command:

```bash
poetry install
```
(if you have problems with pip, run `pip3 install --user -U pip`)

## Input Data and Scope

As input to the model you need an encoded video sequence of short duration, e.g. 8-10s (based on the ITU-T P.1204 documentation).
H.264, H.265 or VP9 are possible video codecs of the given video sequence.

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

## License
Copyright 2017-2020 Deutsche Telekom AG, Technische Universität Ilmenau

Permission is hereby granted, free of charge, to use the software for non-commercial research purposes.

Any other use of the software, including commercial use, merging, publishing, distributing, sublicensing, and/or selling copies of the Software, is forbidden.

For a commercial license, you must contact the respective rights holders of the standards ITU-T Rec. P.1204 and ITU-T Rec. P.1204.3 See https://www.itu.int/en/ITU-T/ipr/Pages/default.aspx for more information.

NO EXPRESS OR IMPLIED LICENSES TO ANY PARTY'S PATENT RIGHTS ARE GRANTED BY THIS LICENSE. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Authors

Main developers:
* Steve Göring; Technische Universität Ilmenau
* Rakesh Rao Ramachandra Rao; Technische Universität Ilmenau

Contributors:
* Alexander Raake; Technische Universität Ilmenau
* Bernhard Feiten; Deutsche Telekom AG
* Peter List; Deutsche Telekom AG
* Ulf Wüstenhagen; Deutsche Telekom AG
* Werner Rubitza; Technische Universität Ilmenau
