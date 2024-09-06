import GUI.config as config
from tkinter import *
from tkinter import ttk
from tkinter import simpledialog
import tkcalendar
from GUI.buttons import *
from GUI.logLoad import *

def settings():
    
    def settings1():
        
        settingswin.title("Data Path Settings")       
        #Frames
        ulFrame = Frame(settingswin, highlightbackground="black", highlightcolor="black", highlightthickness=1, width=200, height=100, bd= 0)#create a frame at the top of the panel
        ulFrame.columnconfigure(1, weight=1)
        ulFrame.grid(row = 0, columnspan = 3,sticky = 'snew')
        
        settings_ULFrame(ulFrame )
        
        ulFrame2 = Frame(settingswin,bg = 'antique white', height = 2)#create a frame at the top of the panel
        ulFrame2.columnconfigure(1, weight=1)
        ulFrame2.grid(row = 1, columnspan = 3, sticky = E)
        
        button2 = Button(ulFrame2, text='    Next    ', command=combine_funcs(savevariables,settings2, ulFrame.destroy, ulFrame2.destroy))
        button2.grid(row = 1, column = 2)

        button3 = Button(ulFrame2, text='    Apply    ',\
                          command=combine_funcs(savevariables,\
        config.master.update, config.master.deiconify, settingswin.destroy))
        button3.grid(row = 1, column = 1)
        
        button3 = Button(ulFrame2, text='    Cancel    ', command=combine_funcs(settingswin.destroy))
        button3.grid(row = 1, column = 0)
    
    def settings2 ():
        settingswin.title("Filter Settings")
        urFrame = Frame(settingswin, highlightbackground="black",\
                        highlightcolor="black", highlightthickness=1, width=100, height=100, bd= 0)#create a frame at the top of the panel
        urFrame.columnconfigure(2, weight=1)
        urFrame.grid(row = 0, columnspan = 3, sticky = 'snew')
        
        settings_URFrame(urFrame)
        
        urFrame2 = Frame(settingswin)
        urFrame2.columnconfigure(2, weight=1)
        urFrame2.grid(row = 1, columnspan = 3, sticky = 'e')

        button3 = Button(urFrame2, text='    Next    ', command=combine_funcs(savevariables, settings3, urFrame.destroy, urFrame2.destroy))
        button3.grid(row = 1, column = 3)
        
        button4 = Button(urFrame2, text='    Back    ', command=combine_funcs(savevariables,settings1, urFrame.destroy, urFrame2.destroy))
        button4.grid(row = 1, column = 1)   
        
        button5 = Button(urFrame2, text='    Apply    ',\
                      command=combine_funcs(savevariables,\
        config.master.update,config.master.deiconify, settingswin.destroy))
        button5.grid(row = 1, column = 2)
        
        button5 = Button(urFrame2, text='    Cancel    ', command=combine_funcs(settingswin.destroy))
        button5.grid(row = 1, column = 0)
  
    def settings3 ():
        settingswin.title("Default Variables")
        blFrame = Frame(settingswin, highlightbackground="black", highlightcolor="black", highlightthickness=1, width=100, height=100, bd= 0)#create a frame at the top of the panel
        blFrame.columnconfigure(2, weight=1)
        blFrame.grid(row = 0, columnspan = 3)
        labelwidth = 20
        labelheight = 1
        row = 0
        n = ttk.Notebook(blFrame)
        for i, key1 in enumerate(config.DefaultValues.keys()):
            dict1 = config.DefaultValues[key1]
            f = ttk.Frame(n)   # current page, would get widgets gridded into it
            for j, key2 in enumerate(dict1.keys()):
                dict2 = dict1[key2]
                f1 = Frame(f,highlightbackground="black", highlightcolor="black", highlightthickness=1, width=100, height=100, bd= 0)
                Label(f1, text=key2, font=("Helvetica", 12), width = 50).pack(side='top', pady=4)
                f1.grid(row = j, columnspan = 3, sticky = E+W)
                for k, key3 in enumerate(dict2.keys()):
                    row += 1
                    f2 = Frame(f1)
                    f2.pack()
                    lbl = Label(f2,width = labelwidth, height = labelheight,text = key3, borderwidth=1,relief="groove")
                    lbl.pack(side = LEFT)
                    if isinstance(dict2[key3], list):
                        for i,e in enumerate(dict2[key3]):
                            entry1 = Entry(f2,width = int(labelwidth/3),textvariable = e)
                            entry1.pack(side = RIGHT)
                    else:
                        entry1 = Entry(f2,width = labelwidth,textvariable = dict2[key3])
                        entry1.pack(side = RIGHT)
            n.add(f, text=key1)
        n.grid(row=0, sticky = 'snew')
        
        blFrame2 = Frame(settingswin)#create a frame at the top of the panel
        blFrame2.columnconfigure(2, weight=1)
        blFrame2.grid(row = 1, columnspan = 3, sticky = 'e')
        
        button3 = Button(blFrame2, text='    Apply    ',\
                          command=combine_funcs(overWriteDefaults,\
         savevariables, config.master.update, config.master.deiconify,settingswin.destroy))
        #         root.update()
