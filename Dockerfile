FROM ubuntu:18.04

ENV LANG C.UTF-8

RUN apt-get -qq update && apt-get install -qq -y \
	python3.8 python3-pip git \
	python3-venv python3-numpy \
	scons ffmpeg \
	autoconf automake \
	build-essential libass-dev \
	libfreetype6-dev libsdl2-dev \
	libtheora-dev libtool \
	libva-dev libvdpau-dev \
	libvorbis-dev libxcb1-dev \
	libxcb-shm0-dev libxcb-xfixes0-dev \
	pkg-config texinfo \
	wget zlib1g-dev yasm && \
	rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pandas

WORKDIR "/p1204_3"
RUN git clone --depth 1 https://github.com/Telecommunication-Telemedia-Assessment/bitstream_mode3_p1204_3.git /p1204_3
RUN pip3 install -r requirements.txt

WORKDIR "/p1204_3/p1204_3/bitstream_mode3_videoparser"
RUN git clone --depth 1 https://github.com/Telecommunication-Telemedia-Assessment/bitstream_mode3_videoparser /p1204_3/p1204_3/bitstream_mode3_videoparser
RUN ./build.sh

WORKDIR "/p1204_3"
ENTRYPOINT ["python3","-m","p1204_3"]
