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
#from tkcalendar import Calendar
from tkinter.filedialog import askopenfilename, asksaveasfilename
import datetime
from tkcalendar import *
from PIL import ImageTk,Image
import threading


#import datepicker_time as datepicker
#import time_converter1 as converter
#from uncertainties import ufloat

#from mp4file.mp4file import Mp4File
#import atom.http_core, atom.core

#pip3 install atom
#pip3 install mp4file
#pip install urllib

#04/03/21,16:00:35.137

OPTIONS = 0
METADATA = 5
PVR_FILE = ' ' #'03082132.pvr'
DATE = 0
DATE2 = 0
TIME = 0
TIME1 = 0
PVR_DATA = 0
PVR_FILE = ' '
PVR_DATA1 = 0
BANNER = ' '
FRAME_NUMBER = 0
TIME_DELTA = 0
EXT = '.mp4'
EXT1 = '.jpg'
#VIDEO_TIME = '10:22:00.771'
#----VIDEO_TIME = '10:11:37.020'
#VIDEO_TIME = '10:19:38.639'  # 09/03/21
#VIDEO_TIME ='08:43:16.884'
#VIDEO_DATE = '09/03/21'
#---VIDEO_TIME = '08:59:44.325'
#VIDEO_DATE = '10/03/21'
#VIDEO_DATE = ' '
#VIDEO_FILE = 0
line = 2
pvr_time = 0
video_time = 0
pvr_date = 0
pvr_banner = ' '
ban = ' '
pvr_count = 0
start_line = 0
new_frame = 0
first_frame = 0
frame_num1 = 0
frame_num = 0
start_banner =  ' '
offset = 0
trim = 1.05
test_value = 'test'
line_num = 0
line_filler = '_'*40
RED = 255  # 0 - 255
BLUE = 255 # 0 - 255
GREEN = 255 # 0 - 255
x,y,w,h = 0,640,560,100
width = 1280
height = 720
pause = False
forward = False
back = False
count1 = 0
count = 0
record_directory = ''
record_bkmark = False
PVR_LINE = 0

#w = int(((w/width)*100)*width)
#h = int(((h/height)*100)*height)
#def start_audit():
#get files

class Auditor:
	def __init__(self, VIDEO_TIME,VIDEO_DATE, PVR_FILE):
		self.VIDEO_TIME = VIDEO_TIME
		self.VIDEO_DATE = VIDEO_DATE
		self.PVR_FILE = PVR_FILE

	#cap = cv2.VideoCapture('/dev/video0')
	#data synchronization
	def sync_data():
		try:
			video_start_time = converter(VIDEO_TIME)
		except NameError:
			#print('Missing VIDEO TIME make sure video file matches naming convention')
			var.set('Missing VIDEO TIME make sure video file matches naming convention')
			messagebox.showinfo("showeinfo", "Missing VIDEO_TIME")
			#time.sleep(1)
			messagebox.destroy()

		global count
		count = 0
		global pvr_time1
		global pvr_time
		pvr_time = 0
		#update
		pvr_file_count = 0
		try:
			while pvr_time != video_start_time:
				pvr = open(PVR_FILE)
        			#for line in enumerate(pvr):
				pvr_data = pvr.readlines()
				PVR_DATA = pvr_data[count]
				BANNER = PVR_DATA
				PVR_DATA = PVR_DATA.rstrip()
				PVR_DATA = PVR_DATA.split(',')
				DATE = PVR_DATA[0]
				TIME = PVR_DATA[1]
				print('pvr time: ',TIME)
				#convert time to seconds
				pvr_time = converter(TIME)
				#sync video with pvr
				if DATE and pvr_time is not None:

# 					stops progress at first pass
#					if VIDEO_DATE != DATE:
#						print('No match found for date selected retry')
#						time.sleep(2)
#						print('debug sync_data')
#						sys.exit()

					if VIDEO_DATE == DATE and pvr_time == video_start_time:
						print('Seconds: ', pvr_time)
						print('DATE: ', DATE)
						print('line_number: ', count)
						global offset
						global pvr_count
						global pvr_date
						offset = pvr_time - video_start_time - trim
						pvr_date = DATE
						pvr_time1 = pvr_time
						return pvr_time, DATE, offset, pvr_count
