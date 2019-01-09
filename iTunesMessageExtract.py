# !/usr/bin/python3

# Created by Matthew Kesselring
# v1.0
# 24 June 2018
# By running this program, the user assumes all responsibility for any file
#     modifications directly caused by this program.
# This program is free to use in whole or in part on the condition that these
#     header comments are included and remain unmodified.

import sqlite3
import datetime
import os
from tkinter import *
from tkinter import messagebox

# Find all subdirectories of the given path
def all_subdirs_of(b='.'):
   result = []
   for d in os.listdir(b):
      bd = os.path.join(b, d)
      if os.path.isdir(bd): result.append(bd)
   return result

# Get the path to the iTunes backups folder
path = os.getenv('APPDATA') + "\Apple Computer\MobileSync\Backup"
# Get most recent backup folder
all_subdirs = all_subdirs_of(path)
latest_subdir = max(all_subdirs, key=os.path.getmtime)
# Get file containing message backups
path = latest_subdir + '\\3d\\3d0d7e5fb2ce288813306e4d4636395e047a3d28'
# Open database connection to message backups
conn = sqlite3.connect(path)
c = conn.cursor()

# Open GUI for phone number input
top = Tk()
L1 = Label(top,  font = "Calibri 12", text="10-digit Phone number (no spaces, only numbers)")
L1.pack()
E1 = Entry(top, bd =5, font = "Calibri 12")
E1.pack()
s = ""

# When GUI button is pressed, find messages
def callback(event=None):
   s = E1.get()
   try:
      int(s)
   except ValueError:
      messagebox.showerror("Phone Number", "Invalid phone number")
      return
   n = ('+1'+s,) # Prepend '+1' country code
   ids = []
   
   # Find all handle_id's for phone number (SMS and iMessage to the same number
   #     have different id's)
   for row in c.execute("SELECT ROWID FROM handle WHERE id = ?", n):
      a, = row
      ids.append(a)
   # Output file name = [phone number]_[year]-[month]-[day].txt
   now = datetime.datetime.now()
   year = str(now.year)
   month = str(now.month)
   day = str(now.day)
   file = s + "_" + year + "-" + month + "-" + day + ".txt"
   text_file = open(file, "w")
   
   # If only iMessage or SMS (not both)
   if len(ids) == 1:
      for row in c.execute("SELECT datetime(substr(date, 1, 9) + 978307200, 'unixepoch', 'localtime') as date, service, is_from_me, text FROM message WHERE handle_id = ?", (ids[0],)):
         try:
            d, serv, f, t = row
            if f:
               sent = "Sent"
            else:
               sent = "Recv"
            # Format = ([date and time of message], [iMessage or SMS], [sent or received], [message text])
            text_file.write(str((d,serv,sent,t)))
            text_file.write('\n')
         # If message was a picture, causes exception
         except UnicodeEncodeError:
            d, serv, f, t = row
            text_file.write(str((d,serv,sent,'UNABLE TO FIND IMAGE')))
            text_file.write('\n')
   elif len(ids) == 2:
      for row in c.execute("SELECT datetime(substr(date, 1, 9) + 978307200, 'unixepoch', 'localtime') as date, service, is_from_me, text FROM message WHERE handle_id = ? OR handle_id = ?", (ids[0], ids[1])):
         try:
            d, serv, f, t = row
            if f:
               sent = "Sent"
            else:
               sent = "Recv"
            # Format = ([date and time of message], [iMessage or SMS], [sent or received], [message text])
            text_file.write(str((d,serv,sent,t)))
            text_file.write('\n')
         # If message was a picture, causes exception
         except UnicodeEncodeError:
            d, serv, f, t = row
            text_file.write(str((d,serv,sent,'UNABLE TO FIND IMAGE')))
            text_file.write('\n')
   # Close output file     
   text_file.close()
   # Notify user
   messagebox.showinfo("Information","Messages saved to file")
   # Close phone number input GUI
   top.withdraw()
   top.quit()

# Auto focus on entry field
E1.focus()
# Bind enter key to button press
top.bind('<Return>', callback)
# Create button
b = Button(top, text="get", font = "Calibri 12", width=20, command=callback)
b.pack()
top.mainloop()

