'''
Created on Feb 12, 2019

@author: Amir Yeganehsahab
         Middle East Tech.
         (A University that I would not get in if I could go back in time. 
         Low quality in terms of student profile and staff knowledge)
         Turkey/ Ankara 
'''
import math
import numpy as np
from xml.dom import IndexSizeErr
from _datetime import datetime
import time
import sqlite3
import os

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
        self.DateTimeList = ['year','month','day','hour','minutes','seconds','centiseconds']
        self.DateTime = {}
        for dt in self.DateTimeList:
            self.DateTime[dt] = 0
        
        # db
        self.fields = ['year','month','day','hour','minutes','seconds', 'prn', 'system']
        self.types = ['integer','integer','integer','integer','integer','float', 'integer', 'text']
            
        self.dbFileName = 'thisdata.db'
        self.prnObs = {}
            
    def Body(self):
        '''
        ================================================================
        Reads the Rinex data and puts it in a sqlite db Table.
        Usage:
            rnx = Rinex(path)
            rnxData = rnx.Body()
        Outputs:
            No array outputs. The db file will be saved to the I_O 
            file in the Project WorkSpace
            db File structure is as below:
             _______________________________________________________
            | Year| Month| Day| Hour| Minutes| Seconds| Other Fiels|
            -------------------------------------------------------
            The 'other fields' is same as the observation types 
            indicated in the rinex file.
        ================================================================
        '''
        # ================== Pre allocate the Time values =========================
        # year = 0; month = 0, day = 0; hour = 0; minutes = 0; seconds = 0 # result
        for item in self.DateTimeList:
            exec(item + ' = 0')
        # ================== Header of the file ====================================
        self.Header()
        # ================== time of first observation =============================
        FirstObsTime = self.header['FirstObsTime'][:-1]
        for idx , item in enumerate(FirstObsTime):
            try:
                dt = self.DateTimeList[idx]
                self.DateTime[dt] = int(item)
                exec(dt + ' = int(item)')
            except:
                FirstObsTime.append(0)
                intPart, decimalPart = math.modf(float(item))
                dt0 = self.DateTimeList[idx]
                self.DateTime[dt0] = int(intPart)
                dt1 = self.DateTimeList[idx+1]
                self.DateTime[dt1] = int(decimalPart*100)
                exec(dt0 + ' = int(intPart)')
                exec(dt1 + ' = int(decimalPart)*100')
                break
        # ================== save the result as date time ============================
        exec('self.rnx["datetime"] = datetime(year,month,day,hour,minutes,seconds,centiseconds)')
        print('rinex of {} is being loaded'.format(self.rnx['datetime']))
        # ================== load the Trunc of the rinex ===============================
        Bdy = self.load(ReadBody = True)
        ObsList = self.header['Observables'][1:]
        # ================== construct the observation dictionary ======================
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
            epoch.append(float(line[5]))
            if epoch[0] < 50: epoch[0] = epoch[0] + 2000
            else: epoch[0] = epoch[0] + 1900
            CurrentObsNum = int(line[7])
            prns = [int(item) for item in line[8:]]
            # Control
            if not CurrentObsNum == len(prns): raise IndexSizeErr() 
            return epoch, prns
        
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
            ================================================================
            '''
            line = line.strip().split()
            prnObs = {}
            for idx, item in enumerate(ObsList):
                prnObs[item] = line[idx]
            return prnObs
        # ======================= For version 2 =========================================
        
        if self.header['Version'] == 2.0:
            system = self.header['FirstObsTime'][-1]
            ObsList.insert(1,'L1_SNR')
            ObsList.insert(3,'L2_SNR')
            
            for item in ObsList: 
                self.fields.append(item)
                self.types.append('float')
            table = ' \n '
            for idx, item in enumerate(self.fields):
                table =table + item + ' ' + self.types[idx] + ', \n '
            SqliteCommand = "CREATE TABLE data (" + table[:-4] + ")"
            
            conn = sqlite3.connect(self.dbFileName)
            c = conn.cursor()
            if not os.path.isfile(self.dbFileName):
                c.execute(SqliteCommand)
            else:
                conn.close()
                os.remove(self.dbFileName) 
                conn = sqlite3.connect(self.dbFileName)
                c = conn.cursor()
                c.execute(SqliteCommand)           
            read_epochInfo = True
            epochLine = 0
            
            self.prnObs['system'] = '"{}"'.format(system)
            while epochLine < len(Bdy):
                
                line = Bdy[epochLine]
                epoch, prns = epochInfo(line)
                dPatch = Bdy[epochLine+1:epochLine+len(prns)+1]
                if not len(prns) == len(dPatch):
                    raise IndexSizeErr()
                
                for idx, item in enumerate(self.DateTimeList[:-1]):
                    exec(item + '= epoch[idx]')
                    self.prnObs[item] = epoch[idx]
                
                for idx, prn in enumerate(prns):
                    patch = dPatch[idx]
                    self.prnObs['prn'] = prn
                    self.prnObs.update(readEpochbody(patch))
                    cmd = ''
                    for field in self.fields:
                        cmd = cmd + '{},'.format(self.prnObs[field])
                    c.execute('INSERT INTO {} Values ({})'.format('data',cmd[:-1]))
                    cmd = {}
                    
                if epochLine % 100 == 0:
                    print('epoch number {} with {} prns is loaded'.format(epochLine, len(prns)))
                epochLine = epochLine + len( prns ) + 1
        conn.commit()
        conn.close()
        
        
    def Header(self):
        '''
        ================================================================
        Getd the header of the observation file,
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
        Hdr = self.load(ReadBody = False)
        for line in Hdr:
            self.header[line[60:-1]] = line[:60] 
            identifiers = line[60:-1].split('/')
            if len(identifiers) > 1:
                if identifiers[0].strip() == 'RINEX VERSION':
                    self.header['Version'] = float(line[:20].strip())
                elif identifiers[1].strip() == 'TYPES OF OBSERV':
                    self.header['Observables'] = line[:60].strip().split()
            else:
                if identifiers[0].strip() == 'TIME OF FIRST OBS':
                    self.header['FirstObsTime'] = line[:60].strip().split()
        return self.header

    def load(self, ReadBody = True)-> list:
        '''
        ================================================================
        Loads file into Header and body arrays.
        Refer to Header and Body functions.
        In Header and Body functions the arrays will -
        be allocated to the corresponding fields.
        usage:
            rnx = Rinex(path)
            rnxBody = rnx.load(ReadBody = True)) 
            or
            rnxHeader = rnx.load(ReadBody = False))
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

if __name__ == '__main__':
    path = '/home/gravity/Dropbox/Sample_Data/cham0140.06o'
    rnx = Rinex(path)
    header = rnx.Header()
    rnx.Body()
    rnx.load() # help(rnx.load)
    