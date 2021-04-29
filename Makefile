# Copyright 2021 Allvision IO, Inc.
# author: ryan@allvision.io
all: build/linux/warping_error

build/linux/warping_error: warping_error.cpp main.cpp warping_error.h
	mkdir -p build/linux
	g++ -o build/linux/warping_error warping_error.cpp main.cpp -l opencv_core -l opencv_imgproc -l opencv_imgcodecs -l opencv_highgui
