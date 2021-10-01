#!/usr/bin/python3
#
# Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#
import sqlite3
import jetson.inference
import jetson.utils
import os
import argparse
import sys
import time
import schedule
import csv
#import schelude_folder_file_delete as file_cleanup
import numpy as np
from datetime import datetime
import logging

video_output = ''
image_output = ''
image_folder = ''
image_name = ''
get_image_time = ''
image_folder_label = 'imageNet_'
image_date = ''
image_file_label = 'imageNet_'
record_video_ext = '.jpg'
image_capture_ext = '.jpg'
image_capture = ''
v_out = ''
img_out = ''
storege_location = ''

#camera_1_folder = 'test_camera'
camera_1_folder = 'camera_1'
camera_2_folder = 'camera_2'
camera_3_folder = 'camera_3'
camera_4_folder = 'camera_4'
camera_sub_dir = ''
make_directory = ''

time_stamp = 0
location = 0
description = 0
description_id = 0
confidence = 0
color = 0
axel_count = 0
license_plate = 0
rfid = 0
speed = 0
image_path = 0
lane_id = 0
take_action = ''
conn = 0

detection_out = 0
FILTER1 = 'vehicle'
FILTER2 = 'bike'
FILTER3 = 'pickup truck'
START_MESS1 = 0
START_MESS2 = 400
EXIT_MESS1 = 900
EXIT_MESS2 = 1000
EXIT_COUNT = 0

distance = 0
center_l = 0
center_r = 0
count = 0
counter = 0
SPEED_TIME1 = 0
SPEED_TIME2 = 0

width = 1280 ## rtsp stream camera
height = 720 ## rtsp stream camera

#logger
LOG_FORMAT = '%(levelname)s %(asctime)s - %(message)s'
logging.basicConfig(filename ='/media/bob/ssd128/event.log',level=logging.DEBUG,format=LOG_FORMAT) #Append mode
#logging.basicConfig(filename ='/XAVIER_RELEASE/test.log',level=logging.DEBUG,format=LOG_FORMAT,filemode='w') #Overwrite mode
logger = logging.getLogger()
#logger.info('This is a test log')
#logger.debug('test debug log')
#logger.warning('test warning log')
#logger.error('test error log')
#logger.critical('test critical log')


MODEL = 'vehicleModel'
STORAGE_DIRECTORY = '/media/bob/ssd128/' # Storage database, images
if os.path.exists(STORAGE_DIRECTORY):
    pass
else:
    os.mkdir(STORAGE_DIRECTORY)

os.chdir(STORAGE_DIRECTORY)

#CREATE TABLE
#Following Python program will be used to create a table in previously created database:
def createTable():
    conn.execute('''CREATE TABLE DATA_AQUISITION2
    (TIMESTAMP TEXT  PRIMARY KEY NOT NULL,
    LOCATION TEXT NOT NULL,
    DESCRIPTION TEXT NOT NULL,
    DESCRIPTION_ID TEXT NOT NULL,
    CONFIDENCE TEXT NOT NULL,
    COLOR TEXT NOT NULL,
    AXEL_COUNT TEXT NOT NULL,
    LICENSE_PLATE TEXT NOT NULL,
    RFID TEXT NOT NULL,
    SPEED TEXT NOT NULL,
    LANE_ID TEXT NOT NULL,
    IMAGE_PATH TEXT NOT NULL);''')
    print ("Table created successfully")


if os.path.exists('Dbox_3.db'):
    conn = sqlite3.connect('Dbox_3.db')
else:
    conn = sqlite3.connect('Dbox_3.db')
    createTable()

print ("Opened database successfully")
print ('data acqusition started....')



def image_folder_name():
    get_image_time = datetime.now()
    camera_sub_dir = get_image_time.strftime("%Y_%m_%d")
    return camera_sub_dir

class cameraDirectory: #camera_root_dir, camera_sub_dir
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getCameraDirectory(self):
        os.chdir(self.x)
        path = (os.getcwd())
        if os.path.exists(self.y):
            pass
        else:
            os.mkdir(os.path.join(path, self.y))
            return


class imageDirectory: #STORAGE_DIRECTORY, camera_sub_dir
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getImageDirectory(self):
        os.chdir(STORAGE_DIRECTORY)
        os.chdir(self.x)
        path = (os.getcwd())
        if os.path.exists(self.y):
            pass
        else:
            os.mkdir(os.path.join(path, self.y))
            return

