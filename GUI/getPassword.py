'''
Created on Feb 8, 2019

@author: root
'''
#!/usr/bin/python3
from tkinter import *
import GUI.config as config



def getpwd():
    password = ''
    root0 = Tk()
    root0.wm_attributes('-type', 'splash')
    root0.wait_visibility(root0)
    root0.configure(background='black')
    root0.wm_attributes('-alpha',0.7)
    root0.geometry("400x200")
    root0.resizable(False, False)
    root0.title('Password Dialog')
    pwdbox = Entry(root0, show = '*', background='black', fg="white")
    #pwdbox.grid(row = 0, sticky = 'we')
    def onpwdentry(evt):
         config.password = pwdbox.get()
         root0.destroy()
    def onokclick():
         config.password = pwdbox.get()
         root0.destroy()
    lbl1= Label(root0, text = 'Password', background='black',fg="white", height = 2).pack(side = 'top')

    pwdbox.pack(side = 'top')
    pwdbox.bind('<Return>', onpwdentry)
    lbl1= Label(root0, text = ' ', background='black',fg="white", height = 2).pack(side = 'top')
    Button(root0, command=onokclick, text = 'OK', background='black', fg="white", width = 8).pack(side = 'top')

    root0.mainloop()
