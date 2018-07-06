FROM nvidia/cuda:8.0-cudnn6-devel-ubuntu16.04

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  python-setuptools \
  python-scipy \
  build-essential \
  cmake \
  git \
  wget \
  unzip \
  yasm \
  pkg-config \
  libjpeg8-dev \
  libtiff5-dev \
  libtiff-dev \
  libjasper-dev \
  libtbb2 \
  libtbb-dev \
  libpng-dev \
  libpng12-dev \
  libavcodec-dev \
  libavformat-dev \
  libswscale-dev \
  libv4l-dev \
  libxvidcore-dev \
  libx264-dev \
  libgtk-3-dev \
  libatlas-base-dev \
  gfortran \
  protobuf-compiler \
  lsb-release \
  libsnappy-dev \
  libprotobuf-dev \
  libopencv-dev \
  liblmdb-dev \
  libleveldb-dev \
  libhdf5-dev \
  libgoogle-glog-dev \
  libgflags-dev \
  libboost-all-dev \
  libatlas-base-dev \
  libatlas-dev \
  libpq-dev \
  && pip3 install --upgrade pip

# installing Opencv3.2

RUN wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.2.0.zip \
    && unzip opencv.zip

RUN wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.2.0.zip \
    && unzip opencv_contrib.zip

RUN pip install numpy

RUN mkdir ./opencv-3.2.0/build

WORKDIR ./opencv-3.2.0/build

RUN cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D INSTALL_C_EXAMPLES=OFF \
    -D OPENCV_EXTRA_MODULES_PATH=/opencv_contrib-3.2.0/modules \
    -D PYTHON_EXECUTABLE=/usr/bin/python3 \
    -D BUILD_EXAMPLES=False ..

RUN make -j4 && make install && ldconfig

WORKDIR /
RUN rm -rf opencv-3.2.0 opencv_contrib-3.2.0 opencv.zip opencv_contrib.zip

# installing Openpose
WORKDIR /

RUN git clone https://github.com/CMU-Perceptual-Computing-Lab/openpose.git

RUN mkdir ./openpose/build

WORKDIR ./openpose/build

RUN cmake -DBUILD_CAFFE=True -DDOWNLOAD_COCO_MODEL=True -DDOWNLOAD_FACE_MODEL=True -DDOWNLOAD_HAND_MODEL=True ..

RUN make -j4 && make install && bash /openpose/models/getModels.sh

# installing PyOpenPose
WORKDIR /

RUN apt-get install -y nano

RUN git clone https://github.com/FORTH-ModelBasedTracker/PyOpenPose.git 

RUN git clone https://github.com/chingchan1996/PyOpenPose-Modified.git
RUN rm ./PyOpenPose/PyOpenPoseLib/OpenPoseWrapper.cpp 
RUN cp ./PyOpenPose-Modified/OpenPoseWrapper.cpp ./PyOpenPose/PyOpenPoseLib/OpenPoseWrapper.cpp 
RUN mkdir ./PyOpenPose/build 
WORKDIR ./PyOpenPose/build
ENV OPENPOSE_ROOT=/openpose
RUN cmake -DWITH_PYTHON3=True ..
RUN make -j4 && make install
RUN ln -s /PyOpenPose/build/PyOpenPoseLib/PyOpenPose.so /usr/local/lib/python3.5/dist-packages/PyOpenPose.so

WORKDIR /openpose/models
# after entering the environment, run "bash ./getModels.sh" 