#         root.deiconify()
        button3.grid(row = 1, column = 2, sticky = E) 
        
        button4 = Button(blFrame2, text='    Back    ', command=combine_funcs(overWriteDefaults, savevariables, settings2, blFrame.destroy, blFrame2.destroy))
        button4.grid(row = 1, column = 1, sticky = E)   
        
        button5 = Button(blFrame2, text='    Cancel    ', command=combine_funcs(settingswin.destroy))
        button5.grid(row = 1, column = 0, sticky = E) 

    settingswin = Toplevel(config.master)
    settingswin.resizable(False, False)
    settings1()
    
def settings_BLFrame(master):
    labelwidth = 13
    labelheight = 1
    # ============================= initial values  =============================
    row = -1
    rc = 0
    for i, key1 in enumerate(config.DefaultValues.keys()):
        row += 2
        dict1 = config.DefaultValues[key1]
         
        lbl = Label(master,text = key1, borderwidth=2,relief="groove")
        lbl.grid(row = row, column = 0, sticky = W+E)
        
        for j, key2 in enumerate(dict1.keys()):
#             row = row + 3*j
            dict2 = dict1[key2]           

            for k, key3 in enumerate(dict2.keys()):

                lbl = Label(master,width = labelwidth, height = labelheight,text = key3, borderwidth=1,relief="groove")
                lbl.grid(row = row, column = k+j+1, sticky = W+E)
                
                entry1 = Entry(master,width = labelwidth,textvariable = dict2[key3])
                entry1.grid(row = row+1, column = k+j+1, columnspan = 1, sticky = 'ew')

    lbl2 = Label(master,width = labelwidth, height = labelheight,text='Dynamic Forces',borderwidth=2,relief="groove")
    lbl2.grid(row = 0, column = 0, sticky = W+E)

def settings_URFrame(master):
    
    def onclick1():
        config.settings['begin']['date'].set(CalendarDialog(master).result)
    def onclick2():
        config.settings['end']['date'].set(CalendarDialog(master).result)
# ================================= Process Period =====================================
    urFrame2 = Frame(master, highlightbackground="black", highlightcolor="black")
    urFrame2.grid(row = 0, columnspan = 4, sticky = 'snew')
    
    lbl1 = Label(urFrame2,text='Process period',borderwidth=2,height = 2, relief="groove", width = 70, bg = 'antique white')
    lbl1.grid(row = 0, columnspan = 5, sticky = W+E)
    
    lbl2 = Label(urFrame2,text='Date',borderwidth=2,relief="groove")
    lbl2.grid(row = 1, column = 0, sticky = W+E)
        
    button1 = Button(urFrame2,text="Begin", width = 8, command=onclick1)
    button1.grid(row = 1, column = 2, sticky = 'n')
    lbl3 = Label(urFrame2,textvariable=config.settings['begin']['date'], borderwidth=2,relief="groove")
    lbl3.grid(row = 1, column = 1, sticky = W+E)

    button2 = Button(urFrame2,text="end", width = 8, command=onclick2)
    button2.grid(row = 1, column = 4, sticky = 'n')
    lbl4 = Label(urFrame2,textvariable=config.settings['end']['date'] ,borderwidth=2,relief="groove")
    lbl4.grid(row = 1, column = 3, sticky = W+E)
    # enter time
    lbl5 = Label(urFrame2,text='Time',borderwidth=2,relief="groove")
    lbl5.grid(row = 2, column = 0, sticky = W+E)
    
    entry1 = Entry(urFrame2,textvariable=config.settings['begin']['hms'])
    entry1.grid(row = 2, column = 1)#, sticky = 'ew')
    if len(config.settings['begin']['hms'].get())==0 : config.settings['begin']['hms'].set('00:00:00')
    
    entry2 = Entry(urFrame2,textvariable=config.settings['end']['hms'])
    entry2.grid(row = 2, column = 3)#, sticky = 'ew')
    if len(config.settings['end']['hms'].get())==0 : config.settings['end']['hms'].set('24:00:00')
    