#					if VIDEO_DATE == DATE and pvr_time < video_start_time:
#						offset = video_start_time - pvr_time - trim
#						return pvr_time, DATE, offset, count

					if VIDEO_DATE == DATE and pvr_time > video_start_time:
						offset = pvr_time - video_start_time - trim
						pvr_time1 = pvr_time
						#print('Audit found ')
						#print('Date: {} Offset: {} - Pvr time: {} - video start time: {}'.format(DATE, offset, pvr_time, video_start_time))
						return pvr_time, DATE, offset, pvr_count, PVR_FILE

					else:
						print('Time not found')
						print('Offset: {} - Pvr time: {} - video start time: {}'.format(offset, pvr_time, video_start_time))
						count = count + 1
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

	#def file_length(PVR_FILE):
#       	with open(PVR_FILE) as f:
#               	for i, l in enumerate(f):
#                       pass
#               return i + 1
	#data analyzation
	#here need global values (count and PVR_FILE) from sync_data()

	def get_pvr_frame(line):
		frame_time = 0
		frame_time1 = 0
		#pvr_count = 56
		start_line = count
		next_frame = 0
		try:
			new_line = line+count
			pvr = open(PVR_FILE)
			pvr_data = pvr.readlines()
			#print('pvr new line number: ', new_line)
			PVR_DATA = pvr_data[new_line]
			#debug time drift
			if new_line > start_line:
				#print('start line:', start_line)
				PVR_DATA1 = pvr_data[new_line-1]
				#print('pvr data1: {} | pvr data: {}'.format(PVR_DATA1, PVR_DATA))
				#debug time drift
				PVR_DATA1 = PVR_DATA1.rstrip()
				PVR_DATA1 = PVR_DATA1.split(',')
				#DATE2 = PVR_DATA[0]
				TIME1 = PVR_DATA1[1]
				frame_time = converter(TIME1)

			else:
				frame_time1 = 0
				TIME1 = 0
		except IndexError:
			print('frames exceed lines')
		BANNER = PVR_DATA
		PVR_DATA = PVR_DATA.rstrip()
		PVR_DATA = PVR_DATA.split(',')
		DATE2 = PVR_DATA[0]
		TIME = PVR_DATA[1]
		#print('time: {} | time1: {}'.format(TIME,TIME1))
		#print('DATE: ', DATE2) #debug
		#print('VIDEO DATE: ', VIDEO_DATE)
		frame_time = converter(TIME)
		#print('offset: ', offset)
		#print('frame time: {} | frame time1: {}'.format(frame_time, frame_time1))
		fps = cap.get(cv2.CAP_PROP_FPS)
		fps = float(fps)
		#print('frame time1: ', frame_time1)
		TIME_DELTA = ((frame_time + (offset + .99)) - pvr_time) # offset adjustment
		TIME_DELTA1 = ((frame_time - frame_time1 + (offset + .99))) # offset adjustment
		#print('pvr_time: {} frame_time: {} | frame_time1: {} | offset: {}'.format(pvr_time, frame_time, frame_time1, offset))
		#print('Time delta: ', TIME_DELTA)
		#print('Time delta1: ', TIME_DELTA1)
		global frame_num
		frame_num = (fps*TIME_DELTA)
		frame_num = int(frame_num)
		next_frame = frame_num+next_frame
		w_1_entry2_12_1.delete(0, END)
		w_1_entry2_12_1.insert(END, next_frame)
		#print('frame_num: {} | next_frame: {}'.format(frame_num, next_frame))
		pvr.close()
		return frame_num, BANNER

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
		#cv2.putText(frame,'Class: {} | Axle: {} {}'.format(g,h,j),(10+i,95),font,font_size,(BLUE,GREEN,RED),1)

	def banner_label3(frame,font):
		font_size = 0.4
		i = 985
		cv2.putText(frame,'Date/Time: {}'.format(Auditor.get_video_name()),(10+i,10),font,font_size,(BLUE,GREEN,RED),1)

	def banner_info(line):
		frame_num, BANNER = Auditor.get_pvr_frame(line)
		BANNER = BANNER.strip()
