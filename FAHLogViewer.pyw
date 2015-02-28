#!/usr/bin/python
# -*- coding: utf-8 -*-

from Tkinter import *
from ttk import *
import datetime, time, threading, sys, ttk, re, os, getpass, tkFont, shutil, winshell
from win32com.client import Dispatch
global nvidia_progress_bar, log_field, lastupdated, root, last_updated, v, z, amd_perc
from datetime import datetime
from dateutil import tz
from time import mktime

#    ___           _   _     _           _   _                 _     _                 
#   |_ _|  _ __   (_) | |_  (_)   __ _  | | (_)  ____   __ _  | |_  (_)   ___    _ __  
#    | |  | '_ \  | | | __| | |  / _` | | | | | |_  /  / _` | | __| | |  / _ \  | '_ \ 
#    | |  | | | | | | | |_  | | | (_| | | | | |  / /  | (_| | | |_  | | | (_) | | | | |
#   |___| |_| |_| |_|  \__| |_|  \__,_| |_| |_| /___|  \__,_|  \__| |_|  \___/  |_| |_|
#                                                                                      

root = Tk()

# Create the Window
root.geometry('450x190')
root.title('FAH Status')
root.wm_iconbitmap('C:\Program Files (x86)\FAHClient\FAHClient.ico')
root.resizable(width=FALSE, height=FALSE)

user = getpass.getuser()
old = time.time()

intervals = (
	('weeks', 604800),  # 60 * 60 * 24 * 7
	('days', 86400),    # 60 * 60 * 24
	('hours', 3600),    # 60 * 60
	('minutes', 60),
	('seconds', 1),
	)


#    ___                 _             _   _           _     _                 
#   |_ _|  _ __    ___  | |_    __ _  | | | |   __ _  | |_  (_)   ___    _ __  
#    | |  | '_ \  / __| | __|  / _` | | | | |  / _` | | __| | |  / _ \  | '_ \ 
#    | |  | | | | \__ \ | |_  | (_| | | | | | | (_| | | |_  | | | (_) | | | | |
#   |___| |_| |_| |___/  \__|  \__,_| |_| |_|  \__,_|  \__| |_|  \___/  |_| |_|
#                                                                              

def find_if_installed():
	if os.path.isdir("C:\Program Files\FAHStatus"):
		pass
	else:
		install()

def find_if_auto_startup():
	if os.path.exists("C:\Users\\" + user + "\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\FAHStatus.lnk"):
		pass
	else:
		add_to_startup()

def find_if_start_menu():
	if os.path.exists("C:\Users\\" + user + "\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\FAHStatus\FAHStatus.lnk"):
		pass
	else:
		add_to_start_menu()

def find_if_desktop():
	desktop = winshell.desktop()
	path = os.path.join(desktop, "FAHStatus.lnk")
	if os.path.exists(path):
		pass
	else:
		add_to_desktop()

def install():
	current_directory = os.getcwd()
	find_if_desktop()
	find_if_auto_startup()
	find_if_start_menu()
	shutil.move(current_directory,"C:\Program Files")


def add_to_desktop():
	desktop = winshell.desktop()
	path = os.path.join(desktop, "FAHStatus.lnk")
	target = r"C:\\Program Files\\FAHStatus\\FAHStatus.exe"
	wDir = r"C:\\Program Files\\FAHStatus"
	icon = r"C:\\Program Files (x86)\\FAHClient\\FAHClient.ico"
	 
	shell = Dispatch('WScript.Shell')
	shortcut = shell.CreateShortCut(path)
	shortcut.Targetpath = target
	shortcut.WorkingDirectory = wDir
	shortcut.IconLocation = icon
	shortcut.save()

