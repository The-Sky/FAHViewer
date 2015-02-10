#!/usr/bin/python
# -*- coding: utf-8 -*-

from Tkinter import *
import tkFont
import ttk
from ttk import Frame, Button, Label, Style
import datetime, time, threading, sys, ttk, re
global progress_bar, log_field, lastupdated, mGui, last_updated, v, z
import getpass

user = getpass.getuser()
old = time.time()

def find_seconds_from_run():
    now = time.time()
    float_seconds_from = now - old
    seconds_from = str(int(round(float(float_seconds_from))))
    v.set(str(seconds_from + " seconds ago"))
    mGui.after(1000, find_seconds_from_run)

def find_minutes_per_percentage():
    latest_time = re.sub(':', '', get_latest_time())
    second_latest_time = re.sub(':', '', get_second_latest_time())

    time_difference = int(latest_time) - int(second_latest_time)

    mmp = str(round(float(time_difference)/60, 2))
    z.set(str(mmp + " minutes"))
    mGui.after(10000, find_minutes_per_percentage)

# Function to Manually Refresh the Log and Progress Bar
def refresh():
    log_field.delete(1.0, END)

    get_last_log_lines()

    # Find the latest percentage from Log
    latest_percentage = get_latest_percentage()
    if latest_percentage:
        progress_bar["value"] = latest_percentage
    else:
        raise Exception("Unable to find latest percentage.")

    # y.set(str(progress_bar["value"]) + "%")
    # now = time.strftime("%I:%M:%S")
    # v.set(str("Last Updated: " + now))

# Function to Automatically Refresh the Log and Progress Bar 
def refresh_timer():
    log_field.delete(1.0, END)
    
    get_last_log_lines()

    # Find the latest percentage from Log
    latest_percentage = get_latest_percentage()
    if latest_percentage:
        progress_bar["value"] = latest_percentage
    else:
        raise Exception("Unable to find latest percentage.")

    global old
    old = time.time()
    find_seconds_from_run()

    # now = time.strftime("%I:%M:%S")
    # v.set(str("Last Updated: " + now))
    # y.set(str(progress_bar["value"]) + "%")
    mGui.after(10000, refresh_timer)

def quit():
    mGui.quit()

def get_last_log_lines():
    i = 0
    f = open("C:\Users\\" + user +"\AppData\Roaming\FAHClient\log.txt", 'r+')
    for line in reversed(f.readlines()):
        regex = re.compile("(Completed \d+ out of \d+ steps \(\d+%\))")
        r = regex.search(line)
        if r:
            i = i + 1
            if i == 1:
                log_field.insert(INSERT, r.group(1))


def get_latest_time():
    i = 0
    f = open("C:\Users\\" + user +"\AppData\Roaming\FAHClient\log.txt", 'r+')
    for line in reversed(f.readlines()):
        regex = re.compile("(\d+:\d+:\d+):.*?:.*?:.*?:Completed \d+ out of \d+ steps \((\d+)%\)")
        r = regex.search(line)
        if r:
            i = i + 1
            if i == 1:
                return r.group(1)

def get_second_latest_time():
    i = 0
    f = open("C:\Users\\" + user +"\AppData\Roaming\FAHClient\log.txt", 'r+')
    for line in reversed(f.readlines()):
        regex = re.compile("(\d+:\d+:\d+):.*?:.*?:.*?:Completed \d+ out of \d+ steps \((\d+)%\)")
        r = regex.search(line)
        if r:
            i = i + 1
            if i == 2:
                return r.group(1)

# Function to find the latest percentage from the last matching line in the log
def get_latest_percentage():
    i = 0
    f = open("C:\Users\\" + user +"\AppData\Roaming\FAHClient\log.txt", 'r+')
    for line in reversed(f.readlines()):
        regex = re.compile("Completed \d+ out of \d+ steps \((\d+)%\)")
        r = regex.search(line)
        if i == 0:
            if r != None:
                i = i + 1
                return r.group(1)

mGui = Tk()

# Create the Window
mGui.geometry('360x80')
mGui.title('F@H Percentage Viewer')
mGui.wm_iconbitmap('C:\Program Files (x86)\FAHClient\FAHClient.ico')
mGui.wm_attributes("-topmost", 1)
mGui.resizable(width=FALSE, height=FALSE)

# Create the Text Field
log_field = Text(mGui, height=1)
log_field.place(x=0, y=0)

# Insert the Log into the Text Field
get_last_log_lines()

# Make the Progress Bar
progress_bar = ttk.Progressbar(mGui,orient="horizontal",length = 360, mode ="determinate")
progress_bar.place(x=0, y=20)
progress_bar["maximum"] = 100

# Find the latest percentage from Log
latest_percentage = get_latest_percentage()
if latest_percentage:
    progress_bar["value"] = latest_percentage
else:
    progress_bar["value"] = 0

# Create 1% Pre Bold
update = StringVar()
last = Label(mGui, textvariable=update)
last.place(x=11,y=40)
last.config(font=('system', 2, 'bold'))
update.set(str("Last Updated:"))

# Find the last time the log/progress bar was refreshed.
v = StringVar()
last_updated = Label(mGui, textvariable=v)
last_updated.place(x=110,y=41)
v.set(str("0 seconds ago"))

# Create the Refresh button
refresh_button = Button(mGui, text="Refresh", command=refresh)
refresh_button.place(x=200, y=55)

# Create the Quit button
quit_button = Button(mGui, text="Quit", command=quit)
quit_button.place(x=280, y=55)

# Create 1% Pre Bold
per = StringVar()
oneper = Label(mGui, textvariable=per)
oneper.place(x=0, y=58)
oneper.config(font=('system', 2, 'bold'))
per.set(str("1 Percent Each:"))

# Create Minutes per Percentage Field
z = StringVar()
minutes_per_percentage = Label(mGui, textvariable=z)
minutes_per_percentage.place(x=110, y=60)
z.set(str("0 minutes"))

mGui.after(1, refresh_timer)
mGui.after(1, find_seconds_from_run)
mGui.after(1, find_minutes_per_percentage)
mGui.mainloop()