#		var.set(BANNER)
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
		w_1_entry0_0_1.delete(0, END)
		w_1_entry0_0_1.insert(END, BANNER[0])
		w_1_entry5_5_1.delete(0, END)
		w_1_entry5_5_1.insert(END, BANNER[3])
		w_1_entry6_6_1.delete(0, END)
		w_1_entry6_6_1.insert(END, banner_speed)
		w_1_entry7_7_1.delete(0, END)
		w_1_entry7_7_1.insert(END, BANNER[5])
		w_1_entry8_8_1.delete(0, END)
		w_1_entry8_8_1.insert(END, BANNER[10])
		w_1_entry9_9_1.delete(0, END)
		w_1_entry9_9_1.insert(END, BANNER[11])
		w_1_entry10_10_1.delete(0, END)
		w_1_entry10_10_1.insert(END, BANNER[6])
		w_1_entry11_11_1.delete(0, END)
		w_1_entry11_11_1.insert(END, BANNER[12])
		return banner_date,banner_time,banner_lane,banner_dir,banner_length,banner_speed,banner_class,banner_axle,banner_note

	def play_video():
		#sync_data()
		record_bkmark == True
		i = 0
		line = count #pvr_count - pvr_count
		fps = cap.get(cv2.CAP_PROP_FPS)
		fps = int(fps)
		frame_number, PLAY_BANNER = Auditor.get_pvr_frame(line)
		#print('first line number is: ', line)
		cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
		fourcc = cv2.VideoWriter_fourcc(*'MP4V')

		while (cap.isOpened()):

			while pause == True:
				Auditor.tracker()

			frame_num, PLAY_BANNER = Auditor.get_pvr_frame(line)
			banner_date,banner_time,banner_lane,banner_dir,banner_length,banner_speed,banner_class,banner_axle,banner_note = Auditor.banner_info(line)
			#cap.set(cv2.CAP_PROP_POS_FRAMES, FRAME_NUMBER)

			ret, frame = cap.read()
			frame = cv2.resize(frame, (width, height))
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0,0,0), -1)
    			#gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			font = cv2.FONT_HERSHEY_SIMPLEX
			if frame_num - (fps*2) < frame_number:
				pvr_line_number = pvr_count + line

				#modified 7/4/21
				#global DISPLAY_BANNER1
				DISPLAY_BANNER1 = Auditor.banner_label2(banner_date,banner_time,banner_lane,banner_dir,banner_length,banner_speed,banner_class,banner_axle,banner_note,pvr_line_number,frame,font,i)
			if banner_lane == '1':
				i = 0 #180

			elif banner_lane == '2':
				i = 0

			next_line = int(line + 1)
			frame_num, PLAY_BANNER = Auditor.get_pvr_frame(next_line)


			if frame_num >= frame_number - (fps):
				DISPLAY_BANNER2 = Auditor.banner_label2(banner_date,banner_time,banner_lane,banner_dir,banner_length,banner_speed,banner_class,banner_axle,banner_note,pvr_line_number,frame,font,i)
				if banner_lane == '1':
					i = 0 #180

				if banner_lane == '2':
					i = 0

				if frame_number > frame_num + (fps):
					line = int(line + 1)

			#cv2.rectangle(frame, (x, x), (x + w, y + h), (0,0,0), -1)
			#cv2.putText(frame,BANNER, (x + int(w/10),y + int(h/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
			#----cv2.putText(frame,BANNER,(100,680),font,0.4,(BLUE,GREEN,RED),1) #BGR
			#cv2.rectangle(frame,(900,450),(500,200),(0,255,0),6)

			if frame_number > frame_num + (fps):
				line = int(line + 1)
			cv2.putText(frame,DISPLAY_BANNER1,(100,680),font,0.4,(BLUE,GREEN,RED),1) #BGR
			cv2.putText(frame,DISPLAY_BANNER2,(100,680),font,0.4,(BLUE,GREEN,RED),1) #BGR
			#cv2.putText(frame,'Lane_2 _____________',(10,20),font,0.4,(BLUE,GREEN,RED),1)
			#cv2.putText(frame,'Lane_1 _____________',(180,20),font,0.4,(BLUE,GREEN,RED),1)

			if record_bkmark == True:
				PVR_LINE = line
				if frame_number == frame_num:
					cv2.imwrite(record_directory+'bookmark_'+str(PVR_LINE)+EXT1, frame)
					#out.write(frame)


			cv2.imshow('frame', frame)

			#modified 7/4/21
			#global get_frame
			get_frame = frame
			#print('playback fps: ', fps)
			#print('pvr line: ',line)
			w_1_entry4_4_1.delete(0, END)
			w_1_entry4_4_1.insert(END, line)
			#print('playback pvr count: ', pvr_count)
			#print('playback get_pvr frame number: ', frame_num)
			#print('playback video frame number: ',frame_number)
			w_1_entry3_3_1.delete(0, END)
			w_1_entry3_3_1.insert(END, frame_number)
			frame_number = frame_number + 1
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

			if stop == True:
				break
				cap.release()
				cv2.destroyAllWindows()

		cap.release()
		cv2.destroyAllWindows()

	def record_live_video():
		record_directory = filedialog.askdirectory()
		record_directory = '{}/'.format(record_directory)
		#record_directory = '/media/bob/ssd128/'
		#record_directory = '/media/bob/ssd128/avc_test_videos/'
		#video_file = 'rtsp://calendar:TTItest1@10.4.1.185:554/axis-media/media.amp?video=1&audio=1&videocodec=jpeg&event=on&fps=0'
		#video_file = askopenfilename(filetypes=[("Files", "*.mp4"), ("All Files", "*.*")])
		#video_file = camera
		global cap
		cap = cv2.VideoCapture(video_file)
		x,y,w,h = 990,0,290,15
		#cap = cv2.VideoCapture(0) # Capture images from main camera
		# Define the codec and create VideoWriter object
		#fourcc = cv2.VideoWriter_fourcc(*'MPEG')
		fourcc = cv2.VideoWriter_fourcc(*'MP4V')
		#fourcc = cv2.VideoWriter_fourcc(*'XVID') #(*'MP4V') #(XVID*'')     #####debug video format
		#fourcc = cv2.VideoWriter_fourcc(*'XVID')
		#Add Text
		#------------------------------------------------------------------------
		#out = cv2.VideoWriter('output.mp4',fourcc, 20.0, (640,480))
		out = cv2.VideoWriter(record_directory+Auditor.get_video_name()+EXT,fourcc, 20.0, (1280,720))
		while(cap.isOpened()):

			#debug set resolution
			ret, frame = cap.read()
			#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
			#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
			#cap.set(cv2.CAP_PROP_FPS, 30)
			frame = cv2.resize(frame, (width,height))
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0,0,0), -1)
			if ret==True:
        			#frame = cv2.flip(frame,0)
				font = cv2.FONT_HERSHEY_SIMPLEX
				#cv2.putText(frame,'OpenCV',(10,500), font, 4,(255,255,255),2,cv2.LINE_AA)
				#----cv2.putText(frame,get_video_name(),(100,50),font,1,(0,0,255),4)
				Auditor.banner_label3(frame,font)
				#cv2.rectangle(frame,(900,450),(500,200),(0,255,0),6)
        			# write the flipped frame
				out.write(frame)

				cv2.imshow('frame',frame,)
				if cv2.waitKey(1) & 0xFF == ord('q'):
					break

				if stop == True:
					break
					cap.release()
					cv2.destroyAllWindows()
			else:
				break

		# Release everything if job is finished
		cap.release()
		out.release()
		cv2.destroyAllWindows()


	def tracker():
		frame = 0
		output = 0
		#cap.set(cv2.CAP_PROP_POS_FRAMES, new_frame)
		#ret, frame = cap.read()
		def nothing(FRAME_NUMBER):
			i = 0
			#play_video1(start_frame_number)
			#print('YOU ARE HERE', count)
			#pass
			#while(cap.isOpened()):
			new_frame, BANNER = Auditor.get_pvr_frame(FRAME_NUMBER)
			BANNER = BANNER.strip()
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

			new_frame = float(new_frame)
			cap.set(cv2.CAP_PROP_POS_FRAMES, new_frame)
			fourcc = cv2.VideoWriter_fourcc(*'MP4V')
			ret, frame = cap.read()
			frame = cv2.resize(frame, (width,height))
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0,0,0), -1)
			if banner_lane == '1':
				i = 0 #180

			if banner_lane == '2':
				i = 0
			pvr_line_number = FRAME_NUMBER + count
			font = cv2.FONT_HERSHEY_SIMPLEX
			BANNER = Auditor.banner_label2(banner_date,banner_time,banner_lane,banner_dir,banner_length,banner_speed,banner_class,banner_axle,banner_note,pvr_line_number,frame,font,i)


			#gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			#font = cv2.FONT_HERSHEY_SIMPLEX
			cv2.putText(frame,BANNER,(100,680),font,0.5,(255,0,0),2) #BGR
			#cv2.rectangle(frame,(900,450),(500,200),(0,255,0),6)
			#cv2.imshow('frame',gray)
			#cv2.putText(frame,'Lane_2 _____________',(10,20),font,0.4,(BLUE,GREEN,RED),1)
			#cv2.putText(frame,'Lane_1 _____________',(180,20),font,0.4,(BLUE,GREEN,RED),1)

			PVR_LINE = pvr_line_number
			#cv2.imwrite(record_directory+'bookmark_'+str(PVR_LINE)+EXT1, frame)

			cv2.imshow('frame', frame)
			#print('new_frame_numer: ', new_frame)
			#print('frame_per_sec: ', fps)

		#back = 0
		# Create a black image, a window
		#cv2.namedWindow("Frame")
		#cv2.createButton("Back",back,none,cv2.QT_PUSH_BUTTON,start_frame_number)
		gui = np.zeros((150,512,1), np.uint8)
		#img = np.zeros((300,512,3), np.uint8)
		cv2.namedWindow('avc_audit')

		# create trackbars for color change
		cv2.createTrackbar('Tracking','avc_audit',count1,totalframecount,nothing)

		#cv2.createTrackbar('Tracking','avc_audit',0,totalframecount,nothing)
		#cv2.createTrackbar('Tracking','avc_audit',0,file_length(PVR_FILE),nothing)
		#cv2.createTrackbar('R','image',0,255,nothing)
		#cv2.createTrackbar('G','image',0,255,nothing)
		#cv2.createTrackbar('B','image',0,255,nothing)

		# create switch for ON/OFF functionality
		#switch = '0 : OFF \n1 : ON'
		#cv2.createTrackbar(switch, 'image',0,1,nothing)
		while(1):
			cv2.imshow('avc_audit', gui)
			k = cv2.waitKey(1) & 0xFF
			if k == 27:
				break

			if stop == True:
				break
				cap.release()
				cv2.destroyAllWindows()

			# get current positions of four trackbars
			FRAME_NUMBER1 = cv2.getTrackbarPos('Tracking','avc_audit')

		cv2.destroyAllWindows()


	def skip_video():
		#host = 'rtsp://calendar:AVCaudit1@10.4.0.187:554/axis-media/media.amp?videocodec=h264'
		host = "10.4.0.175:8080"
		#hoststr = 'rtsp://calendar:AVCaudit1@'+host+'/axix-media/media.amp?videocodec=h264'
		hoststr = 'http://' + host +  '/stream.mjpeg'
		print ('Streaming ' + hoststr)
		stream=urllib.urlopen(hoststr)
		bytes=''
		drop_count = 0
		while True:
			bytes+=stream.read(1024)
    			#bytes+=stream.read(1024)
			a = bytes.find('\xff\xd8')
			b = bytes.find('\xff\xd9')
			if a!=-1 and b!=-1:
				drop_count+=1
				if drop_count > 120:
					drop_count = 0
					jpg = bytes[a:b+2]
					bytes= bytes[b+2:]
					i=cv2.imdecode(np.fromstring(jpg,dtype=np.uint8),cv2.IMREAD_COLOR)
					cv2.imshow(hoststr,i)
					process_img(i)#my image processing
					if cv2.waitKey(1) ==27:
						exit(0)
	#not working
	def find_metadata():
		#atom = file.find('.//%s//data' % name)
		#return atom.get_attribute('data')
		data = os.system('sudo ffprobe -hide_banner -v quiet -show_streams -print_format flat {}'.format(video_metadata))
		#data = os.system('sudo ffprobe -v quiet -show_streams -print_format flat {}'.format(video_metadata))
		#data = os.system('sudo ffprobe -show_frames -print_format flat {}'.format(video_metadata))
		#data = os.system('sudo ffprobe -show_private_data -print_format flat {}'.format(video_metadata))
		#data = os.system('sudo ffprobe -timecode 00:02:05 -print_format flat {}'.format(video_metadata))
		return data




