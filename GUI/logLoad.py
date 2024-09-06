import GUI.config as config
from tkinter import *
import os
def savevariables():
    try:
        config.settings['beginTime']= config.settings['begin']['date'].get()+'-'+config.settings['begin']['hms']
        config.settings['endTime']= config.settings['end']['date'].get()+'-'+config.settings['end']['hms']
    except:
        config.settings['beginTime']= config.settings['begin']['date'].get()+'-'+config.settings['begin']['hms'].get()
        config.settings['endTime']= config.settings['end']['date'].get()+'-'+config.settings['end']['hms'].get()
    # ======================== permanent workspaces ================================
    if config.settings['pws']:
        file0 = config.Mainpath + '/I_O/' + 'PworkSpace.dirs'
        if not os.path.isfile(file0):os.system('echo -n > ' + file0)
        with open(file0, 'w') as fp0:
            fp0.write(config.inputDirs['workspace'].get())
    # ================================== Recent workspaces ==================================
    write = True
    file1 = config.Mainpath + '/I_O/' + 'recent.dirs'
    if not os.path.isfile(file1): os.system('echo -n > ' + file1)
    with open(file1, 'r') as fp0:
        for line in fp0:
            if line == (config.inputDirs['workspace'].get()+'\n'):
                write = False
            else: 
                pass
    fp0.close()
    if write:
        with open(file1, 'a') as fp0:
            fp0.write(config.inputDirs['workspace'].get()+'\n')
        fp0.close()
    # ============================== input dirs of the workspace =============================
    with open(config.inputDirs['workspace'].get()+'/.I-O/'+'ws.dirs', 'w') as fp0:
        for log in config.inputDirs.keys():
            line = log + ' : ' + config.inputDirs[log].get()+'\n'
            fp0.write(line)
    fp0.close()
    # ============================== settings of the workspace =============================
    with open(config.inputDirs['workspace'].get()+'/.I-O/'+'ws.set', 'w') as fp1:
        for log in config.settings.keys():
            if log == 'begin' or log == 'end': continue
            try:
                line = log + ' : ' + (config.settings[log].get())+'\n'
            except:
                try:
                    line = log + ' : ' + str(config.settings[log].get())+'\n'
                except:
                    line = log + ' : ' + str(config.settings[log])+'\n'
            fp1.write(line)
    fp0.close()
    
def loadvariables():
    # ======================== permanent workspaces ================================
    # check the workspace if exists (workspace requirements are ws.dirs and ws.set files)
    # ws.dirs include the directories that input data are located
    # we.set include the preferences of the workspace
    # ws.dirs and we.set are save in workspace/.I_O
    # ======================== permanent workspaces ================================
    file0 = config.Mainpath + '/I_O/' + 'PworkSpace.dirs'
    if os.path.isfile(file0):
        with open(file0 , 'r') as fp0:
            for line in fp0: 
                config.permanentWorkspace = line
                config.inputDirs['workspace'].set(line)
        fp0.close()
        config.logs.append('The permanent workspace has been set to {}\n'.format(config.permanentWorkspace))
    
    if not config.permanentWorkspace == None:
        Bool0 = os.path.isdir(config.permanentWorkspace)
    else:
        Bool0 = 0
    if not config.inputDirs['workspace'].get() == '':
        Bool1 = os.path.isdir(config.inputDirs['workspace'].get()) 
        pathBool1 = os.path.isfile(config.inputDirs['workspace'].get()+'/.I-O/'+'ws.dirs')
        pathBool2 = os.path.isfile(config.inputDirs['workspace'].get()+'/.I-O/'+'ws.set')
    else:
        Bool1 = 0
    pathBool0 = Bool0 or Bool1

    if pathBool0 and pathBool1 and pathBool2:
        config.OntheFly = 'workspace is grabed from {}\n'.format(config.inputDirs['workspace'].get())
    else:
        config.OntheFly = 'workspace is created at {}\n'.format(config.inputDirs['workspace'].get())
    config.logs.append(config.OntheFly)
    # ======================== recent workspaces ===================================
    config.recentWorkspace=['']
    file1 = config.Mainpath + '/I_O/' + 'recent.dirs'
    if os.path.isfile(file1):
        j = 0
        with open(file1, 'r') as fp0:
            for line in fp0:
                j +=1 
                config.recentWorkspace.append(line[:-1])
                config.logs.append('Recent workspace {0:3d}: {1}\n'.format(j,line[:-1]))
        fp0.close()
    # ======================== input dirs of the workspace =========================
    if not config.permanentWorkspace is None:
        config.inputDirs['workspace'].set(config.permanentWorkspace)
        config.logs.append('The workspace has been set to {}\n'.format(config.permanentWorkspace))
         
    path = config.inputDirs['workspace'].get()+'/.I-O/'+'ws.dirs'
    if os.path.isfile(path):
        with open(path, 'r') as fp0:
            for line in fp0: 
                line = str.split(line)
                if len(line) == 2: continue
                config.inputDirs[line[0]].set(line[2])
        config.logs.append('workspace path preferences loaded\n')
        fp0.close()
    # ======================== settings of the workspace ===========================
    path = config.inputDirs['workspace'].get()+'/.I-O/'+'ws.set'
    if os.path.isfile(path):
        with open(path, 'r') as fp1:
            for line in fp1: 
                line = str.split(line)
                if len(line) == 2: continue
                config.settings[line[0]].set(line[2])
        config.logs.append('workspace settings preferences loaded\n')
        fp1.close()
    # ======================== Time set ============================================
    DateTime = config.settings['beginTime'].get()
    config.settings['begin']['date'].set(DateTime[0:10])
    config.settings['begin']['hms'].set(DateTime[11:])
    DateTime = config.settings['endTime'].get()
    config.settings['end']['date'].set(DateTime[0:10])
    config.settings['end']['hms'].set(DateTime[11:])
    
