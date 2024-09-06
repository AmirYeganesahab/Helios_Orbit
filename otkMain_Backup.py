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
#from tkfilebrowser import *
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
#import georinex

        
# # =================================== git georinex ===================================
# gitpath = '/usr/bin/git'
# if not os.path.exists(gitpath):
#     os.system('python3 -m pip install GitPython')
## georinex
# path = Mainpath + '/GNSS/georinex/'
# if not os.path.isdir( path ):
#     command = 'git clone https://github.com/scivision/georinex.git '+path
#     os.system(command)
#     command = 'cd '+path + '; python3 -m pip ' + 'install -e .'
#     os.system(command)

# # =================================== Install georinex ===================================
# os.system('echo {}|sudo -S python3 {}setup.py install'.format('geomatics1985',path))
#Compile rnxcmp
# os.system('gcc -ansi -O2 -static rnx2crx.c -o RNX2CRX')

# =================================== make rnxcmp ===================================
# getPassword.getpwd()
#  
# os.system('echo {}|sudo -S make install -C {}/{}/{}'.\
#           format( config.password , config.Mainpath , 'GNSS' , 'rnxcmp' ))
# # =================================== ''''''''''' ===================================
# config.tempPath = config.Mainpath + '/I_O/' + 'temp.tmp'
# os.system('whereis crx2rnx > ' + config.tempPath)
# with open(config.tempPath) as fp0:
#     config.rnxcmpPath = fp0.read().split()[1]
#     fp0.close()
    
# =================================== convert crnx2rnx ===================================
dataPath = '/home/gravity/Dropbox/Sample Data/cham0140.06d.Z'
if dataPath[-2] == '.Z':
    #unzip
    pass
elif dataPath[-2] == '.d':
    #convert
    pass
else:
    #read
    pass

# # =================================== install xTerm ===================================
# os.system('echo {}|sudo -S sudo apt-get update -y'.format(config.password))
# os.system('echo {}|sudo -S sudo apt-get install -y xterm'.format(config.password))

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

  #create Edit menu
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
        root.config(menu = menubar)

     

        
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
    f0 = Frame(pw, width = 100, height = 700, bg = 'white', borderwidth = 5)
    #f1 = Frame(pw, width = 400, height = 400) # X scrollbar
    f2 = Frame(pw, width = 400, height = 400, borderwidth = 5) # Text box
    f3 = Frame(pw, width = 400, height = 400, bg = 'black', borderwidth = 5) # Entry
    
    pw.add(f0,stretch="always")
    pw.panecget(f0, "stretch")
#     pw.add(f1,stretch="always")
#     pw.panecget(f1, "stretch")
    pw.add(f2,stretch="always")
    pw.panecget(f2, "stretch")
    pw.add(f3,stretch="always")
    pw.panecget(f3, "stretch")
       
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

#     ent.grid(row = 2,sticky = 'ew')
    
    
    # ================================= Upper Frame =================================
#     UpFrame = Frame(root, highlightbackground="black",\
#             highlightcolor="black", highlightthickness=1, width=800, height=600, bd= 0)
#     #UpFrame = Frame(root, height=800, width=800, bg = 'white')
#     UpFrame.pack(side = TOP, fill = BOTH, expand=YES)
#     # ================================= Lower Frame =================================
#     cmdFrame = Frame(root, highlightbackground="black",\
#             highlightcolor="black", highlightthickness=1, width=800, height=300, bd= 0)
#     txt = Text(cmdFrame, width=800, bg = 'white')
#     e = Entry(cmdFrame, width=200)
#     e.pack(side = BOTTOM, fill=X, expand=YES, ipady=3)
#     txt.pack(side = TOP, fill = BOTH, expand=YES)
#     cmdFrame.pack(side = BOTTOM, fill = BOTH, expand=YES)
    
#     e.grid(row =1)
    
    
    #root.withdraw()
    config.master = root
    config.inputDirs = initialize_inputDirs(root)
    config.settings = initialize_settings(root)

    loadvariables()
    print(config.OntheFly)
    
    WorkSpace()
    
#     topFrame = Frame(root)#create a frame at the top of the panel
    
#     topFrame.pack()#pack the frame at the top of the panel  
    m = OTK(root)
    #root.bind('<Return>', (lambda event, e=ents: fetch(e)))
    root.mainloop()