#     lbl50 = Label(master,text='', width = 1 , height = 1 , borderwidth = 2)
#     lbl50.grid(row = 1, columnspan = 4, sticky = W+E)
    # ================================= DropDown menues =====================================
    urFrame3 = Frame(master, highlightbackground="black",  highlightcolor="black")
    urFrame3.grid(row = 2, columnspan = 4, sticky = 'snew')
    
    lbl1 = Label(urFrame3,text='Filter Settings',borderwidth=2,height = 2 ,relief="groove", width = 70, bg = 'antique white')
    lbl1.grid(row = 0, columnspan = 5, sticky = W+E)
    #Filter Type       
    (dropDown(config.filteType, urFrame3, label = 'Filter_Type', row = 1))
    #Observation Type
    (dropDown(config.obsType, urFrame3, label = 'Observation_Type', row = 2))
    #Dynamic mode
    (dropDown(config.dynamicMod, urFrame3, label = 'Dynamic_mode', row = 3))
    
    lbl51 = Label(master,text='', width = 1 , height = 1 , borderwidth = 2)
    lbl51.grid(row = 3, columnspan = 4, sticky = W+E)
    # =========================================================================================
    urFrame5 = Frame(master, highlightbackground="black", highlightcolor="black")
    urFrame5.grid(row = 4, columnspan = 4, sticky = 'snew')
    
    config.master2 = master
    config.frame = urFrame5
    
#     if config.settings['DataEditingMode'].get() == 'Recursive_Outlier_Detection':
#         command = 'ROD'
#     elif config.settings['DataEditingMode'].get() == 'Outlier_Detection_for_RUKF':
#         command = 'RUKFOD'
#     elif config.settings['DataEditingMode'].get() == 'Adaptive_Robust':
#         command = 'AR'
#     else:
#         command = None
    # Data editing mode
    (dropDown(config.dataeditingmode, urFrame3, label = 'DataEditingMode', row = 4))

    lbl1 = Label(urFrame5,text='Data Editting Mode Settings',borderwidth=2,height = 2 ,relief="groove", width = 70, bg = 'antique white')
    lbl1.grid(row = 0, columnspan = 5, sticky = W+E)
    urFrame5.destroy()
    # ================================= Check Buttons ================================================
    lbl51 = Label(master,text='', width = 1 , height = 1 , borderwidth = 2)                     #    |
    lbl51.grid(row = 5, columnspan = 4, sticky = W+E)                                           #    |
    # =================================                                                         #    |
    urFrame4 = Frame(master, highlightbackground="black", highlightcolor="black")               #    |
    urFrame4.grid(row = 6, columnspan = 4, sticky = 'snew')                                     #    |
                                                                                                #    |
    urFrame41 = Frame(urFrame4, highlightbackground="black", highlightcolor="black")            #    |
    urFrame41.grid(row = 0, column = 0, columnspan = 1, sticky = 'snew')                        #    |
    #Adaptive? (checkbox)                                                                       #    |
    chkbx1 = Checkbutton(urFrame41, text="Adaptive Process", variable=config.settings['Adaptive'])#  |
    chkbx1.grid(row=0, column = 0, columnspan = 1, sticky=W)                                    #    |
    #Robust? (checkbox)                                                                         #    |
    chkbx2 = Checkbutton(urFrame41, text="Robust Process", variable=config.settings['Robust'])  #    |
    chkbx2.grid(row=1, column = 0, sticky=W)                                                    #    |
    # =================================                                                         #    |
    urFrame42 = Frame(urFrame4, highlightbackground="black", highlightcolor="black")            #    |
    urFrame42.grid(row = 0, column = 1, sticky = 'snew')                                        #    |
    #Smooting? (checkbox)                                                                       #    |
    chkbx3 = Checkbutton(urFrame42, text="Process with backward smoothing", variable=config.settings['smoothing_bwd'])
    chkbx3.grid(row=0, column = 0, columnspan = 1, sticky=W)                                    #    |
    #Smooting? (checkbox)                                                                       #    |
    chkbx0 = Checkbutton(urFrame42, text="Process with ...", variable=config.settings['smoothing_fwd'])
    chkbx0.grid(row = 1, column = 0, columnspan = 1, sticky=W)                                  #    |
    # =================================                                                         #    |
    urFrame43 = Frame(urFrame4, highlightbackground="black", highlightcolor="black")            #    |
    urFrame43.grid(row = 0, column = 2, columnspan = 1, sticky = 'snew')                        #    |
    # Enable Filter Output Save (checkbox)                                                      #    |
    chkbx4 = Checkbutton(urFrame43, text="Save Filter Output", variable=config.settings['enableSaveFilterOutput'])
    chkbx4.grid(row=0, column = 0, columnspan = 1, sticky=W)                                    #    |
    chkbx5 = Checkbutton(urFrame43, text="Show graphics", variable=config.settings['figure'])   #    |
    chkbx5.grid(row=1, column = 0, columnspan = 1, sticky=W)                                    #    |
    # =================================                                                         #    |
    lbl51 = Label(master,text='', width = 1 , height = 1 , borderwidth = 2)                     #    |
    lbl51.grid(row = 7, columnspan = 4, sticky = W+E)                                           #    |
       
