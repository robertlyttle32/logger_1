#Date: 6/20/2021
#Author: Robert Lyttle

import numpy as np
import cv2
import os
import sys
import urllib.request
import urllib.parse
import urllib.robotparser as rb
import urllib3.request
import datetime
import time
import glob
#import avc_audit_v9 as audit
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
#import tkinter.messagebox
#from tkcalendar import Calendar
from tkinter.filedialog import askopenfilename, asksaveasfilename
import datetime
from tkcalendar import *
from PIL import ImageTk,Image
import threading
from dateutil.relativedelta import relativedelta
import audit_log
from  tkinter import ttk
from datetime import timedelta
from time import strftime
from time import gmtime
import math
import csv
from tkvideo import tkvideo



OPTIONS = 0
METADATA = 5
PVR_FILE = ' ' #'03082132.pvr'
DATE = 0
DATE2 = 0
TIME = 0
TIME1 = 0
PVR_DATA = 0
PVR_FILE = ''
PVR_DATA1 = 0
BANNER = ''
FRAME_NUMBER = 0
TIME_DELTA = 0
EXT = '.mp4'
EXT1 = '.jpg'
pvr_time = 0
video_time = 0
pvr_date = 0
pvr_banner = ''
ban = ''
pvr_count = 0
start_line = 0
frame_num = 0
first_frame = 0
frame_num1 = 0
frame_num = 0
ext_frame_number = 0
start_banner =  ''
play_button_status = 'Play'
offset = 0
trim = 0 #1.05
test_value = 'test'
line_num = 0
line_filler = '_'*40
image_size_scaler = 0.89
RED = 255  # 0 - 255
BLUE = 255 # 0 - 255
GREEN = 255 # 0 - 255
global width
global height
width = 1280 #720
height = 720 #480
time_laps = ''

#Image Banner
x=0
y=640
w=560
h=100
#y = int(height*image_size_scaler)
#w = int(w*image_size_scaler)
#h = int(h*image_size_scaler)
#x,y,w,h = 0,y,560,100

pause = False
forward = False
back = False
play2 = False
skip0 = False
banner_on = False
skip_back = False
start_time = 0
stop_time = 0
count1 = 0
count = 0
record_directory = ''
save_audit = False
detection_trigger = False
PVR_LINE = 0
OFFSET = 0
TRACKER_FRAME = ''
#line = 0
tracker_line = 0
button_status = ''
frame = ''
banner_date = ''
banner_time = ''
banner_lane = ''
banner_dir = ''
banner_length = ''
banner_speed = ''
banner_class = ''
banner_axle = ''
banner_note = ''

#get files
class Auditor:
    def __init__(self, VIDEO_TIME,VIDEO_DATE, PVR_FILE):
        self.VIDEO_TIME = VIDEO_TIME
        self.VIDEO_DATE = VIDEO_DATE
        self.PVR_FILE = PVR_FILE

    #data synchronization
    #get files
