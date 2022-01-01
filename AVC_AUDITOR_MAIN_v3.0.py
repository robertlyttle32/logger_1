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
start_banner =  ''
offset = 0
trim = 1.05
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
count1 = 0
count = 0
record_directory = ''
record_bkmark = False
PVR_LINE = 0
OFFSET = 0
TRACKER_FRAME = ''
#line = 0
tracker_line = 0
button_status = ''
frame = ''

#get files
class Auditor:
	def __init__(self, VIDEO_TIME,VIDEO_DATE, PVR_FILE):
		self.VIDEO_TIME = VIDEO_TIME
		self.VIDEO_DATE = VIDEO_DATE
		self.PVR_FILE = PVR_FILE

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
		global pvr_time1
		global pvr_time
		global offset
		global pvr_count
		global pvr_date
		global DATE
		pvr_time = 0
		count = 0
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
					if VIDEO_DATE == DATE and pvr_time == video_start_time:
						print('Seconds: ', pvr_time)
						print('DATE: ', DATE)
						print('line_number: ', count)
						offset = pvr_time - video_start_time - trim
						pvr_date = DATE
						pvr_time1 = pvr_time
						return count
  
					if VIDEO_DATE == DATE and pvr_time > video_start_time:
						offset = pvr_time - video_start_time - trim
						pvr_time1 = pvr_time
						return count
					
					else:
						#print('Time not found')
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

	def get_pvr_frame(line):
		frame_time = 0
		#pvr_count = 56
		start_line = count
		next_frame = 0
		try:
			fps = cap.get(cv2.CAP_PROP_FPS)
			fps = float(fps)
			line = line+count
			pvr = open(PVR_FILE)
			pvr_data = pvr.readlines()
			PVR_DATA = pvr_data[line]
			if line > start_line:
				PVR_DATA1 = pvr_data[line-1]
				PVR_DATA1 = PVR_DATA1.rstrip()
				PVR_DATA1 = PVR_DATA1.split(',')
				TIME = PVR_DATA1[1]
				frame_time = converter(TIME)
			else:
				TIME = 0
			BANNER = PVR_DATA
			PVR_DATA = PVR_DATA.rstrip()
			PVR_DATA = PVR_DATA.split(',')
			DATE2 = PVR_DATA[0]
			TIME = PVR_DATA[1]
			frame_time = converter(TIME)
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

	def play_video(tracker_line,frame_number,i,pvr_line_number):
		global frame_num
		global frame
		record_bkmark == True
		i = 0
		fps = cap.get(cv2.CAP_PROP_FPS)
		fps = int(fps)
		cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
		fourcc = cv2.VideoWriter_fourcc(*'MP4V')
		#while (cap.isOpened()):
		banner_date,banner_time,banner_lane,banner_dir,banner_length,banner_speed,banner_class,banner_axle,banner_note = Auditor.banner_info(tracker_line)
		ret, frame = cap.read()
		frame = cv2.resize(frame, (width, height))
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0,0,0), -1)
		#cv2.rectangle(frame,(900,450),(500,200),(0,255,0),6)
		font = cv2.FONT_HERSHEY_SIMPLEX
		DISPLAY_BANNER1 = Auditor.banner_label2(banner_date,banner_time,banner_lane,banner_dir,banner_length,banner_speed,banner_class,banner_axle,banner_note,pvr_line_number,frame,font,i)
		DISPLAY_BANNER2 = Auditor.banner_label2(banner_date,banner_time,banner_lane,banner_dir,banner_length,banner_speed,banner_class,banner_axle,banner_note,pvr_line_number,frame,font,i)
		cv2.putText(frame,DISPLAY_BANNER1,(100,int(680*.89)),font,0.4,(BLUE,GREEN,RED),1) #BGR
		cv2.putText(frame,DISPLAY_BANNER2,(100,int(680*.89)),font,0.4,(BLUE,GREEN,RED),1) #BGR
		if record_bkmark == True:
			PVR_LINE = tracker_line
			if frame_number == frame_num:
				cv2.imwrite(record_directory+'bookmark_'+str(PVR_LINE)+EXT1, frame)
		cv2.imshow('frame', frame)

		#global get_frame
		get_frame = frame
		w_1_entry4_15_2.delete(0, END)
		w_1_entry4_15_2.insert(END, tracker_line+count)
		w_1_entry3_14_2.delete(0, END)
		w_1_entry3_14_2.insert(END, frame_number)
		if cv2.waitKey(30) & 0xFF == ord('q'):
			pass
		if stop == True:
			cap.release()
			cv2.destroyAllWindows()
		if play == False:
			cap.release()
			cv2.destroyAllWindows()

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
				Auditor.banner_label3(frame,font)
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

	def tracker(line):
		pass