def add_to_start_menu():
	os.mkdir("C:\Users\\" + user + "\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\FAHStatus")
	start_directory = "C:\Users\\" + user + "\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\FAHStatus"
	path = os.path.join(start_directory, "FAHStatus.lnk")
	target = r"C:\\Program Files\\FAHStatus\\FAHStatus.exe"
	wDir = r"C:\\Program Files\\FAHStatus"
	icon = r"C:\\Program Files (x86)\\FAHClient\\FAHClient.ico"
	 
	shell = Dispatch('WScript.Shell')
	shortcut = shell.CreateShortCut(path)
	shortcut.Targetpath = target
	shortcut.WorkingDirectory = wDir
	shortcut.IconLocation = icon
	shortcut.save()

def add_to_startup():
	start_directory = "C:\Users\\" + user + "\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
	path = os.path.join(start_directory, "FAHStatus.lnk")
	target = r"C:\\Program Files\\FAHStatus\\FAHStatus.exe"
	wDir = r"C:\\Program Files\\FAHStatus"
	icon = r"C:\\Program Files (x86)\\FAHClient\\FAHClient.ico"
	 
	shell = Dispatch('WScript.Shell')
	shortcut = shell.CreateShortCut(path)
	shortcut.Targetpath = target
	shortcut.WorkingDirectory = wDir
	shortcut.IconLocation = icon
	shortcut.save()

#    _____   _                            _____                          _     _                       
#   |_   _| (_)  _ __ ___     ___        |  ___|  _   _   _ __     ___  | |_  (_)   ___    _ __    ___ 
#     | |   | | | '_ ` _ \   / _ \       | |_    | | | | | '_ \   / __| | __| | |  / _ \  | '_ \  / __|
#     | |   | | | | | | | | |  __/       |  _|   | |_| | | | | | | (__  | |_  | | | (_) | | | | | \__ \
#     |_|   |_| |_| |_| |_|  \___|       |_|      \__,_| |_| |_|  \___|  \__| |_|  \___/  |_| |_| |___/
#                                                                                                                                                                       

def display_time(seconds, granularity=2):
	result = []

	for name, count in intervals:
		value = seconds // count
		if value:
			seconds -= value * count
			if value == 1:
				name = name.rstrip('s')
			result.append("{} {}".format(value, name))
	return ' '.join(result[:granularity])

def convert_to_epoch(time):
	if time:
		dt = datetime.strptime(str(time), "%H:%M:%S")
		dt_now = datetime.now()
		dt = dt.replace(year=dt_now.year, month=dt_now.month, day=dt_now.day)
		return int(mktime(dt.timetuple()))
	else:
		return

def convert_utc_to_local_epoch(time):
	if time:
		from_zone = tz.gettz('UTC')
		to_zone = tz.gettz('America/New_York')

		time = datetime.strftime('%Y-%m-%d %H:%M:%S', time)
		utc = datetime.strptime(str(time), '%Y-%m-%d %H:%M:%S')

		utc = utc.replace(tzinfo=from_zone)
		local = utc.astimezone(to_zone)

		return int(mktime(local.timetuple()))
	else: 
		return

#    _____   _               _         _____                          _     _                       
#   |  ___| (_)  _ __     __| |       |  ___|  _   _   _ __     ___  | |_  (_)   ___    _ __    ___ 
#   | |_    | | | '_ \   / _` |       | |_    | | | | | '_ \   / __| | __| | |  / _ \  | '_ \  / __|
#   |  _|   | | | | | | | (_| |       |  _|   | |_| | | | | | | (__  | |_  | | | (_) | | | | | \__ \
#   |_|     |_| |_| |_|  \__,_|       |_|      \__,_| |_| |_|  \___|  \__| |_|  \___/  |_| |_| |___/
#                                                                                                                                     

def find_nvidia_minutes_per_percentage():
	global time_difference
	#try:
	time_difference = int(convert_to_epoch(get_nvidia_latest_time())) - int(convert_to_epoch(get_nvidia_second_latest_time()))

	nvidia_mpf.set(display_time(time_difference))
	# except:
	# 	nvidia_mpf.set("Unknown")
	root.after(1000, find_nvidia_minutes_per_percentage)