class Auditor:
    def __init__(self, VIDEO_TIME,VIDEO_DATE, PVR_FILE):
        self.VIDEO_TIME = VIDEO_TIME
        self.VIDEO_DATE = VIDEO_DATE
        self.PVR_FILE = PVR_FILE

    #data synchronization
    def sync_data():
        try:
            video_start_time = convert_search_time_to_seconds(VIDEO_TIME)
        except NameError:
            #print('Missing VIDEO TIME make sure video file matches naming convention')
            var.set('Missing VIDEO TIME make sure video file matches naming convention')
            messagebox.showinfo("showeinfo", "Missing VIDEO_TIME")
            #time.sleep(1)
            messagebox.destroy()
   
        global pvr_time
        global offset
        global pvr_count
        global pvr_date
        global DATE
        #global count
        pvr_time = 0
        count = 0
        #update
        pvr_file_count = 0
        try:
            #video_start_time = convert_search_time_to_seconds(VIDEO_TIME)
            csv_file = csv.reader(open(PVR_FILE)) #'/home/dev-main/Downloads/Recordings/03041600.pvr','r'))
            for row in csv_file:
                count = count +1
                DATE = row[0]
                row_value = row[1]
                pvr_time = convert_search_time_to_seconds(row_value)
                if VIDEO_DATE == DATE and video_start_time == pvr_time:
                    print(row)
                    print('count: ', count)
                    return count
                elif VIDEO_DATE == DATE and video_start_time < pvr_time:
                    offset = pvr_time - video_start_time - trim
                    print(row)
                    return count
                else:
                    print("File not found", DATE, row_value)
        except IndexError:
            print('Did not find PVR file make sure you have correct video file and retry')
            print('Please waite .... ')
            time.sleep(20)


    #file namer
    def get_video_name():
        get_image_time = datetime.datetime.now()
        microsec = get_image_time.strftime('%f')
        microsec = format(microsec, '.3')
        video_name = get_image_time.strftime("%y-%m-%d_%H:%M:%S")
        video_name = '{}.{}'.format(video_name,microsec)
        return video_name

    def get_pvr_frame(line):
        frame_time = 0
        #pvr_count = 56
        start_line = count
        global frame_number
        next_frame = 0
        try:
            fps = cap.get(cv2.CAP_PROP_FPS)
            fps = float(fps)
            line = line+count
            pvr = open(PVR_FILE)
            pvr_data = pvr.readlines()
            PVR_DATA = pvr_data[line]
            if line > start_line:
                PVR_DATA1 = pvr_data[line] #[line-1]
                PVR_DATA1 = PVR_DATA1.rstrip()
                PVR_DATA1 = PVR_DATA1.split(',')
                TIME = PVR_DATA1[1]
                frame_time = convert_search_time_to_seconds(TIME)
            else:
                TIME = 0
            BANNER = PVR_DATA
            PVR_DATA = PVR_DATA.rstrip()
            PVR_DATA = PVR_DATA.split(',')
            DATE2 = PVR_DATA[0]
            TIME = PVR_DATA[1]
            frame_time = convert_search_time_to_seconds(TIME)
            TIME_DELTA = ((frame_time + (offset + OFFSET)) - pvr_time) # offset adjustment
            #global frame_num
            frame_number = (fps*TIME_DELTA)
            frame_number = int(frame_number)
            next_frame = frame_number+next_frame
            w_1_entry2_13_2.delete(0, END)
            w_1_entry2_13_2.insert(END, next_frame)
            pvr.close()
            return frame_number, BANNER
        except IndexError:
            print('frames exceed lines')
   
    def play_video1(FRAME_NUMBER):
        cap.set(cv2.CAP_PROP_POS_FRAMES, START_FRAME_NUMBER)
        ret, frame = cap.read()
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame,'pvr data goes here Entry time, speed, Direction, Axle count',(100,130),font,1,(255,255,255),2)
        cv2.rectangle(frame,(900,450),(500,200),(0,255,0),6)
        #cv2.imshow('frame',grfay)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            #break
            pass

    def banner_label(a,b,c,d,e,f,g,h,j,k,frame,font,i):
        #i sets postion of banner on screen
        i = int(i)
        font_size = 0.4
        cv2.putText(frame,'Date: '+a,(10+i,50),font,font_size,(BLUE,GREEN,RED),1)
        cv2.putText(frame,'Time: '+b,(10+i,75),font,font_size,(BLUE,GREEN,RED),1)
        cv2.putText(frame,'PVR Line Number: '+k,(10+i,95),font,font_size,(BLUE,GREEN,RED),1)
        cv2.putText(frame,'Lane: '+c,(10+i,115),font,font_size,(BLUE,GREEN,RED),1)
        cv2.putText(frame,'Direction: '+d,(10+i,135),font,font_size,(BLUE,GREEN,RED),1)
        cv2.putText(frame,'Length: '+e,(10+i,155),font,font_size,(BLUE,GREEN,RED),1)
        cv2.putText(frame,'Speed: '+f,(10+i,175),font,font_size,(BLUE,GREEN,RED),1)
        cv2.putText(frame,'Class: '+g,(10+i,195),font,font_size,(BLUE,GREEN,RED),1)
        cv2.putText(frame,'Axle: {} {}'.format(h, j),(10+i,215),font,font_size,(BLUE,GREEN,RED),1)

    def banner_label2(a,b,c,d,e,f,g,h,j,k,frame,font,i):
        #i sets postion of banner on screen
        i = int(i)
        font_size = 0.4
        cv2.putText(frame,'Date: {} | Time: {}'.format(a,b),(10+i,660),font,font_size,(BLUE,GREEN,RED),1)
        cv2.putText(frame,'PVR Line Number: {}'.format(k),(10+i,680),font,font_size,(BLUE,GREEN,RED),1)
        cv2.putText(frame,'Lane: {} | Direction: {} | Length: {} | Speed: {}  mph  | Class: {} | Axle: {} {}'.format(c,d,e,f,g,h,j),(10+i,700),font,font_size,(BLUE,GREEN,RED),1)

    def banner_label3(frame,time_laps,font):
        font_size = 0.4
        i = 985
        #########rt = relativedelta(seconds=time_laps)
        rt = timedelta(seconds=time_laps)
		#print(rt.seconds)
        #time_laps = ('{:02d}:{:02d}:{:02d}:{03d}'.format(int(rt.hours), int(rt.minutes), int(rt.seconds), int(rt.seconds)/1000))
        time_laps = str(datetime.fromtimestamp(rt)+timedelta(hours=-1)).split(' ')[1][:12]
		#cv2.putText(frame,'Date/Time: {}'.format(Auditor.get_video_name()),(10+i,10),font,font_size,(BLUE,GREEN,RED),1)
		#cv2.putText(frame,'Date/Time: {}'.format(time_laps),(10+i,10),font,font_size,(BLUE,GREEN,RED),1)
        return time_laps
        
    def banner_info(line):
        global banner_date
        global banner_time
        global banner_axle
        global banner_dir
        global banner_class
        global banner_lane
        global banner_speed
        global banner_length
        global banner_note
        frame_num, BANNER = Auditor.get_pvr_frame(line)
        BANNER = BANNER.strip()
        #var.set(BANNER)
        BANNER = BANNER.split(',')
        banner_date = BANNER[0]
        banner_time = BANNER[1]
        banner_lane = BANNER[3]
        banner_dir = BANNER[5]
        banner_length = BANNER[6]
        banner_speed = BANNER[7]
        banner_class = BANNER[10]
        banner_axle = BANNER[11]
        banner_note = BANNER[12]
        banner_speed = float(banner_speed)
        banner_speed = banner_speed*2.23694
        banner_speed = int(banner_speed)
        w_1_entry0_10_2.delete(0, END)
        w_1_entry0_10_2.insert(END, BANNER[0])
        w_1_entry5_16_2.delete(0, END)
        w_1_entry5_16_2.insert(END, BANNER[3])
        w_1_entry6_17_2.delete(0, END)
        w_1_entry6_17_2.insert(END, banner_speed)
        w_1_entry7_18_2.delete(0, END)
        w_1_entry7_18_2.insert(END, BANNER[5])
        w_1_entry8_19_2.delete(0, END)
        w_1_entry8_19_2.insert(END, BANNER[10])
        w_1_entry9_20_2.delete(0, END)
        w_1_entry9_20_2.insert(END, BANNER[11])
        w_1_entry10_21_2.delete(0, END)
        w_1_entry10_21_2.insert(END, BANNER[6])
        w_1_entry11_22_2.delete(0, END)
        w_1_entry11_22_2.insert(END, BANNER[12])
        return banner_date,banner_time,banner_lane,banner_dir,banner_length,banner_speed,banner_class,banner_axle,banner_note
    
    def play_video(tracker_line,frame_number,time_laps,next_frame_number,i,count,banner_date,banner_time,banner_lane,banner_dir,banner_length,banner_speed,banner_class,banner_axle,banner_note):
        global frame_num
        global frame
        global detection_trigger
        global banner_on
        global skip_back
        global pause
        font_size = 0.4
        i = 0
        fps = cap.get(cv2.CAP_PROP_FPS)
        fps = int(fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        fourcc = cv2.VideoWriter_fourcc(*'MP4V')
        #while (cap.isOpened()):
        ret, frame = cap.read()
        frame = cv2.resize(frame, (width, height))
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame,'Date/Time: {} {}'.format(banner_date,time_laps),(995,10),font,font_size,(BLUE,GREEN,RED),1)
        if banner_on == True:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0,0,0), -1)
            #cv2.rectangle(frame,(900,450),(500,200),(0,255,0),6)
            Auditor.banner_label2(banner_date,banner_time,banner_lane,banner_dir,banner_length,banner_speed,banner_class,banner_axle,banner_note,pvr_line_number,frame,font,i)
            cv2.imshow('frame', frame)
            
            ###### DEBUG IMAGE DISPLAY ONTO GUI FRAME #######
            # video_label = Label(window)
            # video_label.grid(row=0,column=5)
            # # read video to display on label
            # out = cv2.VideoWriter(str(frame),fourcc, 20.0, (1280,720))
            # player = tkvideo(out, video_label,loop = 1, size = (1280, 720))
            # player.play()

        else:
            cv2.imshow('frame', frame)
            #my_image_display = ImageTk.PhotoImage(Image.open(frame))
       
        if save_audit and pause == True:
            PVR_LINE = tracker_line
            #if frame_number == next_frame_number:
            comments = 'No issues found'
            audit_user = 'Robert Lyttle'
            if pass_fail1 == 'Pass':
                audit_status = pass_fail1
                audit_log.file_format(record_directory+'audit.csv',banner_date,banner_time,banner_lane,banner_dir,banner_length,banner_speed,banner_class,banner_axle,banner_note,count,audit_status,audit_user,comments)
                cv2.imwrite(record_directory+'audit_'+banner_time+str(PVR_LINE)+EXT1, frame)
            if pass_fail1 == 'Fail':
                audit_status = pass_fail1
                banner_speed = 'N/A'
                banner_class = class1
                banner_length = 'N/A'
                comments = w_1_entry16_37_0.get(1.0,'end-1c')
                #inp = inputtxt.get(1.0, "end-1c")
                #lbl.config(text = "Provided Input: "+inp)
                audit_log.file_format(record_directory+'audit.csv',banner_date,time_laps,lane_number1,direction1,banner_length,banner_speed,banner_class,axle_count1,banner_note,count,audit_status,audit_user,comments)		
                cv2.imwrite(record_directory+'audit_'+time_laps+str(PVR_LINE)+EXT1, frame)
            record_audit(False)
            w_1_btn_save_audit_37_1['text'] = 'Saved'
            time.sleep(1)
            w_1_btn_save_audit_37_1['text'] = 'Save Audit'
            w_1_btn_pass_fail_35_0['bg'] ='white'
            w_1_btn_direction_35_1['bg'] = 'white'
            w_1_btn_axle_count_35_2['bg'] = 'white'
            w_1_btn_lane_number_opt_35_3['bg'] = 'white'
            w_1_btn_class_opt_35_4['bg'] = 'white'
            variable1.set(axle_count[0])
            variable2.set(axle_count[0])
            variable3.set(axle_count[0])
            variable4.set(axle_count[0])
            variable5.set(axle_count[0])
            w_1_btn_direction_35_1['state'] = 'normal'
            w_1_btn_axle_count_35_2['state'] = 'normal'
            w_1_btn_lane_number_opt_35_3['state'] = 'normal'
            w_1_btn_class_opt_35_4['state'] = 'normal'
            w_1_entry16_37_0.delete(1.0, 'end-1c')

        #cv2.imshow('frame', frame)
        if banner_on == True:
            stop_time = time_in_milisec()
            time_delta = stop_time-start_time
            print(f'stop_time: {stop_time} - start time: {start_time} = time_delta:{time_delta}')
            if pause == True:
                time_delta = start_time-start_time
            elif time_delta >= 1000:
                banner_on = False
            else:
                banner_on = True

        w_1_entry4_15_2.delete(0, END)
        w_1_entry4_15_2.insert(END, tracker_line+count)
        w_1_entry3_14_2.delete(0, END)
        w_1_entry3_14_2.insert(END, frame_number)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            pass
        if stop == True:
            cap.release()
            cv2.destroyAllWindows()
        #if play == False:
            #cap.release()
            #cv2.destroyAllWindows()

    def record_live_video():
        record_directory = filedialog.askdirectory()
        record_directory = '{}/'.format(record_directory)
        global cap
        cap = cv2.VideoCapture(video_file)
        x,y,w,h = 990,0,290,15
        fourcc = cv2.VideoWriter_fourcc(*'MP4V')
        out = cv2.VideoWriter(record_directory+Auditor.get_video_name()+EXT,fourcc, 20.0, (1280,720))
        while(cap.isOpened()):
            ret, frame = cap.read()
            frame = cv2.resize(frame, (width,height))
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0,0,0), -1)
            if ret==True:
                font = cv2.FONT_HERSHEY_SIMPLEX
                Auditor.banner_label3(frame,time_laps,font)
                out.write(frame)
                cv2.imshow('frame',frame,)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                if stop == True:
                    cap.release()
                    cv2.destroyAllWindows()
                    break
            else:
                # Release everything if job is finished
                cap.release()
                out.release()
                cv2.destroyAllWindows()
                break

	#def tracker(line):
		#pass

