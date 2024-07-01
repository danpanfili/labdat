#!/bin/bash

ffmpeg -y \
-hwaccel_device 0 \
-hwaccel cuda \
-init_hw_device opencl=gpu:0.0 \
-filter_hw_device gpu \
-vsync vfr \
-ss 00:01:30 \
-i $1 \
-vf fps=fps=4,format=yuv420p,hwupload,nlmeans_opencl=2.0:5:3:3:3,hwdownload,format=yuv420p \
-c:a copy \
-crf 22 \
-pix_fmt yuv420p \
-buffer_size 300M \
-movflags \
+faststart \
$2/%06d.bmp

