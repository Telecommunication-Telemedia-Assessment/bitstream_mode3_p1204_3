# ITU-T P.1204.3 Reference Implementation
ITU-T P.1204.3 is a short term video quality prediction model that uses full bitstream data to estimate video quality scores.

## Requirements

* python3, python3-pip
* poetry (e.g. see https://python-poetry.org/docs/#installation)
* ffmpeg
* videoparser (see XYZ), will be installed automatically
    * all dependencies for the videoparser are required
* git

## Input Data and Scope

As input to the model you need an encoded video sequence of short duration, e.g. 8-10s (based on the ITU-T P.1204 documentation).
H.264, H.265 or VP9 are possible video codecs of the given video sequence.

## Usage
To use the provided tool, e.g. run
```bash
poetry run p1204_3 test_videos/test_video_h264.mkv
```

Otherwise check the included help, `poetry run model --help`:
```
# TODO
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