#get files
def pvr_file():
	"""Open a file for editing."""
	global PVR_FILE
	PVR_FILE = askopenfilename(filetypes=[("Files", "*.pvr"), ("All Files", "*.*")])
	w_1_entry12_12_2.delete(0, END)
	w_1_entry12_12_2.insert(END, PVR_FILE)
	print('Pvr file: ', PVR_FILE)

#convert_search_time_to_seconds
def convert_search_time_to_seconds(object_time):
	t = object_time
	h,m,s = t.split(':')
	#convert time to seconds
	convert = float(datetime.timedelta(hours=float(h),minutes=float(m),seconds=float(s)).total_seconds())
	return convert

def convert_time_to_seconds(object_time):
	t = str(object_time)
	h,m,s = t.split(':')
	#convert time to seconds
	convert = float(datetime.timedelta(hours=float(h),minutes=float(m),seconds=float(s)).total_seconds())
	return convert

def search_file_for_match(search_date,present_time):
    count = 0
    global banner_on
    csv_file = csv.reader(open(PVR_FILE)) #'/home/dev-main/Downloads/Recordings/03041600.pvr','r'))
    for row in csv_file:
        count = count +1
        file_date = row[0]
        #file_time_seconds = convert_time_to_seconds(row[1])
        file_time_seconds = row[1]
        #time_value_in_seconds = convert_search_time_to_seconds(time_value)
        #present_time = float('%.03f'%present_time)
        #print(f'search date: {search_date} | file time: {file_time_seconds} | present time: {present_time}')
        if search_date == file_date and file_time_seconds == present_time:
            print("CONGRATES IT WORKS", row)

        else:
            pass
            #print(f'seconds from file: {file_time_seconds} | seconds from frame count: {present_time}')
                    #print('%.3f'%present_time)
                    #present_time = '%.3f'%present_time
            #print('converted present time: ',present_time)

                #print("File found", DATE, file_time_seconds)
                #banner_on = True
            #else:
                #banner_on = False
                #print('MO MATCH FOUND ####################')

#get video files
def pvr_video():
	"""Open a file for editing."""
	global video_file
	video_file = askopenfilename(filetypes=[("Files", "*.mp4"), ("All Files", "*.*")])
	print('AVC AUDITOR')
	w_1_entry1_11_2.delete(0, END)
	w_1_entry1_11_2.insert(END, video_file)
	print()
	global cap
	cap = cv2.VideoCapture(video_file)
	print('video file is: ', video_file)
	global video_metadata
	video_metadata = video_file  #'/media/robert/ssd128/2021_04_10_08:19:38.075552.mp4' #video_file
	global fps
	fps = cap.get(cv2.CAP_PROP_FPS) # get frames per second
	global totalframecount
	totalframecount= int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) # get number of frames
	print('frame_per_sec: ', fps)
	print('total_num_frames: ', totalframecount)

