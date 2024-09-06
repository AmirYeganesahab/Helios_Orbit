'''
Created on Feb 12, 2019

@author: gravity
'''
import math
import numpy as np
from xml.dom import IndexSizeErr
from _datetime import datetime
import time
import sqlite3
import os
import pandas as pd
from astropy.time import Time
class Rinex():
    '''
    Object of Rinex Data
    Attributes are the Heading of the Rinex
    # ====================== Test ====================================
    Copy the following lines and paste them in your scrip. 
    change the file adresses and File Name.
    Then run the code
    #=======================================================#|
        from GNSS.Rinex_h5panda import *                    #|
        InPath = '/home/gravity/Dropbox/Sample_Data/'       #|
        OutPath = '/home/gravity/Documents/workspace/.I-O/' #|
                                                            #|
        FileName = 'cham0140.06o'                           #|
        rnx = Rinex(InPath, OutPath, FileName)              #|
        rnx.load() # help(rnx.load)                         #|
    #=======================================================#|

    '''

    def __init__(self, InPath, OutPath, FileName):
        '''
        Constructor
        '''
        self.path = InPath + FileName
        self.OutPath = OutPath
        self.fid = FileName
        self.EndofHeaderdef = ['END', 'OF', 'HEADER']
        self.header = {}
        self.rnx = {}
        self.system = {'GPS':0, 'Glonass':1, 'Galileo': 2, 'Beidu':3}
        # db
        self.fields = ['year','doy','hour','minutes','seconds', 'system', 'prn']
            
        self.dbFileName = 'thisdata.db'
        self.prnObs = {}
    
    def Header(self):
        '''
        ================================================================
        Gets the header of the observation file,
        Puts the header data in header array. 
        It outputs the header array, 
        also assigns it the to self
        Usage:
            rnx = Rinex(path)
            rnxHeader = rnx.Header()
        Output:
            returns the list of Header data.
            The important elements are as below:
                header['version'] : version of the rinex format
                header['Observations']: list of the Types of observables
        ================================================================
        '''
        Hdr = self.Body(ReadBody = False)
        for line in Hdr:
            identifiers = line[60:-1].split('/')
            if len(identifiers) > 1:
                if identifiers[0].strip() == 'RINEX VERSION':
                    self.header['Version'] = float(line[:20].strip())
                elif identifiers[1].strip() == 'TYPES OF OBSERV':
                    self.header['Observations'] = line[:60].strip().split()
            else:
                if identifiers[0].strip() == 'TIME OF FIRST OBS':
                    self.header['FirstObsTime'] = line[:60].strip().split()
                if identifiers[0].strip() == 'INTERVAL':
                    self.header['INTERVAL'] = int(line[:60].strip().split()[0])
        return self.header
    
    def Body(self, ReadBody = True)-> list:
        '''
        ================================================================
        Loads file into Header and body arrays.
        Refer to Header and load functions.
        In Header and load functions the arrays will -
        be allocated to the corresponding fields.
        usage:
            rnx = Rinex(path)
            rnxBody = rinex.Body(ReadBody = True)) 
            or
            rnxHeader = rinex.Body(ReadBody = False))
        returns: header and body lists of the observations in rinex
        ================================================================
        '''
        line : str
        lines = []
        
        with open(self.path) as rnx:
            for line in rnx:
                lines.append(line)
                if line.split() == self.EndofHeaderdef:
                    if not ReadBody: return lines
                    lines = []
            if ReadBody: return lines
            rnx.close()
            
    def load(self):
        '''
        ================================================================
        Reads the Rinex data and puts it in a sqlite db Table.
        Usage:
            rnx = Rinex(path)
            rnxData = rnx.load()
        Outputs:
            No array outputs. The db file will be saved to the I_O 
            file in the Project WorkSpace
            db File structure is as below:
             ________________________________________________
            | Year| Doy| Hour| Minutes| Seconds| Other Fiels|
            ------------------------------------------------
            The 'other fields' is same as the observation types 
            indicated in the rinex file.
        ================================================================
        '''
        # =========================================================================
        self.Header()
        # =========================================================================
        Bdy = self.Body(ReadBody = True)
        ObsList = self.header['Observations'][1:]
        # =========================================================================
        #construct the observation dictionary       
        def epochInfo(line):
            '''
            ================================================================
            Gets the information of the current ecpoch \
            (date, time, number of observations in current epoch, prn numbers)
            Input:
                 must be the line of epochs which includes the epoch and prn number
                (First line in each epoch)
            Usage:
                epoch, prns = epochInfo(line)
            Outputs:
                epoch and prns given in the epoch line
            ================================================================
            '''
            line = line.strip().split()
            epoch = [int(item) for item in line[:5]]
            epoch.append(float(line[6]))
            if epoch[0] < 50: epoch[0] = epoch[0] + 2000
            else: epoch[0] = epoch[0] + 1900
            CurrentObsNum = int(line[7])
            prns = [int(item) for item in line[8:]]
            return epoch, prns
        # =========================================================================
        def readEpochbody(line):
            '''
            ================================================================
            puts the observables of the given line in the given epoch
            Input:
                must be a line of observation including all \
                observables in the given epoch for given prn
            Usage:
                prnObs = readEpochbody(line)
            Output:
                includes the dictionary of the observations in current line
                wit the fields of field_
            ================================================================
            '''
            line = line.strip().split()
            prnObs = {}
            for idx, item in enumerate(ObsList):
                prnObs[item] = line[idx]
            return prnObs
        # =========================================================================
        if self.header['Version'] == 2.0:
            system_ = self.header['FirstObsTime'][-1]
            ObsList.insert(1,'L1_SNR')
            ObsList.insert(3,'L2_SNR')
            
            l = len(Bdy[1].strip().split()) + 3
            line = [None] * l
            
            data = {}
            for item in self.fields:
                data[item] = []
            
            epochLine, lNum = 0, 0

            def ConstructDataMat(*args):
                # Estimate the length of arrays
                interval = self.header['INTERVAL'] #seconds
                FirstObsTime = self.header['FirstObsTime'][:6]
                FirstObsTime[0:5] = [int(item) for item in FirstObsTime[:5]]
                FirstObsTime[5] = int(float(FirstObsTime[5]))
                temp = Bdy[-50:]#get last 50 obs lines
                temp = np.flip(temp,0)
                LASTObsTime = 0
                for lx in temp:
                    
                    if float(lx.strip().split()[6]) == 0.0: 
                        LASTObsTime = lx.strip().split()[:6]
                        LASTObsTime[0:5] = [int(item) for item in LASTObsTime[:5]]
                        LASTObsTime[5] = int(float(LASTObsTime[5]))
                        if int(LASTObsTime[0]) < 50: 
                            LASTObsTime[0] += 2000
                        else:
                            LASTObsTime[0] += 1900
                    elif isinstance(LASTObsTime , list):
                        del temp 
                        break
                
                FileDuration =\
                (datetime(\
                          LASTObsTime[0],LASTObsTime[1],LASTObsTime[2],\
                          LASTObsTime[3],LASTObsTime[4],LASTObsTime[5]) -\
                datetime(\
                          FirstObsTime[0],FirstObsTime[1],FirstObsTime[2],\
                          FirstObsTime[3],FirstObsTime[4],FirstObsTime[5])).total_seconds()
                # Compute the maximum number of epochs
                N_epochLines = FileDuration/interval
                if N_epochLines.is_integer():
                    N_epochLines = int(N_epochLines)
                else:
                    N_epochLines = int(np.ceil(N_epochLines))
                
                for field in self.fields:
                    data[field] = np.zeros(len(Bdy) - N_epochLines + 26)
                    
                for field in ObsList:
                    data[field] = np.zeros(len(Bdy) - N_epochLines + 26)
                    
                return data
            
            data = ConstructDataMat()
            lNum = -1
            while epochLine < len(Bdy):
                
                epochInformation = Bdy[epochLine].strip().split()
                if int(epochInformation[0]) < 50 : 
                    epochInformation[0] = str(int(epochInformation[0]) + 2000)
                else:
                    epochInformation[0] = str(int(epochInformation[0]) + 1900)
                _time = ('{0:4}-{1:2}-{2:2}T{3:2}:{4:2}:{5}').format\
                (epochInformation[0].zfill(4),epochInformation[1].zfill(2),\
                 epochInformation[2].zfill(2),epochInformation[3].zfill(2),\
                 epochInformation[4].zfill(2),epochInformation[5].zfill(2))
                _time = Time(_time)
                
                prns = [int(item) for item in epochInformation[8:]]
                bdy = Bdy[epochLine + 1 : epochLine + len(prns) + 1]
                
                l= epochLine + len(prns) + 1
                
                epoch = np.zeros(6)
                epoch[0:5] = [int(item) for item in epochInformation[0:5]]
                epoch[5] = float(epochInformation[5])
                #if epoch[0] < 50: epoch[0] += 2000.0
                #else: epoch[0] += 1900 
                year, month, day = int(epoch[0]), int(epoch[1]), int(epoch[2])
                doy = datetime(year,month,day).timetuple().tm_yday
                hour, minutes,seconds = int(epoch[3]), int(epoch[4]), int(epoch[5])
                
                for obsline, prn in enumerate(prns):
                    lNum += 1 

                    obs = bdy[obsline].strip().split()
                    
                    system = self.system[system_]
                    
                    for item in self.fields:
                        try:
                            data[item][lNum] = eval(item)
                        except:
                            np.append(data[item],eval(item))
                            
                    for index, item in enumerate(ObsList):
                        try:
                            data[item][lNum] = obs[index]
                        except:
                            np.append(data[item],obs[index])
                        
                epochLine += len(prns)+1
            field = self.fields
            field_ = field.extend(ObsList)
            path = self.OutPath
            hdf = pd.HDFStore(path + 'rinex.hdf5') 
            df2 = pd.DataFrame(data, columns = field_)
            hdf.put(self.fid, df2, format = 'table', datacolumns = True)
                
            return data

if __name__ == '__main__':
#     path = '/home/gravity/Dropbox/Sample_Data/cham0140.06o'
#     rnx = Rinex(path)
#     rnx.load() # help(rnx.load)
    print('Readint Rinex File')
    