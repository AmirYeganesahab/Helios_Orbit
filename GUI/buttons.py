import GUI.config as config
from tkinter import *
import tkinter
from tkinter import constants
from tkinter import filedialog
#import Tkinter, Tkconstants, tkFileDialog
import os
from tkfilebrowser import askopendirname
from tkfilebrowser import askopenfilename

def browse_button_ws(dir = '/home/'):
    config.inputDirs['workspace'].set(askopendirname(initialdir = dir,title= 'workspace',foldercreation = True))
    
# def browse_button(dir = '/home/'):
#     
#     if len(config.inputDirs['workspace'].get())>0: dir = config.inputDirs['workspace'].get()
#     if len(config.inputDirs['rinex'].get())>0: dir = config.inputDirs['rinex'].get()
#     elif len(config.inputDirs[config.item].get())>0: dir = config.inputDirs[config.item].get()  
#     dir = (askopendirname(initialdir = dir,title= config.item,foldercreation = FALSE))
#     config.inputDirs[config.item].set(dir)
#          
#     elif config.item == 'brdc':
#          
#         if len(config.inputDirs['rinex'].get())>0: dir = config.inputDirs['rinex'].get() 
#         elif len(config.inputDirs['brdc'].get())>0: dir = config.inputDirs['brdc'].get() 
#         else:dir = config.inputDirs['workspace'].get()
#         dir = (askopendirname(initialdir = dir,title= 'brdc',foldercreation = FALSE))
#         config.inputDirs['brdc'].set(dir)
#          
#     elif config.item == 'peph':
#      
#         if len(config.inputDirs['brdc'].get())>0: dir = config.inputDirs['brdc'].get() 
#         elif len(config.inputDirs['peph'].get())>0: dir = config.inputDirs['peph'].get() 
#         else:dir = config.inputDirs['workspace'].get()
#         dir = (askopendirname(initialdir = dir,title= 'peph',foldercreation = FALSE))
#         config.inputDirs['peph'].set(dir)
#  
#     elif config.item == 'jpl': 
#          
#         if len(config.inputDirs['peph'].get())>0: dir = config.inputDirs['peph'].get() 
#         elif len(config.inputDirs['jpl'].get())>0: dir = config.inputDirs['jpl'].get() 
#         else: dir = config.inputDirs['workspace'].get()
#         dir = (askopendirname(initialdir = dir,title= 'jpl',foldercreation = FALSE))
#         config.inputDirs['jpl'].set(dir)   
#      
#     elif config.item == 'eop': 
#          
#         if len(config.inputDirs['jpl'].get())>0: dir = config.inputDirs['jpl'].get()
#         elif len(config.inputDirs['eop'].get())>0: dir = config.inputDirs['eop'].get() 
#         else: dir = config.inputDirs['workspace'].get()
#         dir = (askopendirname(initialdir = dir,title= 'eop',foldercreation = FALSE))
#         config.inputDirs['eop'].set(dir)
#          
#     elif config.item == 'almanac':
#               
#         if len(config.inputDirs['eop'].get())>0: dir = config.inputDirs['eop'].get()
#         elif len(config.inputDirs['almanac'].get())>0: dir = config.inputDirs['almanac'].get() 
#         else: dir = config.inputDirs['workspace'].get()
#         dir = (askopendirname(initialdir = dir,title= 'almanac',foldercreation = FALSE))
#         config.inputDirs['almanac'].set(dir)
#          
#     elif config.item == 'gravity':
#         if len(config.inputDirs['almanac'].get())>0: dir = config.inputDirs['almanac'].get()
#         elif len(config.inputDirs['gravity'].get())>0: dir = config.inputDirs['gravity'].get() 
#         else: dir = config.inputDirs['workspace'].get()
#         dir = (askopendirname(initialdir = dir,title= 'grav',foldercreation = FALSE))
#         config.inputDirs['gravity'].set(dir)
#          
#     elif config.item == 'tle':
#          
#         if len(config.inputDirs['gravity'].get())>0: dir = config.inputDirs['gravity'].get()
#         elif len(config.inputDirs['tle'].get())>0: dir = config.inputDirs['tle'].get() 
#         else: dir = config.inputDirs['workspace'].get()
#         dir = (askopendirname(initialdir = dir,title= 'tle',foldercreation = FALSE))
#         config.inputDirs['tle'].set(dir)