os.system('clear')
def play1():
    global play
    global cap
    global back
    global pause
    global stop
    global record
    global forward
    global button_state
    global play_button_status
    play_button_status =''
    #global tracker_line
    global frame_number
    forward = False
    record = False
    stop = False
    pause = False
    back = False
    #skip0 = False
    play = True
    button_state = False
    exit_program = False
    cap = cv2.VideoCapture(video_file)
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(play)

    def convert_seconds_to_time(seconds):
        seconds = seconds % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        milisec = seconds // 1000
        #milisec = "{:03f}".format(milisec)
        #milisec = round(milisec, 3)
        #time_output = ("%d:%02d:%02d" % (hour, minutes, seconds))
        return print(f'{hour}:{minutes}:{seconds}:{milisec}')

    def run1():
        player_speed = 0
        i = 0
        global pvr_line_number
        global detection_trigger
        global pause
        global banner_on
        global start_time
        global skip_back
        banner_date = ''
        banner_time = ''
        banner_lane = ''
        banner_dir = ''
        banner_length = ''
        banner_speed = ''
        banner_class = ''
        banner_axle = ''
        banner_note = ''
        pvr_line_number = 0
        count = Auditor.sync_data()
        start_frame_number = Auditor.get_pvr_frame(count)[0]
        frame_number = start_frame_number
        next_frame_number = Auditor.get_pvr_frame(count+1)[0]
        banner_lane = Auditor.banner_info(count)[2]
        while True:

            test_test = 1
            if test_test == 1:
                pvr_line_number = count
                t = (frame_number/fps)+pvr_time - offset
                rt = relativedelta(seconds=t)                
                time_laps = ('{:02d}:{:02d}:{:02d}.{}'.format(int(rt.hours), int(rt.minutes), int(rt.seconds), str('%.03f'%t).split(".")[1]))
                #search_file_for_match(VIDEO_DATE,time_laps)
                if next_frame_number >= frame_number - (fps):
                    if banner_lane == '1':
                        i = 0 #180
                    if banner_lane == '2':
                        i = 0
                if frame_number > next_frame_number and forward == True: # forward
                    count = int(count + 1)
                    if pause != True:
                        start_time = time_in_milisec()
                        banner_date,banner_time,banner_lane,banner_dir,banner_length,banner_speed,banner_class,banner_axle,banner_note = Auditor.banner_info(count-1)
                        banner_on = True
                        my_table.tag_configure('oddrow', background='white')
                        my_table.tag_configure('evenrow', background='lightblue')
                        if count % 2 == 0:
                            my_table.insert(parent='',index=0,text='',values=(count,banner_date,banner_time,banner_lane,banner_dir,banner_speed,banner_length,banner_axle,banner_class,banner_note), tags=('evenrow'))
                        else:
                            my_table.insert(parent='',index=0,text='',values=(count,banner_date,banner_time,banner_lane,banner_dir,banner_speed,banner_length,banner_axle,banner_class,banner_note),tags=('oddrow',))
                        next_frame_number = Auditor.get_pvr_frame(count)[0]

                if frame_number < next_frame_number and back == True: # back
                    count = int(count - 1)
                    if pause != True:
                        start_time = time_in_milisec()
                        banner_date,banner_time,banner_lane,banner_dir,banner_length,banner_speed,banner_class,banner_axle,banner_note = Auditor.banner_info(count-1)
                        banner_on = True
                        my_table.tag_configure('oddrow', background='white')
                        my_table.tag_configure('evenrow', background='lightblue')
                        if count % 2 == 0:
                            my_table.insert(parent='',index=0,text='',values=(count,banner_date,banner_time,banner_lane,banner_dir,banner_speed,banner_length,banner_axle,banner_class,banner_note),tags=('evenrow',))
                        else:
                            my_table.insert(parent='',index=0,text='',values=(count,banner_date,banner_time,banner_lane,banner_dir,banner_speed,banner_length,banner_axle,banner_class,banner_note),tags='oddrow')
                        next_frame_number = Auditor.get_pvr_frame(count)[0]

                if frame_number > next_frame_number and play == True: # forward
                    count = int(count + 1)
                    if pause != True:
                        start_time = time_in_milisec()
                        banner_date,banner_time,banner_lane,banner_dir,banner_length,banner_speed,banner_class,banner_axle,banner_note = Auditor.banner_info(count-1)
                        banner_on = True
                        my_table.tag_configure('oddrow', background='white')
                        my_table.tag_configure('evenrow', background='lightblue')
                        if count % 2 == 0:
                            my_table.insert(parent='',index=0,text='',values=(count,banner_date,banner_time,banner_lane,banner_dir,banner_speed,banner_length,banner_axle,banner_class,banner_note),tags=('evenrow',))
                            #if t>convert_time_to_seconds(banner_time) and t-convert_time_to_seconds(banner_time) < t-convert_time_to_seconds(banner_time)+.0001:
                                #print("CONGRATES IT WORKS")
                        else:
                            my_table.insert(parent='',index=0,text='',values=(count,banner_date,banner_time,banner_lane,banner_dir,banner_speed,banner_length,banner_axle,banner_class,banner_note),tags=('oddrow',))
                        next_frame_number = Auditor.get_pvr_frame(count)[0]
                        #print(f'converted time from file to seconds: {convert_time_to_seconds(banner_time)} time in seconds using video fps: {t}')
                        #print(f'{t-convert_time_to_seconds(banner_time)}')
                        
                Auditor.play_video(count,frame_number,time_laps,next_frame_number,i,count,banner_date,banner_time,banner_lane,banner_dir,banner_length,banner_speed,banner_class,banner_axle,banner_note)
            count1 = 0
            if forward == True:
                w_1_btn_forward_24_2['fg'] = 'green'
                w_1_btn_pause_24_1['fg'] = 'black'
                #w_1_btn_tracker_25_0['fg'] = 'red'
                w_1_btn_back_24_0['fg'] = 'black'
                w_1_btn_pause_24_1['text'] = 'PAUSE'
                player_speed=fps
                frame_number = frame_number+player_speed
            else:
                w_1_btn_forward_24_2['fg'] = 'black'
    
            if back == True and frame_number >= start_frame_number:
                w_1_btn_pause_24_1['fg'] = 'black'
                #w_1_btn_tracker_25_0['fg'] = 'red'
                w_1_btn_back_24_0['fg'] = 'green'
                player_speed=fps
                frame_number = frame_number-player_speed
            else:
                w_1_btn_back_24_0['fg'] = 'black'
    
            if pause == True:
				#w_1_btn_pause_24_1['fg'] = 'green'
                w_1_btn_forward_24_2['fg'] = 'black'
                w_1_btn_back_24_0['fg'] = 'black'
                w_1_btn_pause_24_1['text'] = 'PLAY'
                player_speed=0
                frame_number = frame_number+player_speed
    
            if pause == False:
                #w_1_btn_pause_24_1['fg'] = 'green'
                w_1_btn_pause_24_1['text'] = 'PAUSE'
                player_speed=2
                frame_number = frame_number+player_speed
            
            # if skip_back == True:
            #     frame_number = frame_number-2
			
            if stop != True:
                w_1_btn_pause_24_1['fg'] = 'green'
                w_1_btn_play_23_4['fg'] = 'white'
                w_1_btn_play_23_4['bg'] = 'green'
                w_1_btn_play_23_4['text'] = 'Running...'
                w_1_btn_play_23_4['state'] = 'disable'
                w_1_btn_open_23_0['state'] = 'disable'
                w_1_btn_pvrfile_23_1['state'] = 'disable'
                w_1_btn_set_date_23_2['state'] = 'disable'

            else:
                w_1_btn_play_23_4['bg'] = 'red'
                w_1_btn_play_23_4['fg'] = 'white'
                w_1_btn_pause_24_1['fg'] = 'black' 
                w_1_btn_pause_24_1['text'] = 'PLAY / PAUSE'
				   
            if exit_program == True:
                break
            #print(f'BANNER TIME: {banner_time} | Time set to search: {VIDEO_TIME}')
            #print(f'converted time from file to seconds: {convert_time_to_seconds(banner_time)} time in seconds using video fps: {t}')
            #######Auditor.play_video(count,frame_number,time_laps,next_frame_number,i,count,banner_date,banner_time,banner_lane,banner_dir,banner_length,banner_speed,banner_class,banner_axle,banner_note)
            #my_table.tag_configure('row', background='white')

    thread = threading.Thread(target=run1)
    thread.start()
    print(play)

