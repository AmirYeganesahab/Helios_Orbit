'''
Created on Jan 17, 2019

@author: root
'''
#!/usr/bin/env python3
import os
import GUI.config as config
import importlib

packs = ['tkcalendar','tkfilebrowser','numpy', 'tkinter', 'datetime', 'tkcalendar', 'cython', 'matplotlib', 'xarray', 'h5py', 'pandas', 'matplotlib','astropy']
config.Mainpath = os.path.dirname(os.path.abspath(__file__))

for pack in packs:
    try:
        globals()[pack] = importlib.import_module(pack)
    except:
        command = ('echo {}|sudo -S sudo python3 -m pip install '+pack).format('kuscu1234')
        os.system(command)

from GUI import *
import numpy as np
from tkinter import *
import tkinter#, Tkconstants, TkFileDialog
import datetime
from GUI.logLoad import *

from GUI.initialize import *
from GUI.settingsWindow import *
from GUI.settingsWindow import settings
from GUI.buttons import browse_button_ws
from GUI.workSpace import *
from GNSS import *
from GNSS import Rinex
from GUI import getPassword
from tkinter import scrolledtext
import math
    
# =================================== convert crnx2rnx ===================================
dataPath = '/home/gravity/Dropbox/Sample Data/cham0140.06d.Z'

class OTK:
    '''
    classdocs
    '''
    def __init__(self,root):
        '''
        Constructor
        '''
        global workspace
        #create File menu
        menubar = Menu(root)
        menu = Menu(menubar, tearoff = 0)
        
        menu.add_command(label=" Work space    ", command = WorkSpace)
        menu.add_separator()
        config.master = root
        menu.add_command(label=" Settings    ", command = settings)
        menu.add_separator()
        menu.add_command(label = " Exit    ", command = root.quit)
        
        menubar.add_cascade(label = " File    ", menu = menu)
        
        PreProcessMenu = Menu(menubar, tearoff = 0)
        PreProcessMenu.add_command(label = 'Rinex    ', command = Rinex)
        menubar.add_cascade(label = " Pre Processing    ", menu = PreProcessMenu)

        root.config(menu = menubar)
    def initiate(self):
        config.currentDT = datetime.datetime.now()
      
if __name__ == '__main__':
    global currentDT 
    config.currentDT = datetime.datetime.now()
    # Create Main Window
    root = Tk()
    root.geometry("1000x800")
    root.title('Orbit Determination Toolkit_AYS')
    # Make the main window as Paned Window to be able to resize each grid section manually
    pw = PanedWindow(root, orient = VERTICAL)
    pw.pack(fill="both", expand=True)
    # frame at the top (where the processing plots will appear.)
    f0 = Frame(pw, width = 100, height = 700, bg = 'white', borderwidth = 5)# gps ground track
    f1 = Frame(pw, width = 400, height = 400) # the skyplot and snr plot frame
    f2 = Frame(pw, width = 400, height = 400, borderwidth = 5) # Text box
    f3 = Frame(pw, width = 400, height = 400, bg = 'black', borderwidth = 5) # Entry
    # make frames panable
    pw.add(f0,stretch="always")
    pw.panecget(f0, "stretch")
    pw.add(f1,stretch="always")
    pw.panecget(f1, "stretch")
    pw.add(f2,stretch="always")
    pw.panecget(f2, "stretch")
    pw.add(f3,stretch="always")
    pw.panecget(f3, "stretch")
    # 
    text = Text(f2, height=3, width=400, wrap="none", padx=1, pady=5, bg = '#300A24', fg = 'lawn green')
    ysb = Scrollbar(f2, orient="vertical", command=text.yview,bg = '#300A24')
    xsb = Scrollbar(f2, orient="horizontal", command=text.xview,bg = '#300A24')
    text.configure(yscrollcommand=ysb.set, xscrollcommand=xsb.set)
    text.config(insertbackground = 'white')
    f2.grid_rowconfigure(0, weight = 2)
    f2.columnconfigure(0, weight = 2)
    text.grid_rowconfigure(0, weight = 1)
    text.grid_columnconfigure(0, weight = 1)
    xsb.pack(side = TOP, fill = X)
    ysb.pack(side = RIGHT, fill = Y)
    text.pack(fill = BOTH, expand = YES)
    
    lbl = Label(f3, text = '>>> ', bg = '#300A24', fg = 'greenyellow')
    lbl.pack(side = LEFT)
    command = StringVar()
    ent = Entry(f3 ,textvariable = command, bg = '#300A24', fg = 'greenyellow')
    value = ent.get()
    ent.config(insertbackground = 'white')  
    ent.pack(side = RIGHT, fill=X, expand=YES, ipady=3)
    
    def comp_s(event):
        global s
        os.system('{} > {}'.format(command.get(),config.tempPath))
        with open(config.tempPath) as fp0:
            for row,line in enumerate(fp0):
                config.terminal.append(line)
                text.insert(END, "{}".format(line))
        ent.delete(0, 'end')
        text.see("end")

    ent.bind('<Return>', comp_s)

    config.master = root
    config.inputDirs = initialize_inputDirs(root)
    config.settings = initialize_settings(root)

    loadvariables()
    print(config.OntheFly)
    
    WorkSpace()

    m = OTK(root)

    root.mainloop()