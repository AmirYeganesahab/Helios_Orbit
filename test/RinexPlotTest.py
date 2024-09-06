#!/usr/bin/env python3
from GNSS.Rinex import * 
import numpy as np                   #|
import matplotlib.pyplot as plt
from astropy.time import Time
import time
from matplotlib.ticker import MaxNLocator


InPath = '/home/geomatics/Dropbox/Sample_Data/'       #|
OutPath = '/home/geomatics/Documents/workspace/.I-O/' #|
                                                    #|
FileName = 'cham0140.06o'                           #|
# rnx = Rinex(InPath, OutPath, FileName)              #|
# data = rnx.load() # help(rnx.load)                         #|

def autolabel(rects,*args):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2.0, 1.05*height,
                '%d' % int(rect.get_x()+1),
                ha='center', va='bottom')
       

def rnxHeader(f):
    #Read Header
    requirements = ['RINEX VERSION', 'INTERVAL', 'TIME OF FIRST OBS', 'APPROX POSITION XYZ', 'ANTENNA: DELTA H/E/N', 'TYPES OF OBSERV']

    # Read Until the End of Heading as save the place of cursor
    headerInfo = {}
    
    while True:
        line = f.readline()
        identification = line[60:].strip()
        description = line[:60].strip()
        if identification in requirements:
            headerInfo[identification] = description
            a = requirements.index(identification)
            del requirements[a]
        elif '/' in identification:
            identification_ = identification.strip().split('/')
            if identification_[0].strip() == '#': 
                headerInfo[identification_[1].strip()] = description.strip().split() 
            else:
                for idx, item in enumerate(identification_):
                    if item.strip() in requirements:
                        headerInfo[item.strip()] = description.strip().split()[idx]
                        a = requirements.index(item.strip())
                        del requirements[a]
        if identification == 'END OF HEADER':
            cursor = f.tell()
            break
          
    return headerInfo,cursor

def rnxLoad(f,cursor : int):
    
    f.seek(cursor)
    
    ObsType = headerInfo['TYPES OF OBSERV'][1:]
    if headerInfo['RINEX VERSION'] == '2':
        ObsType.insert(1,'L1_SNR')
        ObsType.insert(3,'L2_SNR')
    # epochInfo
    
    line = f.readline()
    line = line.strip().split()
    epoch = line[:6]
    year = int(epoch[0])
    if int(epoch[0]) < 50: 
        epoch[0] = str(year + 2000)
    else: 
        epoch[0] = str(year + 1900)
    
    _time = ('{0:4}-{1:2}-{2:2}T{3:2}:{4:2}:{5}').format\
            (epoch[0].zfill(4),epoch[1].zfill(2),\
             epoch[2].zfill(2),epoch[3].zfill(2),\
             epoch[4].zfill(2),epoch[5].zfill(2))
    _time = Time(_time)  
    
    epoch_ = [int(e) for e in epoch[:5]]
    epoch_.append(float(epoch[5]))
    
    nObs = int(line[7])
    prns = [int(prn) for prn in line[8:]]
    obs = {}
    for item in ObsType:
        obs[item] = np.zeros(prns.__len__())
    obs['prns'] = prns
    obs['mjd'] = _time.mjd 
    
    for idx0, prn in  enumerate(prns):
        line = f.readline().strip().split()
        for idx1,item in enumerate(ObsType):
            obs[ObsType[idx1]][idx0] = float(line[idx1])
    cursor = f.tell()
    return obs, cursor

path = InPath+FileName
f = open(path,'r')
headerInfo,cursor = rnxHeader(f)

SNRs = ['L1_SNR','L2_SNR']

plt.ion()

fig, ax = plt.subplots()
#ax.xaxis.set_major_locator(MaxNLocator(integer=True))
while True:
    data, cursor = rnxLoad(f,cursor)
    prns = data['prns']
    m = max(prns)

    L1_snr = data['L1_SNR']
    L2_snr = data['L2_SNR']
    
    rects = plt.bar(prns,L1_snr, width = 1)
    autolabel(rects)
    plt.xticks()
    #ax.set_xticks(prns)
    plt.show()
    plt.pause(0.1)
    plt.clf()
    

proj = ["lambert", "aitoff", "hammer", "mollweide"]

plt.figure()
plt.subplot(121, projection = proj[0])
plt.title(proj[0])
plt.grid(True)
plt.subplot(122, projection = proj[1])
plt.title(proj[1])
plt.grid(True)
plt.show()