#test image root directory
image_directory = cameraDirectory(STORAGE_DIRECTORY, camera_1_folder)
image_directory.getCameraDirectory()
image_directory = cameraDirectory(STORAGE_DIRECTORY, camera_2_folder)
image_directory.getCameraDirectory()
image_directory = cameraDirectory(STORAGE_DIRECTORY, camera_3_folder)
image_directory.getCameraDirectory()
image_directory = cameraDirectory(STORAGE_DIRECTORY, camera_4_folder)
image_directory.getCameraDirectory()


#test image sub-directory
image_sub_directory = imageDirectory(camera_1_folder, image_folder_name())
image_sub_directory.getImageDirectory()
#os.chdir(STORAGE_DIRECTORY)
image_sub_directory = imageDirectory(camera_2_folder, image_folder_name())
image_sub_directory.getImageDirectory()
#os.chdir(STORAGE_DIRECTORY)
image_sub_directory = imageDirectory(camera_3_folder, image_folder_name())
image_sub_directory.getImageDirectory()
#os.chdir(STORAGE_DIRECTORY)
print('STORAGE_DIRECTORY IS: ', STORAGE_DIRECTORY)
image_sub_directory = imageDirectory(camera_4_folder, image_folder_name())
image_sub_directory.getImageDirectory()

boxes = []
confidence = []
class_id = []
classes = []

def getVideo():
    get_image_time = datetime.now()
    get_image_time = get_image_time.strftime("%Y-%m-%d-%H%M%S%f")
    #image_date, image_time = get_image_time.split('_')
    #image_name = '{}{}{}'.format(image_file_label, get_image_time, record_video_ext)
    video_out_1 = '{}{}'.format(get_image_time, record_video_ext)
    video_out_2 = '{}{}{}'.format(camera_2_folder, get_image_time, image_capture_ext)
    video_out_3 = '{}{}{}'.format(camera_3_folder, get_image_time, image_capture_ext)
    video_out_4 = '{}{}{}'.format(camera_4_folder, get_image_time, image_capture_ext)
    #image_folder = str(image_folder)
    #image_name = str(image_name)
    os.chdir(STORAGE_DIRECTORY)
    path = (os.getcwd())
    #time.sleep(.02)
    video_output = (os.path.join(path, camera_1_folder, image_folder_name(), video_out_1))
    #video_output = (os.path.join(path, image_folder, image_name))
    return video_output, get_image_time

#net = jetson.inference.imageNet('alexnet')
net = jetson.inference.imageNet('googlenet-12')
#net_detect = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.4) ## default is 0.5 higher number less sensitive
net_detect = jetson.inference.detectNet('ssd-mobilenet-v2',['--model=/jetson-inference/python/training/detection/ssd/models/{}/ssd-mobilenet.onnx'.format(MODEL),'--labels=/jetson-inference/python/training/detection/ssd/models/{}/labels.txt'.format(MODEL),'--input-blob=input_0','--output-cvg=scores','--output-bbox=boxes'])
LABELS_FILE = '/jetson-inference/python/training/detection/ssd/models/{}/labels.txt'.format(MODEL)
#LABELS_FILE = '/ssd500/jetson-inference/data/networks/SSD-Mobilenet-v2/ssd_coco_labels.txt'
#    LABELS_FILE = '/jetson-inference/build/aarch64/bin/networks/SSD-Mobilenet-v2/ssd_coco_labels.txt'
#net_detect = jetson.inference.detectNet("ssd-inception-v2", threshold=0.5)
#net = jetson.inference.imageNet('resnet-152',['--model=/home/rdl-xavier/jetson-inference/python/training/classification/MyTrainedCars/resnet18.onnx','--input_blob=input_0','--output_blob=output_0','--labels=/home/rdl-xavier/jetson-inference/my_models/MyTrainedCars/labels.txt'])
#net = jetson.inference.imageNet('googlenet',['--model=~/jetson-inference/python/training/classification/people/resnet18.onnx','--input_blob=input_0','--output_blob=output_0','--lables=~/jetson-inference/people/labels.txt'])
#net = jetson.inference.imageNet('googlenet')
#net = jetson.inference.imageNet('resnet-18') ## 18, 50, 101, and 152
#net = jetson.inference.imageNet('vgg-19')  ## 16, 19
#net = jetson.inference.imageNet('inception-v4')


#VIDEO_DIRECTORY = '/media/bob/1213-2122/Export_2021-08-26_11_31_44_487/' #'/'
#VIDEO_DIRECTORY = '/media/bob/ssd128/Recordings' #'/'

#DIR_LIST = os.listdir(VIDEO_DIRECTORY)
os.system('clear')
print('AI AUDITOR')

