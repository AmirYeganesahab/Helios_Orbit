'''
Created on Jan 17, 2019

@author: root
'''
#!/usr/bin/env python3

import os
import importlib

packs = ['numpy', 'Tkinter', 'datetime','tkFileDialog','tkfilebrowser','git']

print(os.path.dirname(os.path.abspath(__file__)))

for pack in packs:
    try:
        globals()[pack] = importlib.import_module(pack)
    except:
        import pip
        pip.main(['install', pack])
if not os.path.isdir('/home/gravity/georinex'):
    os.system('git clone https://github.com/scivision/georinex.git -> GNSS')
    # os.system('cd georinex/')
    os.system('python -m pip GNSS/georinex/install -e .')
#         
# packs = ['numpy', 'Tkinter', 'datetime']

import numpy as np
from tkinter import *
import tkinter#, Tkconstants, TkFileDialog
from tkfilebrowser import *
import datetime
from logLoad import *
import config
from initialize import *
from settingsWindow import *
from settingsWindow import settings
from buttons import browse_button_ws
from workSpace import *

class OTK:
    '''
    classdocs
    '''
    def __init__(self,root):
        '''
        Constructor
        '''
        global workspace
        self.root = root
        #create File menu
        menubar = Menu(self.root)
        filemenu = Menu(menubar, tearoff = 0)
        
        config.inputDirs = initialize_inputDirs(self.root)
        config.settings = initialize_settings(self.root)

        filemenu.add_command(label="    Work space    ", command = WorkSpace)
        lbl1 = Label(master=root,textvariable=config.inputDirs['workspace'])
        lbl1.pack()
        filemenu.add_separator()
        config.master = root
        filemenu.add_command(label="    Settings    ", command = settings)
        filemenu.add_separator()
        filemenu.add_command(label = "    Exit    ", command = self.root.quit)
        menubar.add_cascade(label = "    File    ", menu = filemenu)
        
#         #create Edit menu
#         editmenu = Menu(menubar, tearoff=0)
#         editmenu.add_command(label = "Edit Global Constants", command = self.donothing)
#         
#         editmenu.add_separator()
#         
#         editmenu.add_command(label = "Edit Project Constants", command = self.donothing)
#         editmenu.add_command(label = "Copy", command = self.donothing)
#         editmenu.add_command(label = "Paste", command = self.donothing)
#         editmenu.add_command(label = "Delete", command = self.donothing)
#         editmenu.add_command(label = "Select All", command = self.donothing)
#         
#         menubar.add_cascade(label = "Edit", menu = editmenu)
#         
        #create help menu
#         helpmenu = Menu(menubar, tearoff=0)
#         helpmenu.add_command(label = "Help Index", command = self.donothing)
#         helpmenu.add_command(label = "About...", command = self.donothing)
#         menubar.add_cascade(label = "Help", menu = helpmenu)
# 
        self.root.config(menu = menubar)
        
if __name__ == '__main__':
    global currentDT 
    config.currentDT = datetime.datetime.now()
    root = Tk()#Create empty panel
    
    root.geometry("1000x800")
    root.title('Orbit Determination Toolkit_AYS')
    topFrame = Frame(root)#create a frame at the top of the panel
    topFrame.pack()#pack the frame at the top of the panel  
    m = OTK(root)
    
    root.mainloop()