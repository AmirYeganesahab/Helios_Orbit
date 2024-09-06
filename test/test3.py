'''
Created on Feb 8, 2019

@author: root
'''
#!/usr/bin/python3



from tkinter import *
# from '/home/geomatics/Dropbox/eclipse-workspace/SatWare_v004/GUI' import *
import GUI.config as config

config.password = []
def getpwd():
    password = ''
    root = Tk()
    root.wait_visibility(root)
    root.configure(background='black')
    root.wm_attributes('-alpha',0.7)
    root.geometry("300x150")
    pwdbox = Entry(root, show = '*', background='black', fg="white")
    #pwdbox.grid(row = 0, sticky = 'we')
    def onpwdentry(evt):
         password = pwdbox.get()
         root.destroy()
    def onokclick():
         password = pwdbox.get()
         root.destroy()
    lbl1= Label(root, text = 'Password', background='black',fg="white", height = 2).pack(side = 'top')

    pwdbox.pack(side = 'top')
    pwdbox.bind('<Return>', onpwdentry)
    lbl1= Label(root, text = ' ', background='black',fg="white", height = 2).pack(side = 'top')
    Button(root, command=onokclick, text = 'OK', background='black', fg="white", width = 8).pack(side = 'top')

    root.mainloop()
    return password
password = getpwd()
print(password)