def time_in_milisec():
    #speed_time = datetime.datetime.now()
    milliseconds = int(round(time.time() * 1000))
    #speed_time = speed_time.strftime("%f")
    #print('speed time: ', speed_time)
    return milliseconds

def pause():
    global pause
    global back
    global forward
    global play
    global save_audit
    forward = False
    back = False
    pause = not pause
    if pause == False:
        play = True
    if pause == True:
        save_audit = False

def skip_back():
    global skip_back
	#skip_back = not skip_back
	#if skip0 == True:
		#w_1_btn_tracker_25_0['fg'] = 'green'
	#else:
		#w_1_btn_tracker_25_0['fg'] = 'red'
    skip_back = True
    print ('Skip', skip_back)

def back():
    global back
    global pause
    global count1
    global forward
    global play
    forward = False
    pause = False
    back = not back
    if back == True:
        play = False
    count1 = -10
    print('Back: ', count1)

def forward():
    global forward
    global count1
    global pause
    global back
    global play
    back = False
    pause = False
    forward = not forward
    if forward == True:
        play = False
    count1 = 10
    print('Forward: ' , count1)

def record():
	global record
	global stop
	global back
	global pause
	global play
	global forward
	forward = False
	play = True
	pause = False
	back = False
	record = True
	print('processing....')
	def run2():
		Auditor.record_live_video()
		print(record)
	thread2 = threading.Thread(target=run2)
	thread2.start()

def add_bkdir():
	global record_directory
	record_directory = filedialog.askdirectory()
	record_directory = '{}/'.format(record_directory)

def record_audit(object):
	global save_audit
	save_audit = object #not save_audit
	print('save_audit')

def add_camera():
	global camera
	camera = w_1_entry1_11_2.get()
	print('Camera: ',camera)
	w_1_entry1_11_2.delete(0, END)

def stop():
	global stop
	global pause
	global back
	global play
	global forward
	global record
	record = False
	forward = False
	back = False
	pause = True
	message = messagebox.askquestion("Stop Program", "Are you sure?")
	print(message)
	if message == 'no':
		#messagebox.destroy()
		pass
	elif message == 'yes':
		w_1_entry2_13_2.delete(0, END)
		w_1_entry3_14_2.delete(0, END)
		w_1_entry4_15_2.delete(0, END)
		w_1_entry5_16_2.delete(0, END)
		w_1_entry6_17_2.delete(0, END)
		w_1_entry7_18_2.delete(0, END)
		w_1_entry8_19_2.delete(0, END)
		w_1_entry9_20_2.delete(0, END)
		w_1_entry10_21_2.delete(0, END)
		w_1_entry11_22_2.delete(0, END)
		w_1_btn_play_23_4['text'] = 'START Audit'
		w_1_btn_play_23_4['state'] = 'normal'
		w_1_btn_open_23_0['state'] = 'normal'
		w_1_btn_pvrfile_23_1['state'] = 'normal'
		w_1_btn_set_date_23_2['state'] = 'normal'
		w_1_btn_direction_35_1['state'] = 'normal'
		w_1_btn_axle_count_35_2['state'] = 'normal'
		w_1_btn_lane_number_opt_35_3['state'] = 'normal'
		w_1_btn_class_opt_35_4['state'] = 'normal'
		w_1_btn_tracker_25_0['fg'] = 'black'
		w_1_btn_forward_24_2['fg'] = 'black'
		w_1_btn_back_24_0['fg'] = 'black'
		w_1_btn_pause_24_1['fg'] = 'black'
		w_1_btn_pass_fail_35_0['bg'] ='white'
		w_1_btn_direction_35_1['bg'] = 'white'
		w_1_btn_axle_count_35_2['bg'] = 'white'
		w_1_btn_lane_number_opt_35_3['bg'] = 'white'
		w_1_btn_class_opt_35_4['bg'] = 'white'
		w_1_entry16_37_0.delete(1.0, 'end-1c')
		variable1.set(axle_count[0])
		variable2.set(axle_count[0])
		variable3.set(axle_count[0])
		variable4.set(axle_count[0])
		variable5.set(axle_count[0])
		play = False
		stop = True
		window.destroy()

def exit():
	global stop
	global exit_program
	global pause
	global back
	global play
	global forward
	global record
	pause = True
	message = messagebox.askquestion("Exit Program", "Are you sure?")
	if message == 'no':
		pass
	elif message == 'yes':
		record = False
		forward = False
		play = False
		back = False
		stop = True
		exit_program = True
		w_1_entry1_11_2.delete(0, END)
		w_1_entry2_13_2.delete(0, END)
		w_1_entry3_14_2.delete(0, END)
		print(stop)
		cv2.destroyAllWindows()
		window.destroy()
	
def set_date():
	# Create Object
	calendar = Tk()
	# Set geometry
	calendar.geometry("600x400")
	calendar.title('Audit date')
	# Add Calender
	cal = Calendar(calendar, selectmode = 'day', year = 2021, month = 5, day = 22)
	cal.grid(row=0, column=0, sticky='enw', padx=20, pady=20)
	#date.config(text = "Selected Date is: " + cal.get_date())
 
	def grad_date():
		date.config(text = 'Selected date is: ' + cal.get_date())
		#print('Date: ',cal.get_date())
		video_date = cal.get_date()
		month, day, year = video_date.split('/')
		global VIDEO_DATE
		VIDEO_DATE  = '{}/{}/{}'.format(day.zfill(2), month.zfill(2), year)
		w_1_entry0_10_2.delete(0, END)
		w_1_entry0_10_2.insert(END, VIDEO_DATE)
		print('Date: ', VIDEO_DATE)
		#calendar.destroy()
	# Add Button and Label
	calendar_btn_sel = Button(calendar, text = "Set Date", command = grad_date)
	calendar_btn_sel.grid(row=2, column=0, sticky='enw', padx=20, pady=2)
	date = Label(calendar, text = "")
	date.grid(row=3, column=0, sticky='enw', padx=20, pady=2)
	time_entries = []
 
	def set_time():
		width = 0
		entry_list = ' '
		for entries in time_entries:
			entry_list = entry_list + str(entries.get()) + '\n'
			#cal_label.config(text=entry_list)
		print(time_entries[0].get()) #to return a value from a specific column
		HOUR = time_entries[0].get()
		MINUTE = time_entries[1].get()
		SECONDS = time_entries[2].get()
		MILISECONDS = time_entries[3].get()
		global VIDEO_TIME
		VIDEO_TIME = '{}:{}:{}.{}'.format(HOUR.zfill(2), MINUTE.zfill(2), SECONDS.zfill(2), MILISECONDS.zfill(3))
		print('This is the new time: ',VIDEO_TIME)

	time_list = ['H', 'M', 'S', 'Milisec']
	for x in range(4):
		cal_label_header = Label(calendar, text=time_list[x])
		cal_label_header.grid(row=5, column=x, sticky='enw', padx=20, pady=2)
		spinbox = Spinbox(calendar, width=2, from_=0, to=999)
		spinbox.grid(row=7, column=x, sticky='enw', padx=1, pady=2)
		time_entries.append(spinbox)
	cal_btn = Button(calendar, text='Set time', command=set_time)
	cal_btn.grid(row=8, column=0, sticky='enw', padx=20, pady=2)
	cal_btn_close = Button(calendar, text = "Close", command=calendar.destroy)
	cal_btn_close.grid(row=9, column=0, sticky='enw', padx=20, pady=2)
	# Excecute Tkinter
	calendar.mainloop()

