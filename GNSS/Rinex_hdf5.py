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
import h5py

class Rinex():
    '''
    Object of Rinex Data
    Attributes are the Heading of the Rinex
    '''


    def __init__(self, path):
        '''
        Constructor
        '''
        self.path = path
        self.EndofHeaderdef = ['END', 'OF', 'HEADER']
        self.header = {}
        self.rnx = {}
        self.DateTimeList = ['hour','minutes','seconds','centiseconds']
        self.DateTime = {}
        for dt in self.DateTimeList:
            self.DateTime[dt] = 0
        
        # db
        self.fields = ['hour','minutes','seconds', 'system', 'prn']
        self.types = ['integer','integer','integer','integer','integer','float', 'text', 'integer']
            
        self.dbFileName = 'thisdata.db'
        self.prnObs = {}
            
    def Body(self):
        
        # =========================================================================
        for item in self.DateTimeList:
            exec(item + ' = 0')
        # =========================================================================
        self.Header()
        # =========================================================================
        # get the time of observation file
#         FirstObsTime = self.header['FirstObsTime'][:-1]
#         for idx , item in enumerate(FirstObsTime):
#             try:
#                 dt = self.DateTimeList[idx]
#                 self.DateTime[dt] = int(item)
#                 
#                 exec(dt + ' = int(item)')
#             except:
#                 FirstObsTime.append(0)
#                 intPart, decimalPart = math.modf(float(item))
#                 dt0 = self.DateTimeList[idx]
#                 self.DateTime[dt0] = int(intPart)
#                 dt1 = self.DateTimeList[idx+1]
#                 self.DateTime[dt1] = int(decimalPart*100)
#                 exec(dt0 + ' = int(intPart)')
#                 exec(dt1 + ' = int(decimalPart)*100')
#                 break
#         # =========================================================================
#         exec('self.rnx["datetime"] = datetime(hour,minutes,seconds,centiseconds)')
#         print(self.rnx['datetime'])
        # =========================================================================
        Bdy = self.load(ReadBody = True)
        ObsList = self.header['Observations'][1:]
        # =========================================================================
        #construct the observation dictionary       
        def epochInfo(line):
            line = line.strip().split()
            epoch = [int(item) for item in line[:5]]
            epoch.append(float(line[6]))
            if epoch[0] < 50: epoch[0] = epoch[0] + 2000
            else: epoch[0] = epoch[0] + 1900
            CurrentObsNum = int(line[7])
            prns = [int(item) for item in line[8:]]
            return epoch, prns
        
        def readEpochbody(line):
            line = line.strip().split()
            prnObs = {}
            for idx, item in enumerate(ObsList):
                prnObs[item] = line[idx]
            return prnObs
        
        if self.header['Version'] == 2.0:
            system = self.header['FirstObsTime'][-1]
            ObsList.insert(1,'L1_SNR')
            ObsList.insert(3,'L2_SNR')
            
            for item in ObsList: 
                self.fields.append(item)
                self.types.append('float')
            table = ' \n '
            
            fields = self.fields[3:]
            
            for idx, item in enumerate(self.fields):
                table =table + item + ' ' + self.types[idx] + ', \n '
            
            #data = np.zeros((len(Bdy),len(Bdy[1].strip().split()) + 8))    
            l = len(Bdy[1].strip().split()) + 4
            line = [None] * l
            #data = [[None] * l] * len(Bdy)
            data=[]
            epochLine = 0
            lNum = 0
            print(len(Bdy))
            while epochLine < len(Bdy):
                
                epochInformation = Bdy[epochLine].strip().split()
                prns = [int(item) for item in epochInformation[8:]]
                bdy = Bdy[epochLine + 1 : epochLine + len(prns) + 1]
                l= epochLine + len(prns) + 1
                epoch = np.zeros(6)
                epoch[0:5] = [int(item) for item in epochInformation[0:5]]
                epoch[5] = float(epochInformation[5])
                
                if epoch[0] < 50: epoch[0] += 2000.0
                else: epoch[0] += 1000 
                year, month, day = epoch[0], epoch[1], epoch[2]
                
                for obsline, prn in enumerate(prns):
                    
                    lNum = epochLine + obsline
                    line[0:3] = epoch[3:6]
                    line[3] = prn
                    line_ = [float(item) for item in bdy[obsline].strip().split()]
                    line[4:] = line_
                    data.append( np.transpose(line) )
                    line = [None] * l
                epochLine += len(prns)+1
            print('done')
            data = np.array(data)

            with h5py.File('test.hdf5','w') as f: 
                G0 = f.create_group( str(int(year)) + '/' + str(int(month)) + '/'+ str(int(day)) ) # parent year, child month
                G0.create_dataset( system, shape = np.shape(data), data = data, compression = 'gzip', compression_opts = 9) # grandchild day
                G0.attrs['CLASS'] = 'SatWare rnx MATRIX'
                G0.attrs['VERSION'] = 'v1.001'
                
                f.close()
                
   
    def Header(self):
        Hdr = self.load(ReadBody = False)
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
        return self.header

    def load(self, ReadBody = True)-> list:
        '''
        Loads file into Header and body arrays.
        Refer to Header and Body functions.
        In Header and Body functions the arrays will -
        be allocated to the corresponding fields.
        usage:
            rnx = Rinex(path)
            rnxBody = rinex.load(ReadBody = True)) 
            or
            rnxHeader = rinex.load(ReadBody = False))
        returns: header and body lists of the observations in rinex
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

if __name__ == '__main__':
    path = '/home/gravity/Dropbox/Sample_Data/cham0140.06o'
    rnx = Rinex(path)
    header = rnx.Header()
    rnx.Body()
    rnx.load() # help(rnx.load)
    