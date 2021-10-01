#!/bin/bash

sudo apt-get install -y libhdf5-dev libc-ares-dev libeigen3-dev
python3 -m pip install keras_applications==1.0.8 --no-deps
python3 -m pip install keras_preprocessing==1.1.0 --no-deps
python3 -m pip install h5py==2.9.0
sudo apt-get install -y openmpi-bin libopenmpi-dev
sudo apt-get install -y libatlas-base-dev
python3 -m pip install -U six wheel mock
#Pick a tensorflow release from https://github.com/lhelontra/tensorfl... (I picked 2.0.0):
#wget https://github.com/lhelontra/tensorfl...
python3 -m pip uninstall tensorflow
wget https://github.com/lhelontra/tensorflow-on-arm/releases/download/v2.4.0/tensorflow-2.4.0-cp37-none-linux_armv7l.whl
#Install wheel from: https://github.com/lhelontra/tensorfl
python3 -m pip install tensorflow-2.4.0-cp37-none-linux_armv7l.whl

#RESTART YOUR TERMINAL
#Reactivate your virtual environment:
#cd Desktop
#cd tf_pi
#source my_dev_venv/bin/activate
#Test:
#Open a python interpreter by executing: python3
#import tensorflow
#tensorflow.__version__
