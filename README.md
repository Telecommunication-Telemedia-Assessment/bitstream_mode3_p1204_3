# ITU-T P.1204.3 Reference Implementation
ITU-T P.1204.3 is a short term video quality prediction model that uses full bitstream data to estimate video quality scores.

## Requirements

* python3, python3-pip
* poetry (e.g. see https://python-poetry.org/docs/#installation)

## Input Data and Scope

As input to the model you need a encoded video sequence of short duration, e.g. 8-10s (based on the ITU-T P.1204 documentation).
H.264, H.265 or VP9 are possible video codecs of the given video sequence.