window = Tk()
window.title("AVC Audit")
window.geometry('800x1080')
#window.rowconfigure(0, minsize=110, weight=1)
#window.columnconfigure(0, minsize=110, weight=1)
#tkinter.messagebox.showinfo("Enter: PVR_file, Set_date, PVR_Video, then press START Audit")
w_1_my_img = ImageTk.PhotoImage(Image.open(r'/home/dev-main/my_logo1.png'))
w_1_my_logo = Label(image = w_1_my_img)

# my_image_display = ImageTk.PhotoImage(Image.open(frame))
# my_image_label = Label(image=my_image_display)
# #display label on screen
# my_image_label.grid_forget()
# my_image_label.grid(row=0, column=5, columnspan=3)

#w_1_my_frame = ImageTk.PhotoImage(Image.open('test_image.png'))
#w_1_my_frame_logo = Label(image = w_1_my_frame)


my_table = ttk.Treeview(window)
my_table['columns'] = ('column_0','column_1','column_2','column_3','column_4','column_5','column_6','column_7','column_8','column_9')

my_table.column("#0", width=0,  stretch=NO)
my_table.column("column_0",anchor=CENTER, width=80)
my_table.column("column_1",anchor=CENTER,width=80)
my_table.column("column_2",anchor=CENTER,width=80)
my_table.column("column_3",anchor=CENTER,width=80)
my_table.column("column_4",anchor=CENTER,width=80)
my_table.column("column_5",anchor=CENTER,width=80)
my_table.column("column_6",anchor=CENTER,width=80)
my_table.column("column_7",anchor=CENTER,width=80)
my_table.column("column_8",anchor=CENTER,width=80)
my_table.column("column_9",anchor=CENTER,width=80)

my_table.heading("#0",text="",anchor=CENTER)
my_table.heading("column_0",text="Line Id",anchor=CENTER)
my_table.heading("column_1",text="Date",anchor=CENTER)
my_table.heading("column_2",text="Time",anchor=CENTER)
my_table.heading("column_3",text="Lane",anchor=CENTER)
my_table.heading("column_4",text="Direction",anchor=CENTER)
my_table.heading("column_5",text="Speed",anchor=CENTER)
my_table.heading("column_6",text="Length",anchor=CENTER)
my_table.heading("column_7",text="Axle",anchor=CENTER)
my_table.heading("column_8",text="Class",anchor=CENTER)
my_table.heading("column_9",text="Note",anchor=CENTER)



#my_table.insert(parent='',index='end',iid=0,text='',values=('1','Ninja','101','Oklahoma', 'Moore'))
# my_table.insert(parent='',index='end',iid=1,text='',values=('2','Ranger','102','Wisconsin', 'Green Bay'))
# my_table.insert(parent='',index='end',iid=2,text='',values=('3','Deamon','103', 'California', 'Placentia'))
# my_table.insert(parent='',index='end',iid=3,text='',values=('4','Dragon','104','New York' , 'White Plains'))
# my_table.insert(parent='',index='end',iid=4,text='',values=('5','CrissCross','105','California', 'San Diego'))
# my_table.insert(parent='',index='end',iid=5,text='',values=('6','ZaqueriBlack','106','Wisconsin' , 'TONY'))

#my_table.grid(row=38, column=0) #pack()

#ws.mainloop()




var = StringVar()
w_1_my_label0_0_1 = Label(window, textvariable=var, relief=RAISED )
w_1_my_label1_0_1 = Label(window, textvariable=var)
w_1_my_label_header_1_0 =Label(window, text='AUDITOR1')
w_1_my_label2_10_0 = Label(window, text="Date")
w_1_my_label3_11_0 = Label(window, text="PVR Video")
w_1_my_label4_12_0 = Label(window, text="PVR File")
w_1_my_label5_13_0 = Label(window, text="Next PVR")
w_1_my_label6_14_0 = Label(window, text="Frame Number")
w_1_my_label7_15_0 = Label(window, text="PVR Line")
w_1_my_label8_16_0 = Label(window, text="Lane Number")
w_1_my_label9_17_0 = Label(window, text="Speed")
w_1_my_label10_18_0 = Label(window, text="Direction")
w_1_my_label11_19_0 = Label(window, text="Class")
w_1_my_label12_20_0 = Label(window, text="Axle")
w_1_my_label13_21_0 = Label(window, text="Length")
w_1_my_label14_22_0 = Label(window, text="Note")

offset_entries = []
def offset_trim():
	global OFFSET
	entry_list = ''
	for entries in offset_entries:
		entry_list = entry_list + str(entries.get()) + '\n'
	#print(offset_entries[0].get()) #to return a value from a specific column
 
	OFFSET = offset_entries[0].get()
	OFFSET = int(OFFSET)/100
	print('OFFSET: ', OFFSET)
	trim_label = Label(window, text=OFFSET)
	trim_label.grid(row=4, column=2, sticky='enw', padx=20)
 		
for x_offset in range(1):
	TRIM_LABEL = OFFSET
	offset_label = Label(window, text='OFFSET TRIM')
	offset_label.grid(row=4, column=x_offset, sticky='enw', padx=20)

	offset_spinbox = Spinbox(window, width=2, from_=0, to=100)
	offset_spinbox.grid(row=4, column=x_offset, sticky='enw', padx=1)
	offset_entries.append(offset_spinbox)
 	
offset_btn = Button(window, text='Set offset trim', command=offset_trim)
offset_btn.grid(row=4, column=0, sticky='wn', pady=20)