def find_nvidia_estimated_completion():
	try:
		percentage_left = 100 -  int(get_nvidia_latest_percentage())
		eta = int(time_difference) * int(percentage_left)
		nvidia_eta.set(display_time(eta))
	except:
		nvidia_eta.set("Unknown")
	root.after(1000, find_nvidia_estimated_completion)

def find_nvidia_time_from_last_precentage():
	try:
		last_percentage = convert_to_epoch(get_nvidia_latest_time())
		last_percentage = last_percentage - 18000

		seconds_from = int(time.time()) - last_percentage

		nvidia_lpu.set(display_time(seconds_from))
	except:
		nvidia_lpu.set("Unknown")
	root.after(1000, find_nvidia_time_from_last_precentage)


def find_amd_minutes_per_percentage():
	global time_difference
	#try:
	time_difference = int(convert_to_epoch(get_amd_latest_time())) - int(convert_to_epoch(get_amd_second_latest_time()))

	amd_mpf.set(display_time(time_difference))
	# except:
	# 	amd_mpf.set("Unknown")
	root.after(1000, find_amd_minutes_per_percentage)

def find_amd_estimated_completion():
	try:
		percentage_left = 100 -  int(get_amd_latest_percentage())
		eta = int(time_difference) * int(percentage_left)
		amd_eta.set(display_time(eta))
	except:
		amd_eta.set("Unknown")
	root.after(1000, find_amd_estimated_completion)

def find_amd_time_from_last_precentage():
	try:
		last_percentage = convert_to_epoch(get_amd_latest_time())
		last_percentage = last_percentage - 18000

		seconds_from = int(time.time()) - last_percentage

		amd_lpu.set(display_time(seconds_from))
	except:
		amd_lpu.set("Unknown")
	root.after(1000, find_amd_time_from_last_precentage)


#    ____            __                       _            __     ___            _   _   
#   |  _ \    ___   / _|  _ __    ___   ___  | |__        / /    / _ \   _   _  (_) | |_ 
#   | |_) |  / _ \ | |_  | '__|  / _ \ / __| | '_ \      / /    | | | | | | | | | | | __|
#   |  _ <  |  __/ |  _| | |    |  __/ \__ \ | | | |    / /     | |_| | | |_| | | | | |_ 
#   |_| \_\  \___| |_|   |_|     \___| |___/ |_| |_|   /_/       \__\_\  \__,_| |_|  \__|
#                                                                                        

def quit():
	root.quit()

# Function to Manually Refresh the Log and Progress Bar
def refresh():

	# Find the latest percentage from Log
	nvidia_latest_percentage = get_nvidia_latest_percentage()
	if nvidia_latest_percentage:
		nvidia_progress_bar["value"] = nvidia_latest_percentage
	else:
		nvidia_progress_bar["value"] = 0

	amd_latest_percentage = get_amd_latest_percentage()
	if amd_latest_percentage:
		amd_progress_bar["value"] = amd_latest_percentage
	else:
		amd_progress_bar["value"] = 0

	global old
	old = time.time()

# Function to Automatically Refresh the Log and Progress Bar 
def refresh_timer():

	# Find the latest percentage from Log
	nvidia_latest_percentage = get_nvidia_latest_percentage()
	if nvidia_latest_percentage:
		nvidia_progress_bar["value"] = nvidia_latest_percentage
	else:
		nvidia_progress_bar["value"] = 0

	amd_latest_percentage = get_amd_latest_percentage()
	if amd_latest_percentage:
		amd_progress_bar["value"] = amd_latest_percentage
	else:
		amd_progress_bar["value"] = 0

	global old
	old = time.time()

	root.after(1000, refresh_timer)


#    _                             _____                          _     _                       
#   | |       ___     __ _        |  ___|  _   _   _ __     ___  | |_  (_)   ___    _ __    ___ 
#   | |      / _ \   / _` |       | |_    | | | | | '_ \   / __| | __| | |  / _ \  | '_ \  / __|
#   | |___  | (_) | | (_| |       |  _|   | |_| | | | | | | (__  | |_  | | | (_) | | | | | \__ \
#   |_____|  \___/   \__, |       |_|      \__,_| |_| |_|  \___|  \__| |_|  \___/  |_| |_| |___/
#                    |___/                                                                      