def dropDown(type, master,label, row, column = 1, command = None):
    # Create a Tkinter variable
    if len(str(config.settings[label].get()))==0: 
        config.settings[label].set(type[0])  
    
    if config.settings[label].get() == 'Recursive_Outlier_Detection':
        command = 'ROD'
    elif config.settings[label].get() == 'Outlier_Detection_for_RUKF':
        command = 'RUKFOD'
    elif config.settings[label].get() == 'Adaptive_Robust':
        command = 'AR'
    else:
        command = None
        
        
    if command is None:
            popupMenu = OptionMenu(master, config.settings[label], *type)
    else:
        popupMenu = OptionMenu(master, config.settings[label], *type, command = eval(command))
    Label(master, text=label, borderwidth=2,relief="groove").grid(row = row, column = 0,sticky = W+E)
    popupMenu.grid(row = row, column = column, columnspan = 3, sticky = W+E)
    popupMenu.config(width = 50, bg='white', anchor = 'e')
    # on change dropdown value
    def change_dropdown(*args):
        print( config.settings[label].get() )
    # link function to change dropdown
    config.settings[label].trace('w', change_dropdown)

class CalendarDialog(simpledialog.Dialog):
    """Dialog box that displays a calendar and returns the selected date"""
    def body(self, master):
        try:
            date =  config.settings['begin']['date']
            year = date[0:4]
            month = date[4:6]
            day = date[6:8]
        except:
            year = 2019
            month = 1
            day = 1
        self.calendar = tkcalendar.Calendar(master, year=year, month=month, day=month)
        self.calendar.pack()

    def apply(self):
        self.result = self.calendar.selection_get()

def settings_ULFrame(master):
    txts = {}
    for item in config.pathes:
        txts[item] = 'select directory of {}'.format(item)
    
#     def Browse(master, item, txt, Frow, row = 0, column = 2, Fwidth = 80, Fheight = 100, Bwidth = 8):
#         f[item] = Frame( master ,\
#                    highlightthickness = 1 , width = Fwidth , height = Fheight , bd = 0 )
#         f[item].grid( row = Frow, columnspan = 2 )        
#         
#         lbl = Label( f[item] , text = txt , width = Fwidth , borderwidth = 2 , relief = "groove" )
#         lbl.grid(row = 0 , columnspan = 2 , sticky = W+E)
#         
#         button1.grid( f[item] , text = "Browse" , width = 8 , command = browse_button1 )
#         button.grid( row = 1 , column = column , sticky = 'n' )
#         
#         entry = Entry( f[item] , textvariable = config.inputDirs[item] )        
#         entry.grid( row = 1 , columnspan = 2 , sticky = 'ew' )
#         entry.columnconfigure( 1 , weight = 1 )
#         entries.append((item, entry))

