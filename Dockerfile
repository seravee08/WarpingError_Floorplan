# Copyright 2021 Allvision IO, Inc.
# author: ryan@allvision.io
# usage: docker build -t <tag> -f <path/to/this/file>
FROM ubuntu:18.04
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y libpng-dev python3 python3-pip libopencv-dev
RUN pip3 install --upgrade awscli
WORKDIR /allvision/dev
COPY ./ /allvision/dev
RUN mkdir /allvision/build
RUN mkdir /allvision/samples
RUN make && cp ./build/linux/warping_error /allvision/build/
RUN cp -R /allvision/dev/samples/* /allvision/samples
WORKDIR /allvision
RUN rm -Rf /allvision/dev
