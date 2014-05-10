#!/usr/bin/python
# -*- coding: utf-8 -*-

from Tkinter import *
import ttk
from ttk import Frame, Button, Label, Style
import datetime, time, threading, sys, ttk, re
global mpb, area, lastupdated, mGui, tlabel, v, y

# Function to Manually Refresh the Log and Progress Bar
def refresh():
    area.delete(1.0, END)

    get_last_log_lines()

    # Find the latest percentage from Log
    latest_percentage = get_latest_percentage()
    if latest_percentage:
        mpb["value"] = latest_percentage
    else:
        raise Exception("Unable to find latest percentage.")

    # y.set(str(mpb["value"]) + "%")
    now = time.strftime("%I:%M:%S")
    v.set(str("Last Updated: " + now))

# Function to Automatically Refresh the Log and Progress Bar 
def refresh_timer():
    area.delete(1.0, END)
    
    get_last_log_lines()

    # Find the latest percentage from Log
    latest_percentage = get_latest_percentage()
    if latest_percentage:
        mpb["value"] = latest_percentage
    else:
        raise Exception("Unable to find latest percentage.")

    now = time.strftime("%I:%M:%S")
    v.set(str("Last Updated: " + now))
    # y.set(str(mpb["value"]) + "%")
    mGui.after(10000, refresh_timer)

def quit():
    mGui.quit()

def get_last_log_lines():
    i = 0
    f = open('C:\ProgramData\FAHClient\log.txt', 'r+')
    for line in reversed(f.readlines()):
        regex = re.compile("(Completed \d+ out of \d+ steps \(\d+%\))")
        r = regex.search(line)
        if r:
            i = i + 1
            if i == 1:
                area.insert(INSERT, r.group(1))



# Function to find the latest percentage from the last matching line in the log
def get_latest_percentage():
    i = 0
    f = open('C:\ProgramData\FAHClient\log.txt', 'r+')
    for line in reversed(f.readlines()):
        regex = re.compile("Completed \d+ out of \d+ steps \((\d+)%\)")
        r = regex.search(line)
        if i == 0:
            if r != None:
                i = i + 1
                newvalue = r.group(1)
                return newvalue

mGui = Tk()

# Create the Window
mGui.geometry('360x70')
mGui.title('F@H Percentage Viewer')
mGui.wm_iconbitmap('C:\Program Files (x86)\FAHClient\FAHClient.ico')
mGui.wm_attributes("-topmost", 1)
mGui.resizable(width=FALSE, height=FALSE)
mGui.columnconfigure(1, weight=1)
mGui.columnconfigure(3, pad=7)
mGui.rowconfigure(3, weight=1)
mGui.rowconfigure(5, pad=7)


# Create the Text Field
area = Text(mGui, height=1)
area.grid(row=1, column=0, columnspan=2, rowspan=4, 
    padx=5, sticky=E+W+N)
area.pack()

# Insert the Log into the Text Field
get_last_log_lines()

# Make the Progress Bar
mpb = ttk.Progressbar(mGui,orient="horizontal",length = 360, mode ="determinate")
mpb.grid(row=3, column=2, ipady=10)
mpb.pack()
mpb["maximum"] = 100

# Find the latest percentage from Log
latest_percentage = get_latest_percentage()
if latest_percentage:
    mpb["value"] = latest_percentage
else:
    mpb["value"] = 0

# Find the last time the log/progress bar was refreshed.
now = time.strftime("%I:%M:%S")

v = StringVar()
tlabel = Label(mGui, textvariable=v)
tlabel.grid(row=2, column=1, sticky=W)
tlabel.pack(side=LEFT)
v.set(str("Last Updated: " + now))

# y = StringVar()
# dlabel = Label(mpb, textvariable=y)
# dlabel.place()
# y.set(str(mpb["value"]) + "%")

# Create the Quit button
qbutton = Button(mGui, text="Quit", command=quit)
qbutton.grid(row=2, column=4)
qbutton.pack(side=RIGHT)

# Create the Refresh button
button = Button(mGui, text="Refresh", command=refresh)
button.grid(row=2, column=3)
button.pack(side=RIGHT)

mGui.after(10000, refresh_timer)
mGui.mainloop()