def get_nvidia_latest_time():
	i = 0
	f = open("C:\Users\\" + user +"\AppData\Roaming\FAHClient\log.txt", 'r+')
	for line in reversed(f.readlines()):
		regex = re.compile("(\d+:\d+:\d+):.*?:FS01:.*?:Completed\s+\d+ out of \d+ steps \(\d+\%\)")
		r = regex.search(line)
		if r:
			i = i + 1
			if i == 1:
				return r.group(1)

def get_nvidia_second_latest_time():
	i = 0
	f = open("C:\Users\\" + user +"\AppData\Roaming\FAHClient\log.txt", 'r+')
	for line in reversed(f.readlines()):
		regex = re.compile("(\d+:\d+:\d+):.*?:FS01:.*?:Completed\s+\d+ out of \d+ steps \(\d+\%\)")
		r = regex.search(line)
		if r:
			i = i + 1
			if i == 2:
				return r.group(1)

# Function to find the latest percentage from the last matching line in the log
def get_nvidia_latest_percentage():
	i = 0
	f = open("C:\Users\\" + user +"\AppData\Roaming\FAHClient\log.txt", 'r+')
	for line in reversed(f.readlines()):
		regex = re.compile("\d+:\d+:\d+:.*?:FS01:.*?:Completed\s+\d+ out of \d+ steps \((\d+)%\)")
		r = regex.search(line)
		if i == 0:
			if r != None:
				i = i + 1
				nvidia_perc.set(str(r.group(1) + "%"))
				return r.group(1)

def get_amd_latest_time():
	i = 0
	f = open("C:\Users\\" + user +"\AppData\Roaming\FAHClient\log.txt", 'r+')
	for line in reversed(f.readlines()):
		regex = re.compile("(\d+:\d+:\d+):.*?:FS00:.*?:Completed\s+\d+ out of \d+ steps \(\d+\%\)")
		r = regex.search(line)
		if r:
			i = i + 1
			if i == 1:
				return r.group(1)

def get_amd_second_latest_time():
	i = 0
	f = open("C:\Users\\" + user +"\AppData\Roaming\FAHClient\log.txt", 'r+')
	for line in reversed(f.readlines()):
		regex = re.compile("(\d+:\d+:\d+):.*?:FS00:.*?:Completed\s+\d+ out of \d+ steps \(\d+\%\)")
		r = regex.search(line)
		if r:
			i = i + 1
			if i == 2:
				return r.group(1)

# Function to find the latest percentage from the last matching line in the log
def get_amd_latest_percentage():
	i = 0
	f = open("C:\Users\\" + user +"\AppData\Roaming\FAHClient\log.txt", 'r+')
	for line in reversed(f.readlines()):
		regex = re.compile("\d+:\d+:\d+:.*?:FS00:.*?:Completed\s+\d+ out of \d+ steps \((\d+)%\)")
		r = regex.search(line)
		if i == 0:
			if r != None:
				i = i + 1
				amd_perc.set(str(r.group(1) + "%"))
				return r.group(1)


#    ____                                                           ____                 
#   |  _ \   _ __    ___     __ _   _ __    ___   ___   ___        | __ )    __ _   _ __ 
#   | |_) | | '__|  / _ \   / _` | | '__|  / _ \ / __| / __|       |  _ \   / _` | | '__|
#   |  __/  | |    | (_) | | (_| | | |    |  __/ \__ \ \__ \       | |_) | | (_| | | |   
#   |_|     |_|     \___/   \__, | |_|     \___| |___/ |___/       |____/   \__,_| |_|   
#                           |___/                                                        

# Make the Progress Bar
nvidia_progress_bar = ttk.Progressbar(root, style="red.Horizontal.TProgressbar", orient="horizontal",length = 270, mode ="determinate")
nvidia_progress_bar.place(x=180, y=0)
nvidia_progress_bar["maximum"] = 100