#def start_audit():
#get files
def pvr_file():
	"""Open a file for editing."""
	global PVR_FILE
	PVR_FILE = askopenfilename(filetypes=[("Files", "*.pvr"), ("All Files", "*.*")])
	w_1_entry12_2_1.delete(0, END)
	w_1_entry12_2_1.insert(END, PVR_FILE)
	print('Pvr file: ', PVR_FILE)

#converter
def converter(converter):
	t = converter
	h,m,s = t.split(':')
	#convert time to seconds
	convert = float(datetime.timedelta(hours=float(h),minutes=float(m),seconds=float(s)).total_seconds())
	return convert

#get video files
def pvr_video():
	"""Open a file for editing."""
	global video_file
	video_file = askopenfilename(filetypes=[("Files", "*.mp4"), ("All Files", "*.*")])
	print('AVC AUDITOR')
	w_1_entry1_1_1.delete(0, END)
	w_1_entry1_1_1.insert(END, video_file)
	print()
	global VIDEO_TIME
	VIDEO_TIME = video_file
	#print('Video file name: ', VIDEO_FILE)
	date1, time1 = VIDEO_TIME.split('_')
	time1 = time1.strip('mp4')
	VIDEO_TIME = time1.rstrip('.')
	print('Video time: ', VIDEO_TIME)
	#pvr_year, pvr_month, pvr_day = date1.split('-')
	#global VIDEO_DATE
	#VIDEO_DATE  = '{}/{}/{}'.format(pvr_day, pvr_month, pvr_year)
	#print('Video search date: ', VIDEO_DATE)

	#video_file = 'rtsp://calendar:AVCaudit1@10.4.0.175:554/axis-media/media.amp?videocodec=h264'
	#video_file = '/ssd500/pvr_video_2021-03-09-10_19_38_639.mp4'
	#video_file = VIDEO_FILE #'/media/B64E859D4E8556D1/AVC_AUDIT_TEST/Export_2021-03-23_15_03_57_473/axis_2021-03-10_08_59_44_325.mp4'
	#video_file = '/media/B64E859D4E8556D1/march_5_2021.mp4'
	global cap
	cap = cv2.VideoCapture(video_file)
	print('video file is: ', video_file)

	#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
	#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
	#cap.set(cv2.CAP_PROP_FPS, 30)
	#---cap = cv2.VideoCapture('/dev/video0')
	#video_metadata = '/media/B64E859D4E8556D1/march_5_2021.mp4'
	global video_metadata
	video_metadata = video_file  #'/media/robert/ssd128/2021_04_10_08:19:38.075552.mp4' #video_file
	#cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame_number) # skip frames
	global fps
	fps = cap.get(cv2.CAP_PROP_FPS) # get frames per second
	global totalframecount
	totalframecount= int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) # get number of frames
	print('frame_per_sec: ', fps)
	print('total_num_frames: ', totalframecount)