#     entries = []
#     for i, item in enumerate(config.pathes):
#         Browse(master = master, item = item, txt = txts[item], Frow = i+1)
    # ============================= Button for changing the global constants =============================
    f0 = Frame(master, highlightbackground="black", highlightcolor="black", highlightthickness=1, width=80, height=100, bd= 0)
    f0.grid(row = 0, columnspan = 2)
    lbl1 = Label(f0,text='Change Constants',borderwidth=2,width = 80, relief="groove", bg = 'antique white')
    lbl1.grid(row = 0,columnspan = 2, sticky = W+E)

    button1 = Button(f0,text="    Open    ", command= open_button)
    button1.grid(row = 0,column = 2, sticky = 'n')
    # ============================= Button for changing the global constants =============================
    # '''''''' rinex ''''''''  
    row = 1;column = 2; Fwidth = 80; Fheight = 100; Bwidth = 8; Frow = 0
    Frow += 1; config.item = 'rinex'
    f1 = Frame( master ,\
               highlightthickness = 1 , width = Fwidth , height = Fheight , bd = 0 )
    f1.grid( row = Frow, columnspan = 2 )        
#     text = txts['rinex']
    lbl1 = Label( f1 , text = ['rinex'] , width = Fwidth , borderwidth = 2 , relief = "groove" )
    lbl1.grid(row = row - 1 , columnspan = 2 , sticky = W+E)
    
    button1 = Button( f1 , text = "Browse" , width = 8 , command = browse_button1 )
    button1.grid( row = row , column = column , sticky = 'n' )
    
    entry1 = Entry( f1 , textvariable = config.inputDirs['rinex'] )        
    entry1.grid( row = row , columnspan = 2 , sticky = 'ew' )
    entry1.columnconfigure( 1 , weight = 1 )
    # '''''''' brdc ''''''''  
    Frow += 1; config.item = 'brdc'
    row += 1
    f2 = Frame( master ,\
               highlightthickness = 1 , width = Fwidth , height = Fheight , bd = 0 )
    f2.grid( row = Frow, columnspan = 2 )        
    
    lbl2 = Label( f2 , text = ['brdc'] , width = Fwidth , borderwidth = 2 , relief = "groove" )
    lbl2.grid(row = row - 1 , columnspan = 2 , sticky = W+E)
    
    button2 = Button( f2 , text = "Browse" , width = 8 , command = browse_button2 )
    button2.grid( row = row , column = column , sticky = 'n' )
    
    entry2 = Entry( f2 , textvariable = config.inputDirs['brdc'] )        
    entry2.grid( row = row , columnspan = 2 , sticky = 'ew' )
    entry2.columnconfigure( 1 , weight = 1 )
    # '''''''' peph ''''''''  
    Frow += 1; config.item = 'peph'
    row += 1
    f3 = Frame( master ,\
               highlightthickness = 1 , width = Fwidth , height = Fheight , bd = 0 )
    f3.grid( row = Frow, columnspan = 2 )        
    
    lbl3 = Label( f3 , text = ['peph'] , width = Fwidth , borderwidth = 2 , relief = "groove" )
    lbl3.grid(row = row - 1 , columnspan = 2 , sticky = W+E)
    
    button3 = Button( f3 , text = "Browse" , width = 8 , command = browse_button3 )
    button3.grid( row = row , column = column , sticky = 'n' )
    
    entry3 = Entry( f3 , textvariable = config.inputDirs['peph'] )        
    entry3.grid( row = row , columnspan = 2 , sticky = 'ew' )
    entry3.columnconfigure( 1 , weight = 1 )
    # '''''''' jpl ''''''''  
    Frow += 1; config.item = 'jpl'
    row += 1
    f4 = Frame( master ,\
               highlightthickness = 1 , width = Fwidth , height = Fheight , bd = 0 )
    f4.grid( row = Frow, columnspan = 2 )        
    
    lbl4 = Label( f4 , text = ['jpl'] , width = Fwidth , borderwidth = 2 , relief = "groove" )
    lbl4.grid(row = row - 1 , columnspan = 2 , sticky = W+E)
    
    button4 = Button( f4 , text = "Browse" , width = 8 , command = browse_button4 )
    button4.grid( row = row , column = column , sticky = 'n' )
    
    entry4 = Entry( f4 , textvariable = config.inputDirs['jpl'] )        
    entry4.grid( row = row , columnspan = 2 , sticky = 'ew' )
    entry4.columnconfigure( 1 , weight = 1 )
    # '''''''' eop ''''''''  
    Frow += 1; config.item = 'eop'
    row += 1
    f5 = Frame( master ,\
               highlightthickness = 1 , width = Fwidth , height = Fheight , bd = 0 )
    f5.grid( row = Frow, columnspan = 2 )        
    
    lbl5 = Label( f5 , text = ['eop'] , width = Fwidth , borderwidth = 2 , relief = "groove" )
    lbl5.grid(row = row - 1 , columnspan = 2 , sticky = W+E)
    
    button5 = Button( f5 , text = "Browse" , width = 8 , command = browse_button5 )
    button5.grid( row = row , column = column , sticky = 'n' )
    
    entry5 = Entry( f5 , textvariable = config.inputDirs['eop'] )        
    entry5.grid( row = row , columnspan = 2 , sticky = 'ew' )
    entry5.columnconfigure( 1 , weight = 1 )
    # '''''''' almanac ''''''''  
    Frow += 1; config.item = 'almanac'
    row += 1
    f6 = Frame( master ,\
               highlightthickness = 1 , width = Fwidth , height = Fheight , bd = 0 )
    f6.grid( row = Frow, columnspan = 2 )        
    
    lbl6 = Label( f6 , text = ['almanac'] , width = Fwidth , borderwidth = 2 , relief = "groove" )
    lbl6.grid(row = row - 1 , columnspan = 2 , sticky = W+E)
    
    button6 = Button( f6 , text = "Browse" , width = 8 , command = browse_button6 )
    button6.grid( row = row , column = column , sticky = 'n' )
    
    entry6 = Entry( f6 , textvariable = config.inputDirs['almanac'] )        
    entry6.grid( row = row , columnspan = 2 , sticky = 'ew' )
    entry6.columnconfigure( 1 , weight = 1 )
    # '''''''' gravity ''''''''  
    Frow += 1; config.item = 'gravity'
    row += 1
    f7 = Frame( master ,\
               highlightthickness = 1 , width = Fwidth , height = Fheight , bd = 0 )
    f7.grid( row = Frow, columnspan = 2 )        
    
    lbl7 = Label( f7 , text = ['gravity'] , width = Fwidth , borderwidth = 2 , relief = "groove" )
    lbl7.grid(row = row - 1 , columnspan = 2 , sticky = W+E)
    
    button7 = Button( f7 , text = "Browse" , width = 8 , command = browse_button7 )
    button7.grid( row = row , column = column , sticky = 'n' )
    
    entry7 = Entry( f7 , textvariable = config.inputDirs['gravity'] )        
    entry7.grid( row = row , columnspan = 2 , sticky = 'ew' )
    entry7.columnconfigure( 1 , weight = 1 )
    # '''''''' tle ''''''''  
    Frow += 1; config.item = 'tle'
    row += 1
    f7 = Frame( master ,\
               highlightthickness = 1 , width = Fwidth , height = Fheight , bd = 0 )
    f7.grid( row = Frow, columnspan = 2 )        
    
    lbl7 = Label( f7 , text = ['tle'] , width = Fwidth , borderwidth = 2 , relief = "groove" )
    lbl7.grid(row = row - 1 , columnspan = 2 , sticky = W+E)
    
    button7 = Button( f7 , text = "Browse" , width = 8 , command = browse_button8 )
    button7.grid( row = row , column = column , sticky = 'n' )
    
    entry7 = Entry( f7 , textvariable = config.inputDirs['tle'] )        
    entry7.grid( row = row , columnspan = 2 , sticky = 'ew' )
    entry7.columnconfigure( 1 , weight = 1 )

    