# Make the Progress Bar
amd_progress_bar = ttk.Progressbar(root, style="red.Horizontal.TProgressbar", orient="horizontal",length = 270, mode ="determinate")
amd_progress_bar.place(x=180, y=29)
amd_progress_bar["maximum"] = 100


#    ____            _     _                         
#   | __ )   _   _  | |_  | |_    ___    _ __    ___ 
#   |  _ \  | | | | | __| | __|  / _ \  | '_ \  / __|
#   | |_) | | |_| | | |_  | |_  | (_) | | | | | \__ \
#   |____/   \__,_|  \__|  \__|  \___/  |_| |_| |___/
#                                                    

# Create the Refresh button
refresh_button = Button(root, text="Refresh", command=refresh)
refresh_button.place(x=80, y=160)

# Create the Quit button
quit_button = Button(root, text="Quit", command=quit)
quit_button.place(x=290, y=160)

#    _  __    _               _              _       
#   (_)/ /   | |       __ _  | |__     ___  | |  ___ 
#     / /    | |      / _` | | '_ \   / _ \ | | / __|
#    / /_    | |___  | (_| | | |_) | |  __/ | | \__ \
#   /_/(_)   |_____|  \__,_| |_.__/   \___| |_| |___/
#                                                                                                                   

# AMD Label
amd = StringVar()
amdgpu = Label(root, textvariable=amd)
labelfont = ('tahoma', 12, 'bold')
amdgpu.place(x=13, y=28)
amdgpu.config(font=labelfont)
amd.set(str("AMD GPU:"))

# Nvidia Label
nvidia = StringVar()
nvidiagpu = Label(root, textvariable=nvidia)
nvidiagpu.place(x=0, y=2)
nvidiagpu.config(font=labelfont)
nvidia.set(str("Nvidia GPU:"))

#    _  __   __     __                 _           _       _              
#   (_)/ /   \ \   / /   __ _   _ __  (_)   __ _  | |__   | |   ___   ___ 
#     / /     \ \ / /   / _` | | '__| | |  / _` | | '_ \  | |  / _ \ / __|
#    / /_      \ V /   | (_| | | |    | | | (_| | | |_) | | | |  __/ \__ \
#   /_/(_)      \_/     \__,_| |_|    |_|  \__,_| |_.__/  |_|  \___| |___/
#      

amd_perc = StringVar()
amd_percentage = Label(root, textvariable=amd_perc)
amd_percentage.config(font=labelfont)
amd_percentage.place(x=120, y=28)
amd_perc.set(str("Unknown"))

nvidia_perc = StringVar()
nvidia_percentage = Label(root, textvariable=nvidia_perc)
nvidia_percentage.config(font=labelfont)
nvidia_percentage.place(x=120, y=3)
nvidia_perc.set(str("Unknown"))


#    ___            __                 _               _              _ 
#   |_ _|  _ __    / _|   ___         | |       __ _  | |__     ___  | |
#    | |  | '_ \  | |_   / _ \        | |      / _` | | '_ \   / _ \ | |
#    | |  | | | | |  _| | (_) |       | |___  | (_| | | |_) | |  __/ | |
#   |___| |_| |_| |_|    \___/        |_____|  \__,_| |_.__/   \___| |_|
#                                                                       

# AMD Label
amd_info = StringVar()
info_labelfont = ('tahoma', 16, 'bold', 'underline')
amdgpu_info = Label(root, textvariable=amd)
amdgpu_info.place(x=62, y=63)
amdgpu_info.config(font=info_labelfont)
amd_info.set(str("AMD GPU:"))

# AMD Label
nvidia_info = StringVar()
info_labelfont = ('tahoma', 16, 'bold', 'underline')
nvidiagpu_info = Label(root, textvariable=nvidia)
nvidiagpu_info.place(x=272, y=63)
nvidiagpu_info.config(font=info_labelfont)
nvidia_info.set(str("Nvidia GPU:"))