os.system('clear')
def open_file():
	"""Open a file for editing."""
	filepath = askopenfilename(filetypes=[("Files", "*.mp4"), ("All Files", "*.*")])
	audit.file_select(filepath)
       	#if not filepath:
		#return
		#txt_edit.delete(1.0, tk.END)
        	#with open(filepath, "r") as input_file:
        	#text = input_file.read()
		#print('Selected file: ', text)
	print('Selected file: ', filepath)
	audit.file_select(filepath)
	#return filepath
	#txt_edit.insert(tk.END, text)
	#window.title(f"Simple Text Editor - {filepath}")

def play():
	global play
	global back
	global pause
	global stop
	global record
	global forward
	global video_file
	global button_state
	forward = False
	record = False
	stop = False
	pause = False
	back = False
	play = True
	button_state = False
	#Button(window, text="Play", state=DISABLED)
	def run1():
		Button(window, text="Play", state=DISABLED)
		Auditor.sync_data()
		Auditor.play_video()
	thread = threading.Thread(target=run1)
	thread.start()
	print(play)

def pause():
	global pause
	pause = not pause
	print('Pause again: ', pause)

def skip():
	global skip
	#global stop
	#stop = True
	#time.sleep(2)
	print('processing ....')
	skip = True
	def run():
		Auditor.sync_data()
		Auditor.tracker()
	thread1 = threading.Thread(target=run)
	thread1.start()
	print(skip)