def combine_funcs(*funcs):
        def combined_func(*args, **kwargs):
            for f in funcs:
                f(*args, **kwargs)
        return combined_func
    
    
def ROD(*args):# recursive Outlier detection
    master = config.master2
    urFrame5 = config.frame
    urFrame5.destroy()
    
    urFrame5 = Frame(master, highlightbackground="black", highlightcolor="black")
    urFrame5.grid(row = 4, columnspan = 4, sticky = 'snew')

    config.settings['Adaptive'] .set( False )
    lbl6 = Label(urFrame5,text='outlierFactor',borderwidth=2,relief="groove")
    lbl6.grid(row = 7, column = 0, sticky = W+E)

    entry6 = Entry(urFrame5,textvariable=config.DefaultValues['dataEditing']['set']['outlierFactor'])
    entry6.grid(row = 7, column = 1, columnspan = 1, sticky = 'ew')
    
    lbl7 = Label(urFrame5,text='AmbBiasFactor',borderwidth=2,relief="groove")
    lbl7.grid(row = 7, column = 2, sticky = W+E)

    entry7 = Entry(urFrame5,textvariable=config.DefaultValues['dataEditing']['set']['AmbBiasFactor'])
    entry7.grid(row = 7, column = 3, columnspan = 1, sticky = 'ew')
    
    lbl8 = Label(urFrame5,text='elevationThreshold',borderwidth=2,relief="groove")
    lbl8.grid(row = 8, column = 0, sticky = W+E)

    entry8 = Entry(urFrame5,textvariable=config.DefaultValues['dataEditing']['set']['elevationThreshold'])
    entry8.grid(row = 8, column = 1, columnspan = 1, sticky = 'ew')
    
    lbl8 = Label(urFrame5,text='Adaptivity',borderwidth=2,relief="groove")
    lbl8.grid(row = 8, column = 2, sticky = W+E)
    
    lbl9 = Label(urFrame5,text=config.settings['Adaptive'].get(),borderwidth=2,relief="groove")
    lbl9.grid(row = 8, column = 3, sticky = W+E)

