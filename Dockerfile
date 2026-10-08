FROM ubuntu:20.04

ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -qq update && apt-get install -qq -y \
	python3 git \
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

WORKDIR /p1204_3
COPY --from=ghcr.io/astral-sh/uv:0.12.5 /uv /usr/local/bin/uv
ENV UV_PYTHON_INSTALL_DIR=/opt/python UV_LINK_MODE=copy
COPY . /p1204_3/
RUN uv sync --frozen --no-dev
ENV PATH="/p1204_3/.venv/bin:$PATH"

COPY ./p1204_3/bitstream_mode3_videoparser /p1204_3/p1204_3/
WORKDIR /p1204_3/p1204_3/bitstream_mode3_videoparser
RUN ./build.sh

WORKDIR /p1204_3
ENTRYPOINT ["python", "-m", "p1204_3"]