def back():
	global back
	global count1
	back = True
	count1 = count1 - 1
	#back = not back
	print('Back: ', count1)

def forward():
	global forward
	global count1
	forward = True
	count1 = count1 + 1
	#forward = not forward
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
	#audit.record_live_video()


def add_bkdir():
	global record_directory
	record_directory = filedialog.askdirectory()
	record_directory = '{}/'.format(record_directory)


def record_bookmark():
	global record_bkmark
	record_bkmark = not record_bkmark
	print(record_bkmark)


def add_camera():
	global camera
	camera = w_1_entry1_1_1.get()
	print('Camera: ',camera)
	w_1_entry1_1_1.delete(0, END)

def stop():
	global stop
	global pause
	global back
	global play
	global forward
	global record
	record = False
	forward = False
	play = False
	back = False
	pause = False
	stop = True
	#entry1.delete(0, END)
	w_1_entry2_12_1.delete(0, END)
	w_1_entry3_3_1.delete(0, END)
	w_1_entry4_4_1.delete(0, END)
	w_1_entry5_5_1.delete(0, END)
	w_1_entry6_6_1.delete(0, END)
	w_1_entry7_7_1.delete(0, END)
	w_1_entry8_8_1.delete(0, END)
	w_1_entry9_9_1.delete(0, END)
	w_1_entry10_10_1.delete(0, END)
	w_1_entry11_11_1.delete(0, END)
	print(stop)

