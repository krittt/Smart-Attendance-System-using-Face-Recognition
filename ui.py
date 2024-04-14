import tkinter as tk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import cv2,os
import csv
import numpy as np
from threading import Thread
from tkinter import * 
from tkinter.ttk import *
from PIL import Image,ImageTk
import pandas as pd
import datetime
import time

from Take_Attendance import take_attendance

window = tk.Tk()

class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=3
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)            
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom

app=FullScreenApp(window)

class Example(Frame):
    def __init__(self, master, *pargs):
        Frame.__init__(self, master, *pargs)



        self.image = Image.open("landscape.png")
        self.img_copy= self.image.copy()


        self.background_image = ImageTk.PhotoImage(self.image)

        self.background = Label(self, image=self.background_image)
        self.background.pack(fill=BOTH, expand=YES)
        self.background.bind('<Configure>', self._resize_image)

    def _resize_image(self,event):

        new_width = event.width
        new_height = event.height

        self.image = self.img_copy.resize((new_width, new_height))

        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image =  self.background_image)

e = Example(window)
e.pack(fill=BOTH, expand=YES)
C = tk.Canvas(window, height=600, width=600)

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day,month,year=date.split("-")

mont={'01':'January',
      '02':'February',
      '03':'March',
      '04':'April',
      '05':'May',
      '06':'June',
      '07':'July',
      '08':'August',
      '09':'September',
      '10':'October',
      '11':'November',
      '12':'December'
      }

window.title("Smart Attendance System")

message3 = tk.Label(window, text="Smart Attendance System" ,fg="white",bg="black" ,width=55 ,height=1,font=('Helvetica', 30, ' bold '))
message3.place(relx = 0.5, rely = 0.1, anchor = CENTER)

frame4 = tk.Frame(window, bg="#8a2e7f")
frame4.place(relx=0.5, rely=0.17, relwidth=0.2, relheight=0.05,anchor=CENTER)

datef = tk.Label(frame4, text = day+"-"+mont[month]+"-"+year, fg="white",bg="#262523" ,width=55 ,height=1,font=('Helvetica', 20, ' bold '))
datef.pack(fill='both',expand=1)

frame1 = tk.Frame(window, bg="#ffffff")
frame1.place(relx=0.30, rely=0.21, relwidth=0.41, relheight=0.78)

head1 = tk.Label(frame1, text="                               For Already Registered                                ", fg="white",bg="black" ,font=('Helvetica', 17, ' bold ') )
head1.place(x=0,y=0)

lbl3 = tk.Label(frame1, text="Select Class",width=20,fg="white",bg="black"  ,height=1 ,font=('Helvetica', 13, ' bold '))
lbl3.place(x=200, y=50)

v = tk.IntVar()
v.set(1)
selection=0
def ShowChoice():
    global selection
    selection=v.get()
    print(selection)
  
first=tk.Radiobutton(frame1, text="Hindi", variable=v, command=ShowChoice,
              value=1,bg="#fff",activeforeground="#507d2a",borderwidth=10,font=('Helvetica', 14, ' bold '),foreground="black").place(x=200, y=110,anchor=CENTER)

second=tk.Radiobutton(frame1, text="English", variable=v, command=ShowChoice,
              value=2,bg="#fff",activeforeground="#507d2a",borderwidth=10,font=('Helvetica', 14, ' bold '),foreground="black").place(x=340, y=88)


###########################################################################################################################

def attendance():
    if(selection==1):
        take_attendance("Hindi_attendance/Hindi_Attendance.csv",1)
    else:
        take_attendance("English_attendance/English_Attendance.csv",2)

trackImg = tk.Button(frame1, text="Take Attendance",fg="white"  ,bg="#507d2a" ,command=attendance, width=35  ,height=1, activebackground = "white" ,font=('Helvetica', 15, ' bold '))
trackImg.place(x=95,y=150)

msg1= tk.Label(frame1, text="           For Student Enrolment Or To View Attendance       \nLogin As Admin", fg="white",bg="#00aeff" ,font=('Helvetica', 17, ' bold ') )
msg1.place(x=0,y=230)

lbl = tk.Label(frame1, text="Enter I'D: ",width=18  ,height=1  ,fg="white"  ,bg="black" ,font=('Helvetica', 13, ' bold ') )
lbl.place(x=95,y=340)

txt = tk.Entry(frame1,width=30 ,fg="black",font=('Helvetica', 13 ))
txt.place(x=310,y=340)

lbl2 = tk.Label(frame1, text="Enter Password: ",width=18,height=1   ,fg="white"  ,bg="black" ,font=('Helvetica', 13, ' bold '))
lbl2.place(x=95,y=390)

txt2 = tk.Entry(frame1,width=30 ,show="*",fg="black",font=('Helvetica', 13)  )
txt2.place(x=310,y=390)

def Enter_Admin():
    if(txt.get()=="Admin" and txt2.get()=="qwerty"):
        window.destroy()
        import Admin
    else:
        mess.showerror("Invalid Credentials", "Please check I'D or Password")    
takeImg = tk.Button(frame1, text="Submit",command=Enter_Admin ,fg="white"  ,bg="#8a2e7f"  ,width=25  ,height=1, activebackground = "white" ,font=('Helvetica', 13, ' bold '))

takeImg.place(x=175, y=440)

###############################QUIT###########################################################################################

# res=0
def destroy():
  window.destroy()

quitWindow = tk.Button(frame1, text="Quit",fg="white"  ,bg="red"  ,width=35 ,height=1,command=destroy ,activebackground = "white" ,font=('Helvetica', 15, ' bold '))
quitWindow.place(x=100, y=490)

# # ########################################### END 

window.mainloop()