def RUKFOD(*args):# Outlier detection fro RUKF
    master = config.master2
    urFrame5 = config.frame
    urFrame5.destroy()
    urFrame5 = Frame(master, highlightbackground="black", highlightcolor="black")
    urFrame5.grid(row = 4, columnspan = 4, sticky = 'snew')
    
    lbl6 = Label(urFrame5,text='chiSquare.los',borderwidth=2,relief="groove")
    lbl6.grid(row = 7, column = 0, sticky = W+E)

    entry6 = Entry(urFrame5,textvariable=config.DefaultValues['dataEditing']['set']['chiSquareLos'])
    entry6.grid(row = 7, column = 1, columnspan = 1, sticky = 'ew')
    
    lbl8 = Label(urFrame5,text='Adaptivity',borderwidth=2,relief="groove")
    lbl8.grid(row = 7, column = 2, sticky = W+E)
    config.settings['Adaptive'] .set( False )
    lbl9 = Label(urFrame5,text=config.settings['Adaptive'].get(),borderwidth=2,relief="groove")
    lbl9.grid(row = 7, column = 3, sticky = W+E)
    
def AR(*args):# Adaptive Robust
    master = config.master2
    urFrame5 = config.frame
    urFrame5.destroy()
    urFrame5 = Frame(master, highlightbackground="black", highlightcolor="black")
    urFrame5.grid(row = 4, columnspan = 4, sticky = 'snew')

    
    lbl10 = Label(urFrame5,text='Adaptivity_Adaptive Robust',borderwidth=2,relief="groove")
    lbl10.grid(row = 8, column = 0, sticky = W+E)
    config.settings['Adaptive'] .set( 'True' )
    lbl10 = Label(urFrame5,text=config.settings['Adaptive'].get(),borderwidth=2,relief="groove")
    lbl10.grid(row = 8, column = 1, sticky = W+E)
    
