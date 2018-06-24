# !/usr/bin/python3
import sqlite3
import datetime
import os
from tkinter import *
from tkinter import messagebox

def all_subdirs_of(b='.'):
   result = []
   for d in os.listdir(b):
      bd = os.path.join(b, d)
      if os.path.isdir(bd): result.append(bd)
   return result

path = os.getenv('APPDATA') + "\Apple Computer\MobileSync\Backup"

all_subdirs = all_subdirs_of(path)
latest_subdir = max(all_subdirs, key=os.path.getmtime)
path = latest_subdir + '\\3d\\3d0d7e5fb2ce288813306e4d4636395e047a3d28'
conn = sqlite3.connect(path)
c = conn.cursor()

top = Tk()
L1 = Label(top,  font = "Calibri 12", text="10-digit Phone number (no spaces, only numbers)")
L1.pack()
E1 = Entry(top, bd =5, font = "Calibri 12")
E1.pack()
s = ""

def callback(event=None):
   s = E1.get()
   n = ('+1'+s,)
   ids = []

   for row in c.execute("SELECT ROWID FROM handle WHERE id = ?", n):
      a, = row
      ids.append(a)
   now = datetime.datetime.now()
   year = str(now.year)
   month = str(now.month)
   day = str(now.day)
   file = s + "_" + year + "-" + month + "-" + day + ".txt"
   text_file = open(file, "w")
   if len(ids) == 1:
      for row in c.execute("SELECT datetime(substr(date, 1, 9) + 978307200, 'unixepoch', 'localtime') as date, service, is_from_me, text FROM message WHERE handle_id = ?", (ids[0],)):
         try:
            d, serv, f, t = row
            if f:
               sent = "Sent"
            else:
               sent = "Recv"
            text_file.write(str((d,serv,sent,t)))
            text_file.write('\n')
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
            text_file.write(str((d,serv,sent,t)))
            text_file.write('\n')
         except UnicodeEncodeError:
            d, serv, f, t = row
            text_file.write(str((d,serv,sent,'UNABLE TO FIND IMAGE')))
            text_file.write('\n')
         
   text_file.close()
   messagebox.showinfo("Information","Messages saved to file")
   top.withdraw()
   top.quit()

E1.focus()
top.bind('<Return>', callback)
b = Button(top, text="get", font = "Calibri 12", width=20, command=callback)
b.pack()
top.mainloop()