#    print('DATA-SET LIST: ',DIR_LIST)
print()
#print('File List')
#for line in range(len(DIR_LIST)):
#        print('{} {} {}'.format(line, '-'*50, DIR_LIST[line]))

print()
#print('Select video from the file list above: ')
#print('1 ---------------------------- Enter search date ')
#print('2 ---------------------------------- Select file ')
print()
# VIDEO_FILE = int(input('Select number for VIDEO from the File List above: '))
# VIDEO_FILE = '{}/{}'.format(VIDEO_DIRECTORY, DIR_LIST[VIDEO_FILE])
# print('video file: ', VIDEO_FILE)


VIDEO_FILE = '/media/bob/ssd128/Recordings/pvr-21-03-09_10:19:38.639.mp4'
#v_out = getVideo()
#input = jetson.utils.videoSource('csi://0')
#input = jetson.utils.videoSource('rtsp://root:TTItest1@10.4.0.190:554/axis-media/media.amp?videocodec=h264')
#input = jetson.utils.videoSource('rtsp://root:AVCaudit1@10.4.0.187:554/axis-media/media.amp?videocodec=h264')
#input = jetson.utils.videoSource('/dev/video0') ## USB camera
#input = jetson.utils.videoSource('/media/robert/ssd128/axis_2021-03-10_08_59_44_325.mp4') #/ssd500/cars17.mp4') #'/dev/video1')
input = jetson.utils.videoSource(VIDEO_FILE)

def speedTime():
    #speed_time = datetime.datetime.now()
    milliseconds = int(round(time.time() * 1000))
    #speed_time = speed_time.strftime("%f")
    #print('speed time: ', speed_time)
    return milliseconds


def newVideo():
    v_out = getVideo()
    #output = jetson.utils.videoOutput(v_out) ##is_headless
    return v_out

font = jetson.utils.cudaFont()
def collectData():
    location = ''

    count = 0
    global SPEED_TIME1
    global SPEED_TIME2
    global SPEED
    #capture the next image
    img = input.Capture()
    #detections = net.Detect(img, overlay=opt.overlay) overlay options (--overlay=box,labels,conf, and overlay=none)
    #detections  = net_detect.Detect(img, overlay='none')
    detections  = net_detect.Detect(img)
    #print("detected {:d} objects in image".format(len(detections)))
    objects = (len(detections))
    objects = int(objects)
    detection = detections
    #perameter = jetson.inference.detectNet.Detection()
    #print (perameter)
    #print (objects)
    for detection in detections:
        #print('detections: ',detection)
        #net_detect.PrintProfilerTimes()
        class_id_detectNet = int(detection.ClassID)
        Confidence = detection.Confidence
        Left = int(detection.Left)
        Top = int(detection.Top)
        Right = int(detection.Right)
        Bottom = int(detection.Bottom)
        Width = int(detection.Width)
        Height = int(detection.Height)
        Area = int(detection.Area)
        center_x, center_y = detection.Center
        center_x = int(center_x)
        center_y = int(center_y)
        #if objects > 0:
        if class_id_detectNet > 0:
            object_names = open(LABELS_FILE)
            object_name = object_names.readlines()
            object_name = object_name[class_id_detectNet]
            object_nane = object_name.rstrip()
            class_id, confidence = net.Classify(img)
            # find the object description
            class_desc = net.GetClassDesc(class_id)

            #overlay the result on the image
            confidence = int(confidence * 100)
            Confidence = int(Confidence * 100)
            class_id = int(class_id)
            w  = Width
            h = Height
            # In odrer to get the positions of the upper left corner
            x = int(center_x - w/2)
            y = int(center_y - h/2)
            #print ('x_position:{} y_position:{}'.format(x, y))
        
            #Set trigger x or y trigger position here
            if 0 < x < 100:
                x_1 = 1 # start_entry
                logger.info('start_entry')
                #SPEED_TIME1 = get_speed_time()
            else:
                x_1 = 0

            if 200 < y < 600:
                y_1 = 1 # start_entry
                #SPEED_TIME2 = get_speed_time()
            else:
                y_1 = 0

            if 150 < x < 250:
                x_2 = 1 # stop_entry
                logger.info('stop_entry')
            else:
                x_2 = 0

            if 200 < y < 600:
                y_2 = 1 # start_entry
            else:
                y_2 = 0

            if 300 < x < 350:
                x_3 = 1 # start_exit
                logger.info('start_exit')
            else:
                x_3 = 0

            if 200 < y < 600:
                y_3 = 1 # start_entry
            else:
                y_3 = 0
                    
            if 500 < x < 650:
                x_4 = 1 # stop_exit
                logger.info('stop_exit')
            else:
                x_4 = 0

            if 200 < y < 600:
                y_4 = 1 # start_entry
            else:
                y_4 = 0
            # data = (class_id_detectNet,object_name, Confidence,
            # Left,Top,Right,Bottom,Width,Height,Area,center_x,center_y)
            # logger.info(data)


