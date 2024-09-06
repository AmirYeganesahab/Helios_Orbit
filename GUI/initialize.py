from tkinter import *
import GUI.config as config

def initialize_inputDirs(master):
    def pathdict(master):
        inputDirs={}
        for path in config.pathes:
            inputDirs[path] = StringVar(master)
        return inputDirs
#     inputDirs = pathdict()
    return pathdict(master)

def initialize_settings(master):
        return {'begin' : {'date':StringVar(master),'hms':StringVar(master)},\
                'end' : {'date':StringVar(master),'hms':StringVar(master)},\
                'endTime' : StringVar(master),\
                'beginTime' : StringVar(master),\
                'Adaptive' : BooleanVar(master),\
                'smoothing_bwd' : IntVar(master),\
                'Robust' : IntVar(master),\
                'smoothing_fwd' : IntVar(master),\
                'Filter_Type' : StringVar(master),\
                'Observation_Type' : StringVar(master),\
                'Dynamic_mode' : StringVar(master),\
                'DataEditingMode' : StringVar(master),\
                'enableSaveFilterOutput' : IntVar(master),\
                'figure': IntVar(master),\
                'pws':IntVar(master)}