def exit():
	global stop
	global pause
	global back
	global play
	global forward
	global record
	record = False
	forward = False
	play = False
	back = False
	pause = False
	stop = True
	w_1_entry1_1_1.delete(0, END)
	w_1_entry2_12_1.delete(0, END)
	w_1_entry3_3_1.delete(0, END)
	print(stop)
	window.destroy()

def set_date():
	# Create Object
	calendar = Tk()

	# Set geometry
	calendar.geometry("400x400")
	calendar.title('Audit date')

	# Add Calender
	cal = Calendar(calendar, selectmode = 'day', year = 2021, month = 5, day = 22)
	cal.pack(pady = 20)
	#date.config(text = "Selected Date is: " + cal.get_date())
	def grad_date():
		date.config(text = 'Selected date is: ' + cal.get_date())
		#print('Date: ',cal.get_date())
		video_date = cal.get_date()
		month, day, year = video_date.split('/')
		global VIDEO_DATE
		VIDEO_DATE  = '{}/{}/{}'.format(day.zfill(2), month.zfill(2), year)
		w_1_entry0_0_1.delete(0, END)
		w_1_entry0_0_1.insert(END, VIDEO_DATE)
		print('Date: ', VIDEO_DATE)
		calendar.destroy()

	# Add Button and Label
	calendar_btn_sel = Button(calendar, text = "Set Date", command = grad_date)
	calendar_btn_sel.pack(pady = 20)

	date = Label(calendar, text = "")
	date.pack(pady = 20)

	# Excecute Tkinter
	calendar.mainloop()


window = Tk()
window.title("AVC Audit")
window.rowconfigure(0, minsize=800, weight=1)
window.columnconfigure(0, minsize=800, weight=1)
w_1_my_img1 = ImageTk.PhotoImage(Image.open('/DATA/camera_1/2020_12_06/test.png'))
#my_img1 = ImageTk.PhotoImage(Image.open(get_frame))
#labels
#my_label Label(image=my_img1[frame_number])
var = StringVar()
w_1_my_label0_0_1 = Label(window, textvariable=var, relief=RAISED )
#my_label = Label(window, text='Images')
w_1_my_label1_0_1 = Label(window, textvariable=var)
w_1_my_label2_3_1 = Label(window, text="PVR Line Number")
#my_label.grid_forget()

#Debug
#labelText=StringVar()
#labelText.set("Enter directory of log files")
#labelDir=Label(window, textvariable=labelText, height=4)
#labelDir.grid(row=0,column=0)

#var = StringVar()
#label = Label( calendar, textvariable=var, relief=RAISED )
#var.set('Image')
#var.set("Hey!? How are you doing?")
#label.pack()
#calendar.mainloop()
#txt_edit = tk.Text(window)

#entry box
window = Frame(window, relief=RAISED, bd=2)
w_1_entry0_0_1 = Entry(window, width=10)  #Date
w_1_entry1_1_1 = Entry(window, width=100) #camera path
w_1_entry2_12_1 = Entry(window, width=10) #next frame
w_1_entry3_3_1 = Entry(window, width=10) #current frame
w_1_entry4_4_1 = Entry(window, width=10) #pvr line number
w_1_entry5_5_1 = Entry(window, width=10) #lane number
w_1_entry6_6_1 = Entry(window, width=10) #speed
w_1_entry7_7_1 = Entry(window, width=10) #direction
w_1_entry8_8_1 = Entry(window, width=10) #
w_1_entry9_9_1 = Entry(window, width=10)
w_1_entry10_10_1 = Entry(window, width=10)
w_1_entry11_11_1 = Entry(window, width=10)
w_1_entry12_2_1 = Entry(window, width=100) #PVR_FILE


