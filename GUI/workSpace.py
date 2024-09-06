import GUI.config as config 
from GUI.logLoad import *
import os
from shutil import copyfile as cp
from GUI.settingsWindow import *
import numpy as np
                     
def WorkSpace():
    folderwin = Toplevel(config.master)
    folderwin.geometry("800x300")
    folderwin.resizable(False, False)
    # =================== Frame 1 =================== 
    f1 = Frame(folderwin,bg = 'antique white')
    f1.grid(row = 0, columnspan =4 ,sticky = 'ew')
    
    l1 = Label(f1, text = 'Select a directory as workspace', font = 'Helvetica 12 bold',\
               bg = 'antique white', width = 100, height = 2,  anchor="w")
    l1.grid(row = 0, columnspan = 4)
    
    l2 = Label(f1, text = '  OTK uses the workspace to store its preferences and settings',\
               font = ' Helvetica 11', bg = 'antique white', width = 100,  height = 2, anchor="w")
    l2.grid(row = 1, columnspan = 4)
    # =================== Frame 2 =================== 
    f2 = Frame(folderwin, height = 5)
    f2.grid(row = 1, columnspan =4 ,sticky = 'ew')

    f22 = Frame(f2, height = 5)
    f22.grid(row = 1, columnspan =4 ,sticky = 'ew')

    l0 = Label(f22, text = ' ', width = 50, height = 2)
    l0.grid(row = 0,columnspan =4)
    
    f23 = Frame(f2, height = 5)
    f23.grid(row = 2, columnspan =4 ,sticky = 'ew')
    
    l1 = Label(f23, text = 'Workspace: ', height = 2, anchor="w")
    l1.grid(row = 1)
    type = config.recentWorkspace
    popupMenu = OptionMenu(f23, config.inputDirs['workspace'], *type)
    #entry1 = Entry(f23,textvariable = config.inputDirs['workspace'], width = 70)#, height = 2)        
    popupMenu.grid(row = 1, column = 1, columnspan = 3)
    popupMenu.config(width = 70, bg='white', anchor = 'w')
    
    button1 = Button(f23,text="    Browse    ", command= browse_button_ws)
    button1.grid(row  = 1, column = 4)
    # =================== Frame 3 ===================
    f3 = Frame(folderwin)
    f3.grid(row = 2, columnspan =4 ,sticky = 'w')
    
    l1 = Label(f3, text = ' ', width = 70, height = 3)
    l1.grid(row = 0)
    
    chkbx = Checkbutton(f3, text="Use this as the default and do not ask again",variable = config.settings['pws'] , height = 1)
    chkbx.grid(row=0, column = 0, columnspan = 3, sticky='ws')
    
    if config.settings['pws'].get():
        config.PermanentWS = config.inputDirs['workspace'].get()
        print(config.PermanentWS)
    # =================== Frame 4 ===================
    f3 = Frame(folderwin)
    f3.grid(row = 3, columnspan =4 ,sticky = 'ew')
    
    f4 = Frame(f3, width = 70)
    f4.grid(row = 0, columnspan =3 ,sticky = 'ew')
    
    l1 = Label(f4, text = ' ', width = 70, height = 5)
    l1.grid(row = 0)
    
    f5 = Frame(f3, width = 20)
    f5.grid(row = 0, column = 4, columnspan =1 ,sticky = 'ew')
    
    button2 = Button(f5, text='    Launch    ', command= combine_funcs(generateWorkspace,settings, folderwin.destroy))
    button2.grid(row = 0,column = 4, sticky = 'ew')
    
    button3 = Button(f5, text='    Cancel    ', command= combine_funcs(folderwin.destroy,config.master.destroy ))
    button3.grid(row = 0, column = 3,sticky = 'ew')
#     
#     
#     print (config.settings['pws'].get())
#     if config.settings['pws'].get():
#         button2.invoke()
#         settings()

def generateWorkspace():
        path = config.inputDirs['workspace'].get()
        # =================================== Load workspace =============================
#         loadvariables()
        
        # =================================== creating default directories ===============
        config.logs.append('the workspace is set to '+ path  + '\n')
        for dir in ( config.WorkspaceDirs ):
            thispath = path + '/' + dir
            if not os.path.isdir(thispath ): 
                os.mkdir(thispath )
                config.logs.append( dir + ' is created at ' + path  +'\n')
            else:
                config.logs.append( dir + ' exists at ' + path  +'\n')
        # transiting the files of mathe, phys and astro constants in .Constants
        #math constants
        dir_root = os.path.dirname(os.path.realpath(__file__))[:-3]
        dir_root = dir_root + 'Constants/'
        confs = []
        for conf in (config.Configs):
            file_root = dir_root + conf+'.conf'
            config.path2consts = path  +'/.Constants/'
            dest_root = config.path2consts + conf+'.conf'
            confs.append(dest_root)
            if not os.path.isfile(dest_root):
                cp(file_root, dest_root)
                config.logs.append('configuration for '+ conf + ' is set\n')
            else:
                config.logs.append('configuration for '+ conf + ' already exists\n')
            
            config.DefaultValues = {'help':[conf]}
            config.DefaultValues = ReadDefaults(conf,dest_root)
        
        
def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func    