#    _   _           _       _   _                 _               _              _       
#   | \ | | __   __ (_)   __| | (_)   __ _        | |       __ _  | |__     ___  | |  ___ 
#   |  \| | \ \ / / | |  / _` | | |  / _` |       | |      / _` | | '_ \   / _ \ | | / __|
#   | |\  |  \ V /  | | | (_| | | | | (_| |       | |___  | (_| | | |_) | |  __/ | | \__ \
#   |_| \_|   \_/   |_|  \__,_| |_|  \__,_|       |_____|  \__,_| |_.__/   \___| |_| |___/
#                                                                                         

# Create 1% Pre Bold
nvidia_per_label = StringVar()
nvidiaoneper = Label(root, textvariable=nvidia_per_label)
nvidiaoneper.place(x=26, y=93)
nvidiaoneper.config(font=('tahoma', 10, 'bold'))
nvidia_per_label.set(str("Last TPF:"))

# ETA Bold
nvidia_eta_label = StringVar()
nvidiaestimated = Label(root, textvariable=nvidia_eta_label)
nvidiaestimated.place(x=10, y=110)
nvidiaestimated.config(font=('tahoma', 10, 'bold'))
nvidia_eta_label.set(str("Completion:"))

# Create 1% Pre Bold
nvidia_last_label = StringVar()
nvidiaonelast = Label(root, textvariable=nvidia_last_label)
nvidiaonelast.place(x=10, y=127)
nvidiaonelast.config(font=('tahoma', 10, 'bold'))
nvidia_last_label.set(str("Last Frame:"))


#       _      __  __   ____          _               _              _       
#      / \    |  \/  | |  _ \        | |       __ _  | |__     ___  | |  ___ 
#     / _ \   | |\/| | | | | |       | |      / _` | | '_ \   / _ \ | | / __|
#    / ___ \  | |  | | | |_| |       | |___  | (_| | | |_) | |  __/ | | \__ \
#   /_/   \_\ |_|  |_| |____/        |_____|  \__,_| |_.__/   \___| |_| |___/
#                                                                            

# Create 1% Pre Bold
amd_per_label = StringVar()
amdoneper = Label(root, textvariable=amd_per_label)
amdoneper.place(x=246, y=93)
amdoneper.config(font=('tahoma', 10, 'bold'))
amd_per_label.set(str("Last TPF:"))

# ETA Bold
amd_eta_label = StringVar()
amdestimated = Label(root, textvariable=amd_eta_label)
amdestimated.place(x=230, y=110)
amdestimated.config(font=('tahoma', 10, 'bold'))
amd_eta_label.set(str("Completion:"))

# Create 1% Pre Bold
amd_last_label = StringVar()
amdonelast = Label(root, textvariable=amd_last_label)
amdonelast.place(x=230, y=127)
amdonelast.config(font=('tahoma', 10, 'bold'))
amd_last_label.set(str("Last Frame:"))

#       _      __  __   ____         __     __                 _           _       _              
#      / \    |  \/  | |  _ \        \ \   / /   __ _   _ __  (_)   __ _  | |__   | |   ___   ___ 
#     / _ \   | |\/| | | | | |        \ \ / /   / _` | | '__| | |  / _` | | '_ \  | |  / _ \ / __|
#    / ___ \  | |  | | | |_| |         \ V /   | (_| | | |    | | | (_| | | |_) | | | |  __/ \__ \
#   /_/   \_\ |_|  |_| |____/           \_/     \__,_| |_|    |_|  \__,_| |_.__/  |_|  \___| |___/
#                                                                                                 

# Create Minutes per Percentage Field
amd_mpf = StringVar()
amd_minutes_per_percentage = Label(root, textvariable=amd_mpf)
amd_minutes_per_percentage.place(x=95, y=94)
amd_mpf.set(str("Unknown"))

# Create Minutes per Percentage Field
amd_eta = StringVar()
estimated_completion = Label(root, textvariable=amd_eta)
estimated_completion.place(x=95, y=112)
amd_eta.set(str("Unknown"))