#get files
def pvr_file():
	"""Open a file for editing."""
	global PVR_FILE
	PVR_FILE = askopenfilename(filetypes=[("Files", "*.pvr"), ("All Files", "*.*")])
	w_1_entry12_12_2.delete(0, END)
	w_1_entry12_12_2.insert(END, PVR_FILE)
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
def play():
	global play
	global cap
	global back
	global pause
	global stop
	global record
	global forward
	global button_state
	#global tracker_line
	global frame_number
	forward = False
	record = False
	stop = False
	pause = False
	back = False
	play = True
	button_state = False
	#play = not play
	cap = cv2.VideoCapture(video_file)
	fps = cap.get(cv2.CAP_PROP_FPS)
	print(play)
	def run1():
		frame_num = 0
		file_read_dir = 1 # switches the pvr count to + or -
		player_control = 0
		player_speed = 0
		i = 0
		pvr_line_number = 0
		count = Auditor.sync_data()
		start_frame_number = Auditor.get_pvr_frame(count)[0]
		frame_number = start_frame_number
		next_frame_number = Auditor.get_pvr_frame(count+1)[0]
		banner_lane = Auditor.banner_info(count)[2]
		while True:

			test_test = 1
			if test_test == 1: #start_frame_number < frame_number < totalframecount:
				#tracker_line = int((count1/totalframecount)*100)

				next_frame_number = Auditor.get_pvr_frame(count+1)[0]
				banner_lane = Auditor.banner_info(count)[2]
				pvr_line_number = count
				if next_frame_number - (fps) < frame_number and back == False: # forward
					#global DISPLAY_BANNER1
					if banner_lane == '1':
						i = 0 #180
					if banner_lane == '2':
						i = 0
					next_frame_number = Auditor.get_pvr_frame(count+1)[0]
				if frame_number < next_frame_number-(fps) and back == True: # back
						#global DISPLAY_BANNER1
					if banner_lane == '1':
						i = 0 #180
					if banner_lane == '2':
						i = 0
					next_frame_number = Auditor.get_pvr_frame(count-1)[0]
      
				if next_frame_number >= frame_number - (fps):
					if banner_lane == '1':
						i = 0 #180
					if banner_lane == '2':
						i = 0
				if frame_number > next_frame_number + (fps) and back == False: # forward
					if forward == True:
						count = int(count + 1)
					if back == True:
						count = int(count - 1)
					else:
						count = int(count + 1)
      
				if frame_number < next_frame_number + (fps) and back == True: # back
					if forward == True:
						count = int(count + 1)
					if back == True:
						count = int(count - 1)
					else:
						count = int(count + 1)
     

			Auditor.play_video(count,frame_number,i,pvr_line_number)
			if forward == True:
				player_speed=fps
				frame_number = frame_number+player_speed
			if back == True:
				player_speed=fps
				frame_number = frame_number-player_speed
			if pause == True:
				player_speed=0
				frame_number = frame_number+player_speed
			if pause != True:
				player_speed=5
				frame_number = frame_number+player_speed
			print(f'Button pause: {pause} | Button back: {back} | Button forward: {forward}')
       				    
			if stop == True:
				break
    
	thread = threading.Thread(target=run1)
	thread.start()
	print(play)
    
def pause():
	global pause
	global back
	global forward
	forward = False
	back = False
	pause = not pause
	print('Pause again: ', pause)

def skip():
	global skip
	global cap
	global play
	global cap
	global back
	global pause
	global stop
	global record
	global forward
	global button_state
	forward = False
	record = False
	stop = False
	pause = False
	back = False
	play = False
	print('processing ....')
	skip = True
	cap = cv2.VideoCapture(video_file)
	def run():
		Auditor.sync_data()
		Auditor.tracker(tracker_line)
	thread1 = threading.Thread(target=run)
	thread1.start()
	print(skip)

def back():
	global back
	global pause
	global count1
	global forward
	forward = False
	pause = False
	back = not back
	count1 = count1-12
	print('Back: ', count1)

def forward():
	global forward
	global count1
	global pause
	global back
	back = False
	pause = False
	forward = not forward
	count1 = count1+12
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

def record_bookmark():
	global record_bkmark
	record_bkmark = not record_bkmark
	print(record_bkmark)

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
	play = False
	back = False
	pause = False
	stop = True
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
	w_1_entry1_11_2.delete(0, END)
	w_1_entry2_13_2.delete(0, END)
	w_1_entry3_14_2.delete(0, END)
	print(stop)
	window.destroy()

def set_date():
	# Create Object
	calendar = Tk()
	# Set geometry
	calendar.geometry("800x100")
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
w_1_my_img = ImageTk.PhotoImage(Image.open(r'/media/bob/USB20FD/neology_logo.PNG'))
w_1_my_logo = Label(image = w_1_my_img)

#w_1_my_frame = ImageTk.PhotoImage(Image.open('test_image.png'))
#w_1_my_frame_logo = Label(image = w_1_my_frame)

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