def log(projectroot,logs):
    
    logfilename = projectroot+'/.I-O/logs/log' + str( config.currentDT ) + '.txt'
    print (logfilename)
    f = open( logfilename,"w+" )
    for log in (logs):
        f.write(log)
    logs = []
    f.close()
    
def ReadDefaults(conf,dest_root):
    # Reads the default preferences of the program.
    # can be changed in the third page of the settings or
    # from the .Constants/DefaultsValues.conf
    # The format of the configuration file is discribed in Defaultvalues.conf
    
    config.DefaultValues = {'help':[conf]}
    with open(dest_root, 'r') as f:
        dict = {}
        dictHelp = {}
        config.logs.append('Workspace preferences are :\n')
        for line in f:
            # ============================= Comments          ====================   
            if line[0] =="'": 
                pass          # comment
            # ============================= Primary keys      ==================== 
            elif line[0] == '!': 
                config.logs.append(line)
                key = line.split()[1]
                dict[key] = {}
            # ============================= Discription       ====================
            elif line[0] == '$': pass
            # ============================= Secondary keys    ====================
            elif line[0] == '#':
                config.logs.append(line)
                subkey = line.split()[1]
                dict[key][subkey] = {}
            # ============================= Preference Values ====================
            else:
                config.logs.append(line)
                print(line)
                vs = eval(line.split()[2])
                id = line.split()[0]
                d={}
                if isinstance(vs, list):
                    dict[key][subkey][id] = []
                    for i,v in enumerate(vs):
                        dict[key][subkey][id].append(DoubleVar(config.master))
                        dict[key][subkey][id][i].set(v)
                else:
                  dict[key][subkey][id] = DoubleVar(config.master)
                  dict[key][subkey][id].set(vs)  
    return dict
    
def overWriteDefaults():
    # Header
    H = []
    H.append("' [!]=> key 1                     |")
    H.append("' [!]=> key 1                     |")
    H.append("' [#]=> sub key                   |")
    H.append("' [$]=> Discription of upper line |")
    H.append("' [']=> comment                   |")
    H.append("' [no prefixes]=> variable'       |")
    Header = ''
    for h in H:
        if Header == '': Header = h
        else:
            Header = Header + '\n' + h
    Header = Header + '\n'
    with open(config.inputDirs['workspace'].get()+ '/.Constants/DefaultValues.conf', 'w') as f:
        f.write(Header)         
        for key1 in config.DefaultValues.keys():
            f.write("' =======================================\n")
            f.write( '! ' + key1 + '\n' )
            for key2 in config.DefaultValues[key1].keys():
                f.write( '# ' + key2 + '\n' )
                for id in config.DefaultValues[key1][key2].keys():
                    if isinstance(config.DefaultValues[key1][key2][id], list):
                        l='['
                        for i,v in enumerate(config.DefaultValues[key1][key2][id]):
                            l = l + str(v.get())
                            if i < len(config.DefaultValues[key1][key2][id])-1: 
                                l = l +','
                            else:
                                l = l +']'
                        f.write( id+ ' : ' + l + '\n' )
                    else:
                        f.write( id+ ' : ' + str(config.DefaultValues[key1][key2][id].get()) + '\n')
    f.close()
    config.logs.append('Default Preferences are updated_ Altered if change applied\n')