def get_time():
    timer = datetime.now()
    return timer

def get_speed_time():
    timer = time.time()
    return timer


def runInference():
    collectData()

while True:
    runInference()
    #time.sleep(2)
 

            # test = presentsChecker(x_1,x_2,x_3,x_4,y_1,y_2,y_3,y_4)
            # #print('Trigger Message: ',x_1,x_2,x_3,x_4,y_1,y_2,y_3,y_4)
            # test1 = test.presents_checker()
            # test1 = str(test1)
            # if test1 == 'send_trigger':
            #     if y_4 == 1: #class_desc == FILTER1:
            #         if confidence > 0:
            #             v_out, time_stamp = getVideo()
            #             font.OverlayText(img, img.width, img.height, "Time:{} |{:05.2f}% {:s}".format(time_stamp, confidence, class_desc, net.GetNetworkFPS()), 5, 5, font.White, font.Gray40)
            #             font.OverlayText(img, img.width, img.height, "Top:{}".format(Top), 5, 45, font.White, font.Gray40)
            #             font.OverlayText(img, img.width, img.height, "Left:{}".format(Left), 5, 85, font.White, font.Gray40)
            #             font.OverlayText(img, img.width, img.height, "Right:{}".format(Right), 5, 120, font.White, font.Gray40)
            #             font.OverlayText(img, img.width, img.height, "Bottom:{}".format(Bottom), 5, 160, font.White, font.Gray40)
            #             font.OverlayText(img, img.width, img.height, "Height:{}".format(Height), 5, 195, font.White, font.Gray40)
            #             font.OverlayText(img, img.width, img.height, "Width:{}".format(Width), 5, 235, font.White, font.Gray40)
            #             font.OverlayText(img, img.width, img.height, "Area:{}".format(Area), 5, 270, font.White, font.Gray40)
            #             font.OverlayText(img, img.width, img.height, "Center_X:{}".format(x), 5, 305, font.White, font.Gray40)
            #             font.OverlayText(img, img.width, img.height, "Center_Y:{}".format(y), 5, 345, font.White, font.Gray40)
            #             jetson.utils.saveImageRGBA(v_out, img, width, height)

            #             t1 = float(SPEED_TIME1)
            #             t2 = float(SPEED_TIME2)
            #             t_delta = t2 - t1
            #             #print('time delta: ', t_delta)
            #             #CALCULATE SPEED
            #             #SPEED = D/T
            #             distance = 30
            #             #speed = int(distance/t_delta) #meters per second
            #             SPEED = ((distance/t_delta)*0.681818) ##mph
            #             SPEED = int(SPEED)
            #             info_speed = 'Speed: {}'.format(SPEED)
            #             #print('speed-time delta: ', t_delta)
            #             logger.info(info_speed)
            #         else:
            #             speed = 'UNKOWN'
            #         os.chdir(STORAGE_DIRECTORY)
            #         path = (os.getcwd())

            #         object_names = open(LABELS_FILE)
            #         #for line in enumerate(pvr):
            #         object_name = object_names.readlines()
            #         object_name = object_name[class_id_detectNet]
            #         #print('Object name: ',object_name)

            #         location = 'TP2' #GPS
            #         description =  class_id_detectNet
            #         description_id = object_name
            #         #confidence = int(confidence * 100)
            #         color = 0          #vehicle color
            #         if description == 'Car':
            #             axle_count = 2
            #         if description == 'Van':
            #             axle_count = 3
            #         else:
            #             axle_count = 2

            #         #axle_count = x_4 #objects ##
            #         license_plate = 0 #######
            #         rfid = 0 ################
            #         image_path = v_out
            #         lane_id = 0
            #         speed = SPEED
            #         #INSERT INTO DATABASE
            #         data =  (time_stamp, location, description, description_id, Confidence, color, axle_count, license_plate, rfid, speed, lane_id, image_path)
            #         logger.info(data)
            #         #conn.execute('INSERT INTO DATA_AQUISITION2 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', data)
            #         #conn.commit()
            #         #class_id_detectNet = 0
            #         #return description  #testing only