#entry box
#window = Frame(window, relief=RAISED, bd=2)
w_1_entry0_10_2 = Entry(window, width=10)  #Date
w_1_entry1_11_2 = Entry(window, width=100) #camera path
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
w_1_entry12_12_2 = Entry(window, width=100) #PVR_FILE

#buttons
w_1_btn_open_23_0 = Button(window, text="Import video", command=pvr_video)
w_1_btn_play_24_0 = Button(window, text="Play", command=play)
w_1_btn_pause_25_0 = Button(window, text="Pause", command=pause)
w_1_btn_tracker_28_0 = Button(window, text="Tracker", command=skip)
w_1_btn_back_26_0 = Button(window, text="<<", command=back)
w_1_btn_forward_27_0 = Button(window, text=">>", command=forward)
w_1_btn_bkdir_34_0 = Button(window, text="Add Bookmark Dir", command=add_bkdir)
w_1_btn_bookmark_35_0 = Button(window, text="Record", command=record)
w_1_btn_record_36_0 = Button(window, text="Record Bookmark", command=record_bookmark)
w_1_btn_stop_30_0 = Button(window, text="Stop", command=stop)
w_1_btn_set_date_31_0 = Button(window, text = "Select Date", command = set_date) #.pack(pady = 20)
w_1_btn_pvrfile_32_0 = Button(window, text="Import PVR file", command=pvr_file)
w_1_btn_add_camera_33_0 = Button(window, text="Add Camera", command=add_camera)
w_1_btn_exit_37_0 = Button(window, text="Exit", command=exit)

#buttons
#btn_play.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
w_1_btn_open_23_0.grid(row=23, column=0, sticky="wse", padx=5)
w_1_btn_play_24_0.grid(row=24, column=0, sticky="wse", padx=5)
w_1_btn_pause_25_0.grid(row=25, column=0, sticky="wse", padx=5)
w_1_btn_back_26_0.grid(row=26, column=0, sticky="wse", padx=5)
w_1_btn_forward_27_0.grid(row=27, column=0, sticky="wse", padx=5)
w_1_btn_tracker_28_0.grid(row=28, column=0, sticky="wse", padx=5)
w_1_btn_bookmark_35_0.grid(row=29, column=0, sticky="wse", padx=5)
w_1_btn_stop_30_0.grid(row=30, column=0, sticky="wse", padx=5)
w_1_btn_set_date_31_0.grid(row=31, column=0, sticky="wse", padx=5)
w_1_btn_pvrfile_32_0.grid(row=32, column=0, sticky="wse", padx=5)
w_1_btn_add_camera_33_0.grid(row=33, column=0, sticky="wse", padx=5)
w_1_btn_bkdir_34_0.grid(row=34, column=0, sticky="wse", padx=5)
w_1_btn_bookmark_35_0.grid(row=35, column=0, sticky='wse', padx=5)
w_1_btn_record_36_0.grid(row=36, column=0, sticky='wse', padx=5)
w_1_btn_exit_37_0.grid(row=37, column=0, sticky="wse", padx=5)

#entry box
w_1_entry0_10_2.grid(row=10, column=2, sticky="wn", padx=5)  #Date
w_1_entry1_11_2.grid(row=11, column=2, sticky="wn", padx=5)  #Camera Path
w_1_entry12_12_2.grid(row=12, column=2, sticky="wn", padx=5) #PVR File
w_1_entry2_13_2.grid(row=13, column=2, sticky="wn", padx=5)  #Next Frame
w_1_entry3_14_2.grid(row=14, column=2, sticky="wn", padx=5)  #Current Frame
w_1_entry4_15_2.grid(row=15, column=2, sticky="wn", padx=5)  #PVR Line Number
w_1_entry5_16_2.grid(row=16, column=2, sticky="wn", padx=5)  #lane Number
w_1_entry6_17_2.grid(row=17, column=2, sticky="wn", padx=5)  #Speed
w_1_entry7_18_2.grid(row=18, column=2, sticky="wn", padx=5)  #Direction
w_1_entry8_19_2.grid(row=19, column=2, sticky="wn", padx=5)  #
w_1_entry9_20_2.grid(row=20, column=2, sticky="wn", padx=5)
w_1_entry10_21_2.grid(row=21, column=2, sticky="wn", padx=5)
w_1_entry11_22_2.grid(row=22, column=2, sticky="wn", padx=5)

#labels
w_1_my_label_header_1_0.grid(row=1, column=0, sticky='wn', padx=5)  #Header
w_1_my_label2_10_0.grid(row=10, column=0, sticky='wn', padx=5)      #Date
w_1_my_label3_11_0.grid(row=11, column=0, sticky='wn', padx=5)      #PVR Video
w_1_my_label4_12_0.grid(row=12, column=0, sticky='wn', padx=5)      #PVR File
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
w_1_my_logo.grid(row=0, column=0, sticky='w')                       #Logo
#w_1_my_frame_logo.grid(row=24, column=4, sticky='w')


#create window
window.mainloop()