def browse_button1(dir = '/home/'):
    if len(config.inputDirs['workspace'].get())>0: dir = config.inputDirs['workspace'].get() 
    elif len(config.inputDirs['rinex'].get())>0: dir = config.inputDirs['rinex'].get() 
    else:dir = config.inputDirs['workspace'].get()
    dir = (askopendirname(initialdir = dir,title= 'rinex',foldercreation = FALSE))
    config.inputDirs['rinex'].set(dir)
      
def browse_button2(dir = '/home/'):
    if len(config.inputDirs['rinex'].get())>0: dir = config.inputDirs['rinex'].get() 
    elif len(config.inputDirs['brdc'].get())>0: dir = config.inputDirs['brdc'].get() 
    else:dir = config.inputDirs['workspace'].get()
    dir = (askopendirname(initialdir = dir,title= 'brdc',foldercreation = FALSE))
    config.inputDirs['brdc'].set(dir)
  
def browse_button3(dir = '/home/'):
    if len(config.inputDirs['brdc'].get())>0: dir = config.inputDirs['brdc'].get() 
    elif len(config.inputDirs['peph'].get())>0: dir = config.inputDirs['peph'].get() 
    else:dir = config.inputDirs['workspace'].get()
    dir = (askopendirname(initialdir = dir,title= 'peph',foldercreation = FALSE))
    config.inputDirs['peph'].set(dir)
      
def browse_button4(dir = '/home/'):
    if len(config.inputDirs['peph'].get())>0: dir = config.inputDirs['peph'].get() 
    elif len(config.inputDirs['jpl'].get())>0: dir = config.inputDirs['jpl'].get() 
    else: dir = config.inputDirs['workspace'].get()
    dir = (askopendirname(initialdir = dir,title= 'jpl',foldercreation = FALSE))
    config.inputDirs['jpl'].set(dir)
  
def browse_button5(dir = '/home/'):
    if len(config.inputDirs['jpl'].get())>0: dir = config.inputDirs['jpl'].get()
    elif len(config.inputDirs['eop'].get())>0: dir = config.inputDirs['eop'].get() 
    else: dir = config.inputDirs['workspace'].get()
    dir = (askopendirname(initialdir = dir,title= 'eop',foldercreation = FALSE))
    config.inputDirs['eop'].set(dir)
  
def browse_button6(dir = '/home/'):
    if len(config.inputDirs['eop'].get())>0: dir = config.inputDirs['eop'].get()
    elif len(config.inputDirs['almanac'].get())>0: dir = config.inputDirs['almanac'].get() 
    else: dir = config.inputDirs['workspace'].get()
    dir = (askopendirname(initialdir = dir,title= 'almanac',foldercreation = FALSE))
    config.inputDirs['almanac'].set(dir)
  
def browse_button7(dir = '/home/'):
    if len(config.inputDirs['almanac'].get())>0: dir = config.inputDirs['almanac'].get()
    elif len(config.inputDirs['gravity'].get())>0: dir = config.inputDirs['gravity'].get() 
    else: dir = config.inputDirs['workspace'].get()
    dir = (askopendirname(initialdir = dir,title= 'grav',foldercreation = FALSE))
    config.inputDirs['gravity'].set(dir)
 
def browse_button8(dir = '/home/'):
    if len(config.inputDirs['gravity'].get())>0: dir = config.inputDirs['gravity'].get()
    elif len(config.inputDirs['tle'].get())>0: dir = config.inputDirs['tle'].get() 
    else: dir = config.inputDirs['workspace'].get()
    dir = (askopendirname(initialdir = dir,title= 'tle',foldercreation = FALSE))
    config.inputDirs['tle'].set(dir)

def open_button():
    try:
        dir = config.path2consts
        filepath = askopenfilename(initialdir = config.path2consts,title = "Select file",filetypes = (("configuration files","*.conf"),("all files","*.*")))
    except:
        dir = '/home/'
        filepath = askopenfilename(initialdir = '/home/',title = "Select file",filetypes = (("configuration files","*.conf"),("all files","*.*")))

    if os.path.isfile(filepath):
        os.system('gedit '+filepath)
        config.logs.append(filepath +' is editted')
        config.logs.append('editting '+filepath+' is canceled' )
    else:
        pass