pass_fail = ['Select Option','Pass','Fail']
variable1 = StringVar(window)
variable1.set(pass_fail[0]) # default value
def option_pass_fail():
    global pass_fail1
    print ("value is:" + variable1.get())
    pass_fail1 = variable1.get()
    w_1_btn_pass_fail_35_0['bg'] ='green'
    if pass_fail1 == 'Pass':
        w_1_btn_direction_35_1['state'] = 'disable'
        w_1_btn_axle_count_35_2['state'] = 'disable'
        w_1_btn_lane_number_opt_35_3['state'] = 'disable'
        w_1_btn_class_opt_35_4['state'] = 'disable'
        my_table.tag_configure('passrow', background='lightgreen')
        my_table.insert(parent='',index=0,text='',values=(count,banner_date,banner_time,banner_lane,banner_dir,banner_speed,banner_length,banner_axle,banner_class,banner_note), tags=('passrow'))
    else:
        w_1_btn_direction_35_1['state'] = 'normal'
        w_1_btn_axle_count_35_2['state'] = 'normal'
        w_1_btn_lane_number_opt_35_3['state'] = 'normal'
        w_1_btn_class_opt_35_4['state'] = 'normal'
        my_table.tag_configure('failrow', background='#FF4500') #python color constant
        my_table.insert(parent='',index=0,text='',values=(count,banner_date,banner_time,banner_lane,banner_dir,banner_speed,banner_length,banner_axle,banner_class,banner_note), tags=('failrow'))

direction = ['Select Option','F','R']
variable2 = StringVar(window)
variable2.set(direction[0]) # default value
def direction_f_r():
	global direction1
	print ("value is:" + variable2.get())
	direction1 = variable2.get()
	w_1_btn_direction_35_1['bg'] = 'green'

axle_count = ['Select Option','1','2','3','4','5','6','7','8','9','10']
variable3 = StringVar(window)
variable3.set(axle_count[0]) # default value
def axle_count_btn():
	global axle_count1
	print ("value is:" + variable3.get())
	axle_count1 = variable3.get()
	w_1_btn_axle_count_35_2['bg'] = 'green'

lane_number_opt = ['Select Option','1','2','3','4','5','6','7','8','9','10']
variable4 = StringVar(window)
variable4.set(lane_number_opt[0]) # default value
def lane_number_btn():
	global lane_number1
	print ("value is:" + variable4.get())
	lane_number1 = variable4.get()
	w_1_btn_lane_number_opt_35_3['bg'] = 'green'

class_opt = ['Select Option','1','2','3','4','5','6','7','8','9','10']
variable5 = StringVar(window)
variable5.set(class_opt[0]) # default value
def class_btn():
	global class1
	print ("value is:" + variable5.get())
	class1 = variable5.get()
	w_1_btn_class_opt_35_4['bg'] = 'green'

# tkinter.messagebox.showinfo(title=None, message=None, **options)
# Warning message boxes

# tkinter.messagebox.showwarning(title=None, message=None, **options)
# tkinter.messagebox.showerror(title=None, message=None, **options)
# Question message boxes

# tkinter.messagebox.askquestion(title=None, message=None, **options)
# tkinter.messagebox.askokcancel(title=None, message=None, **options)
# tkinter.messagebox.askretrycancel(title=None, message=None, **options)
# tkinter.messagebox.askyesno(title=None, message=None, **options)
# tkinter.messagebox.askyesnocancel(title=None, message=None, **options)¶


#entry box
#window = Frame(window, relief=RAISED, bd=2)
w_1_entry0_10_2 = Entry(window, width=10)  #Date
w_1_entry1_11_2 = Entry(window, width=10) #camera path 100
#w_1_entry1_11_2 = Label(window, text='camera path') #Entry(window, width=10) #camera path 100
w_1_entry2_13_2 = Entry(window, width=10) #next frame
w_1_entry3_14_2 = Entry(window, width=10) #current frame
w_1_entry4_15_2 = Entry(window, width=10) #pvr line number
w_1_entry5_16_2 = Entry(window, width=10) #lane number
w_1_entry6_17_2 = Entry(window, width=10) #speed
w_1_entry7_18_2 = Entry(window, width=10) #direction
w_1_entry8_19_2 = Entry(window, width=10) #
w_1_entry9_20_2 = Entry(window, width=10)
w_1_entry10_21_2 = Entry(window, width=10)
w_1_entry11_22_2 = Entry(window, width=10)
w_1_entry12_12_2 = Entry(window, width=10) #PVR_FILE 100
w_1_entry16_37_0 = Text(window, height=10, width=10) #audit comments

#buttons
#button = Button(tkWindow, text = 'Submit', bg='blue', fg='white')
#button['state'] = tk.DISABLED
w_1_btn_open_23_0 = Button(window, text="Import video", state='normal', command=pvr_video) 
w_1_btn_play_23_4 = Button(window, text="START Audit",bg="red",fg="white", state='normal',command=play1) # Start Audit
w_1_btn_pause_24_1 = Button(window, text="PLAY / PAUSE", command=pause)
w_1_btn_tracker_25_0 = Button(window, text="<<Skip", fg='black', command=skip_back)
w_1_btn_back_24_0 = Button(window, text="<<", fg='black', command=back)
w_1_btn_forward_24_2 = Button(window, text=">>", fg='black', command=forward)
w_1_btn_audit_dir_23_3 = Button(window, text="Audit Dir", command=add_bkdir)
w_1_btn_record_24_3 = Button(window, text="Record", command=record)
w_1_btn_save_audit_37_1 = Button(window, text="Save Audit", command=lambda: record_audit(True))
w_1_btn_stop_24_4 = Button(window, text="Stop", command=stop)
w_1_btn_set_date_23_2 = Button(window, text = "Select Date", state='normal', command = set_date)
w_1_btn_pvrfile_23_1 = Button(window, text="Import PVR file", state='normal', command=pvr_file)
w_1_btn_add_camera_25_3 = Button(window, text="Add Camera", command=add_camera)
w_1_btn_exit_25_4 = Button(window, text="Exit", command=exit)

#options button
w_1_pass_fail_label15_33_0 = Label(window, text="Pass/Fail")
w_1_btn_pass_fail_34_0 = OptionMenu(window, variable1, *pass_fail)
w_1_btn_pass_fail_35_0 = Button(window, text="Set", bg='white', state='normal', command=option_pass_fail)

w_1_direction_label16_33_1 = Label(window, text="Direction")
w_1_btn_direction_34_1 = OptionMenu(window, variable2, *direction)
w_1_btn_direction_35_1 = Button(window, text="Set", bg='white', state='normal', command=direction_f_r)

w_1_axle_count_label17_33_2 = Label(window, text="Axle Count")
w_1_btn_axle_count_34_2 = OptionMenu(window, variable3, *axle_count)
w_1_btn_axle_count_35_2 = Button(window, text="Set", bg='white', state='normal', command=axle_count_btn)

w_1_lane_number_label18_33_3 = Label(window, text="Lane Number")
w_1_btn_lane_number_opt_34_3 = OptionMenu(window, variable4, *lane_number_opt)
w_1_btn_lane_number_opt_35_3 = Button(window, text="Set", bg='white', state='normal', command=lane_number_btn)