# Create Minutes per Percentage Field
amd_lpu = StringVar()
amd_last_percentage_update = Label(root, textvariable=amd_lpu)
amd_last_percentage_update.place(x=95, y=129)
amd_lpu.set(str("Unknown"))


#    _   _           _       _   _                __     __                 _           _       _              
#   | \ | | __   __ (_)   __| | (_)   __ _        \ \   / /   __ _   _ __  (_)   __ _  | |__   | |   ___   ___ 
#   |  \| | \ \ / / | |  / _` | | |  / _` |        \ \ / /   / _` | | '__| | |  / _` | | '_ \  | |  / _ \ / __|
#   | |\  |  \ V /  | | | (_| | | | | (_| |         \ V /   | (_| | | |    | | | (_| | | |_) | | | |  __/ \__ \
#   |_| \_|   \_/   |_|  \__,_| |_|  \__,_|          \_/     \__,_| |_|    |_|  \__,_| |_.__/  |_|  \___| |___/
#                                                                                                              

# Create Minutes per Percentage Field
nvidia_mpf = StringVar()
nvidia_minutes_per_percentage = Label(root, textvariable=nvidia_mpf)
nvidia_minutes_per_percentage.place(x=315, y=94)
nvidia_mpf.set(str("Unknown"))

# Create Minutes per Percentage Field
nvidia_eta = StringVar()
estimated_completion = Label(root, textvariable=nvidia_eta)
estimated_completion.place(x=315, y=112)
nvidia_eta.set(str("Unknown"))

# Create Minutes per Percentage Field
nvidia_lpu = StringVar()
nvidia_last_percentage_update = Label(root, textvariable=nvidia_lpu)
nvidia_last_percentage_update.place(x=315, y=129)
nvidia_lpu.set(str("Unknown"))


#    ____                                        _                                  _____                          _     _                       
#   |  _ \    ___   _ __    ___    ___   _ __   | |_    __ _    __ _    ___        |  ___|  _   _   _ __     ___  | |_  (_)   ___    _ __    ___ 
#   | |_) |  / _ \ | '__|  / __|  / _ \ | '_ \  | __|  / _` |  / _` |  / _ \       | |_    | | | | | '_ \   / __| | __| | |  / _ \  | '_ \  / __|
#   |  __/  |  __/ | |    | (__  |  __/ | | | | | |_  | (_| | | (_| | |  __/       |  _|   | |_| | | | | | | (__  | |_  | | | (_) | | | | | \__ \
#   |_|      \___| |_|     \___|  \___| |_| |_|  \__|  \__,_|  \__, |  \___|       |_|      \__,_| |_| |_|  \___|  \__| |_|  \___/  |_| |_| |___/
#                                                              |___/                                                                             

# Find the latest percentage from Log
nvidia_latest_percentage = get_nvidia_latest_percentage()
if nvidia_latest_percentage:
	nvidia_progress_bar["value"] = nvidia_latest_percentage
else:
	nvidia_progress_bar["value"] = 0

amd_latest_percentage = get_amd_latest_percentage()
if amd_latest_percentage:
	amd_progress_bar["value"] = amd_latest_percentage
else:
	amd_progress_bar["value"] = 0


#    ____    _                    _           _                                   
#   / ___|  | |_    __ _   _ __  | |_        | |       ___     ___    _ __    ___ 
#   \___ \  | __|  / _` | | '__| | __|       | |      / _ \   / _ \  | '_ \  / __|
#    ___) | | |_  | (_| | | |    | |_        | |___  | (_) | | (_) | | |_) | \__ \
#   |____/   \__|  \__,_| |_|     \__|       |_____|  \___/   \___/  | .__/  |___/
#                                                                    |_|          

find_if_installed()
root.after(1, refresh_timer)
root.after(1, find_nvidia_minutes_per_percentage)
root.after(1, find_nvidia_time_from_last_precentage)
root.after(1, find_nvidia_estimated_completion)
root.after(1, find_amd_minutes_per_percentage)
root.after(1, find_amd_time_from_last_precentage)
root.after(1, find_amd_estimated_completion)
root.mainloop()