#buttons
w_1_btn_open_0_0 = Button(window, text="Import video", command=pvr_video)
w_1_btn_play_1_0 = Button(window, text="Play", command=play)
w_1_btn_pause_2_0 = Button(window, text="Pause", command=pause)
w_1_btn_tracker_5_0 = Button(window, text="Tracker", command=skip)
w_1_btn_back_3_0 = Button(window, text="<<", command=back)
w_1_btn_forward_4_0 = Button(window, text=">>", command=forward)
w_1_btn_bkdir_11_0 = Button(window, text="Add Bookmark Dir", command=add_bkdir)
w_1_btn_bookmark_12_0 = Button(window, text="Record", command=record)
w_1_btn_record_13_0 = Button(window, text="Record Bookmark", command=record_bookmark)
w_1_btn_stop_7_0 = Button(window, text="Stop", command=stop)
#btn_set_date = tk.Button(fr_buttons, text = "Set Date", command = set_date)
w_1_btn_set_date_8_0 = Button(window, text = "Select Date", command = set_date) #.pack(pady = 20)
w_1_btn_pvrfile_9_0 = Button(window, text="Import PVR file", command=pvr_file)
w_1_btn_add_camera_10_0 = Button(window, text="Add Camera", command=add_camera)
w_1_btn_exit_14_0 = Button(window, text="Exit", command=exit)
#text_box = tk.Text()
#entry = tk.Entry()

#buttons
#btn_play.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
w_1_btn_open_0_0.grid(row=0, column=0, sticky="ew", padx=5)
w_1_btn_play_1_0.grid(row=1, column=0, sticky="ew", padx=5)
w_1_btn_pause_2_0.grid(row=2, column=0, sticky="ew", padx=5)
w_1_btn_back_3_0.grid(row=3, column=0, sticky="ew", padx=5)
w_1_btn_forward_4_0.grid(row=4, column=0, sticky="ew", padx=5)
w_1_btn_tracker_5_0.grid(row=5, column=0, sticky="ew", padx=5)
w_1_btn_bookmark_12_0.grid(row=6, column=0, sticky="ew", padx=5)
w_1_btn_stop_7_0.grid(row=7, column=0, sticky="ew", padx=5)
w_1_btn_set_date_8_0.grid(row=8, column=0, sticky="ew", padx=5)
w_1_btn_pvrfile_9_0.grid(row=9, column=0, sticky="ew", padx=5)
w_1_btn_add_camera_10_0.grid(row=10, column=0, sticky="ew", padx=5)
w_1_btn_bkdir_11_0.grid(row=11, column=0, sticky="ew", padx=5)
w_1_btn_bookmark_12_0.grid(row=12, column=0, sticky='ew', padx=5)
w_1_btn_record_13_0.grid(row=13, column=0, sticky='ew', padx=5)
w_1_btn_exit_14_0.grid(row=14, column=0, sticky="ew", padx=5)

#entry box
w_1_entry0_0_1.grid(row=0, column=1, sticky="nw", padx=5)
w_1_entry1_1_1.grid(row=1, column=1, sticky="nw", padx=5)
w_1_entry2_12_1.grid(row=12, column=1, sticky="nw", padx=5)
w_1_entry3_3_1.grid(row=3, column=1, sticky="nw", padx=5)
w_1_entry4_4_1.grid(row=4, column=1, sticky="nw", padx=5)
w_1_entry5_5_1.grid(row=5, column=1, sticky="nw", padx=5)
w_1_entry6_6_1.grid(row=6, column=1, sticky="nw", padx=5)
w_1_entry7_7_1.grid(row=7, column=1, sticky="nw", padx=5)
w_1_entry8_8_1.grid(row=8, column=1, sticky="nw", padx=5)
w_1_entry9_9_1.grid(row=9, column=1, sticky="nw", padx=5)
w_1_entry10_10_1.grid(row=10, column=1, sticky="nw", padx=5)
w_1_entry11_11_1.grid(row=11, column=1, sticky="nw", padx=5)
w_1_entry12_2_1.grid(row=2, column=1, sticky="nw", padx=5)
#labels
w_1_my_label0_0_1.grid(row=0, column=1, sticky="ne")
w_1_my_label1_0_1.forget()
w_1_my_label1_0_1.grid(row=0, column=1, sticky="wn", padx=5)
w_1_my_label2_3_1.grid(row=3, column=1, sticky="wn", padx=5)
#text_box.grid(row=2, column=5, sticky="ew", padx=5, pady=5)
#entry.grid(row=2, column=5, sticky="ew", padx=5, pady=5)
#label.pack()
#entry.pack()

#btn_forward.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
#btn_skip.grid(row=4, column=0, sticky="ew", padx=5, pady=5)
#btn_record.grid(row=5, column=0, sticky="ew", padx=5, pady=5)
#btn_save.grid(row=1, column=0, sticky="ew", padx=5)

window.grid(row=0, column=0, sticky="nw")
#txt_edit.grid(row=5, column=1, sticky="nsew")
#create window
window.mainloop()

#if __name__ == "__Auditor__":
	# execute only if run as a script
#	main()