w_1_btn_comments_label20_36_0 = Label(window, text="Comments")
w_1_btn_class_opt_label19_33_4 = Label(window, text="Class")
w_1_btn_class_opt_34_4 = OptionMenu(window, variable5, *class_opt)
w_1_btn_class_opt_35_4 = Button(window, text="Set", bg='white', state='normal', command=class_btn)




#command=lambda: button_click(1)
#buttons
#btn_play.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
w_1_btn_open_23_0.grid(row=23, column=0, sticky="wse", padx=5) #Import Video "wse"
w_1_btn_play_23_4.grid(row=23, column=4, sticky="wse", padx=5)
w_1_btn_pause_24_1.grid(row=24, column=1, sticky="wse", padx=5)
w_1_btn_back_24_0.grid(row=24, column=0, sticky="wse", padx=5)
w_1_btn_forward_24_2.grid(row=24, column=2, sticky="wse", padx=5)
w_1_btn_tracker_25_0.grid(row=25, column=0, sticky="wse", padx=5)
w_1_btn_stop_24_4.grid(row=24, column=4, sticky="wse", padx=5)
w_1_btn_set_date_23_2.grid(row=23, column=2, sticky="wse", padx=5)
w_1_btn_pvrfile_23_1.grid(row=23, column=1, sticky="wse", padx=5)
w_1_btn_add_camera_25_3.grid(row=25, column=3, sticky="wse", padx=5)
w_1_btn_audit_dir_23_3.grid(row=23, column=3, sticky="wse", padx=5)
w_1_btn_record_24_3.grid(row=24, column=3, sticky='wse', padx=5) 
w_1_btn_save_audit_37_1.grid(row=37, column=1, sticky='wse', padx=5)
w_1_btn_exit_25_4.grid(row=25, column=4, sticky="wse", padx=5)

#options button
w_1_btn_pass_fail_34_0.grid(row=34, column=0, sticky="wse", padx=5) #pass fail option display
w_1_btn_pass_fail_35_0.grid(row=35, column=0, sticky="wse", padx=5) #Pass/Fail

w_1_btn_direction_34_1.grid(row=34, column=1, sticky="wse", padx=5) #direction option display
w_1_btn_direction_35_1.grid(row=35, column=1, sticky="wse", padx=5) #direction set button

w_1_btn_axle_count_34_2.grid(row=34, column=2, sticky="wse", padx=5) #axle_count option display
w_1_btn_axle_count_35_2.grid(row=35, column=2, sticky="wse", padx=5) #axle count button

w_1_btn_lane_number_opt_34_3.grid(row=34, column=3, sticky="wse", padx=5) #lane number option display
w_1_btn_lane_number_opt_35_3.grid(row=35, column=3, sticky="wse", padx=5) #lane number set button

w_1_btn_class_opt_34_4.grid(row=34, column=4, sticky="wse", padx=5) #class option display
w_1_btn_class_opt_35_4.grid(row=35, column=4, sticky="wse", padx=5) #class set button

#entry box
w_1_entry0_10_2.grid(row=1, column=2, sticky="wse", padx=5)  #Date row 10, column 2 "wn"
w_1_entry1_11_2.grid(row=2, column=1, sticky="wse", padx=5)  #Camera Path row 11 column 2
w_1_entry12_12_2.grid(row=3, column=2, sticky="wse", padx=5) #PVR File row 12 column 2
w_1_entry2_13_2.grid(row=13, column=2, sticky="wse", padx=5)  #Next Frame
w_1_entry3_14_2.grid(row=14, column=2, sticky="wse", padx=5)  #Current Frame
w_1_entry4_15_2.grid(row=15, column=2, sticky="wse", padx=5)  #PVR Line Number
w_1_entry5_16_2.grid(row=16, column=2, sticky="wse", padx=5)  #lane Number
w_1_entry6_17_2.grid(row=17, column=2, sticky="wse", padx=5)  #Speed
w_1_entry7_18_2.grid(row=18, column=2, sticky="wse", padx=5)  #Direction
w_1_entry8_19_2.grid(row=19, column=2, sticky="wse", padx=5)  #
w_1_entry9_20_2.grid(row=20, column=2, sticky="wse", padx=5)
w_1_entry10_21_2.grid(row=21, column=2, sticky="wse", padx=5)
w_1_entry11_22_2.grid(row=22, column=2, sticky="wse", padx=5)
w_1_entry16_37_0.grid(row=37, column=0, sticky="wse", padx=5) #audit comments 

#labels
w_1_my_label_header_1_0.grid(row=1, column=0, sticky='wn', padx=5)  #Header
w_1_my_label2_10_0.grid(row=1, column=1, sticky='wn', padx=5)      #Date row 10, column 0
w_1_my_label3_11_0.grid(row=2, column=0, sticky='wn', padx=5)      #PVR Video row 11 column 0
w_1_my_label4_12_0.grid(row=3, column=1, sticky='wn', padx=5)      #PVR File row 12 column 0
w_1_my_label5_13_0.grid(row=13, column=0, sticky='wn', padx=5)      #Next PVR
w_1_my_label6_14_0.grid(row=14, column=0, sticky='wn', padx=5)      #Frame Number
w_1_my_label7_15_0.grid(row=15, column=0, sticky='wn', padx=5)      #PVR Line
w_1_my_label8_16_0.grid(row=16, column=0, sticky='wn', padx=5)      #Lane Number
w_1_my_label9_17_0.grid(row=17, column=0, sticky='wn', padx=5)      #Speed
w_1_my_label10_18_0.grid(row=18, column=0, sticky='wn', padx=5)     #Direction

w_1_my_label11_19_0.grid(row=19, column=0, sticky='wn', padx=5)     #Class
w_1_my_label12_20_0.grid(row=20, column=0, sticky='wn', padx=5)     #Axle
w_1_my_label13_21_0.grid(row=21, column=0, sticky='wn', padx=5)     #Length
w_1_my_label14_22_0.grid(row=22, column=0, sticky='wn', padx=5)     #Note
w_1_my_logo.grid(row=0, column=0)                       #Logo sticky='w'
#w_1_my_frame_logo.grid(row=24, column=4, sticky='w')
w_1_pass_fail_label15_33_0.grid(row=33, column=0, sticky='wse', padx=5)
w_1_direction_label16_33_1.grid(row=33, column=1, sticky='wse', padx=5)
w_1_axle_count_label17_33_2.grid(row=33, column=2, sticky='wse', padx=5)
w_1_lane_number_label18_33_3.grid(row=33, column=3, sticky='wse', padx=5)
w_1_btn_class_opt_label19_33_4.grid(row=33, column=4, sticky='wse', padx=5)
w_1_btn_comments_label20_36_0.grid(row=36, column=0, sticky='wse', padx=5)

#Tables
my_table.grid(row=38, column=0) #pack()

#create window
window.mainloop()



