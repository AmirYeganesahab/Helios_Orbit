'''
Created on Feb 23, 2019

@author: geomatics
'''
from astropy.time import Time, TimeDelta
import pyproj
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
from xml.dom import IndexSizeErr
from _datetime import datetime
from numpy.polynomial import polynomial as plft
from scipy import interpolate as ntp
from Math.polynomial import *
import matplotlib
import os
import mpl_toolkits
import cartopy.crs as ccrs

class Read():
    '''
    classdocs
    '''
    def __init__(self, file, fileType : str):
        '''
        Constructor
        '''
        # ============================ inits of rinex obs file ============================
        # Read Header
        if fileType == 'rinex':
            self.requirements = ['RINEX VERSION', 'INTERVAL', 'TIME OF FIRST OBS',\
                                 'APPROX POSITION XYZ', 'ANTENNA: DELTA H/E/N',\
                                 'TYPES OF OBSERV']
        elif fileType == 'brdc':
            self.requirements = ['RINEX VERSION', 'ION ALPHA', 'ION BETA',\
                                 'DELTA-UTC: A0,A1,T,W', 'LEAP SECONDS','TYPE']
            
            l1 = ['iPRN','iEpochYear','iEpochMonth','iEpochDay','iEpochHour','iEpochMinute','iEpochSecond', 'dateTime','dClockBias','dClockDrift','dClockDriftRate']
            l2 = ['dIDOE','dCrs','dDeltaN','dM0']
            l3 = ['dCuc','dEccent','dCus','dSqrtA']
            l4 = ['dToe','dCic','dOMEGA','dCis']
            l5 = ['di0','dCrc','dOmega','dOMEGADot']
            l6 = ['dIdot','dCodeOnL2','dGpsWeek','dPDataFlag']
            l7 = ['dSVaccur', 'dSVhealth', 'dTGD','dIODC']
            l8 = ['dTransTime','dSpare1','dSpare2','dSpare3']
            self.list = []
            for i in range(8): 
                self.list.extend(eval('l{}'.format(i+1)))
            self.brdc_list = {}
            for item in self.list: self.brdc_list[item] = None
            #Ephemeris Overlap : 3 hours
            A = Time(datetime(2000,1,1,3,0,0))
            B = Time(datetime(2000,1,1,0,0,0))
            self.ephOverLap =  A - B # Result is in days (0.125*24 >> hours)
            del A,B
            # interval = 15*60 (15 minutes
            A = Time(datetime(2000,1,1,0,15,0))
            B = Time(datetime(2000,1,1,0,0,0))
            self.dInterval =  A - B # Result is in days (0.125*24 >> hours)
            
            # ========================== Standard Orbit Attributes ========================== 
            PolynomialOrder = 16
            self.StandardOrbit = {'PolynomialOrder' : PolynomialOrder,
                                  'nPolynomialCoeff' : PolynomialOrder + 1,
                                  'dTbeg' : Time,
                                  'dTend' : Time,
                                  'dInterval': 2*3600,
                                  
                                  'dXCoef' : None,
                                  'dXmu' : np.zeros(2),
                                  'dYCoef' : None,
                                  'dYmu' : np.zeros(2),
                                  'dZCoef' : None,
                                  'dZmu' : np.zeros(2),
                                  'dFitInt' : 4*3600,
                                  'dTimeSet' : Time}
        self.f = file
        self.headerInfo = {}
        self.cursor = None
        self.SNRs = ['S1','S2']
        
        self.my = 3.986005e14              # Gravitional constant for WGS84
        self.OmegaDotE = 7.2921151467e-5   # Earth's rotation rate for WGS84  
        self.C = 299792458                 # The speed of light in vacuum
        
        self.current_t = 0
        #GPS frequencies
        self.f_L1 = 1575.42e6
        self.f_L2 = 1227.60e6
        # GPS waveLengthes
        self.Lmbd_L1 = self.C/self.f_L1
        self.Lmbd_L2 = self.C/self.f_L2
        
    def Header(self):
        '''
            Read Until the End of rinex Heading and returns the header info and cursor
        ''' 
        line : str
        identification : str
        description : str
        identification_ : str
        idx : int
        item : str
        a : int

        while True:
            line = self.f.readline()
            identification = line[60:].strip()
            description = line[:60].strip()
            if identification in self.requirements:
                self.headerInfo[identification] = description
                a = self.requirements.index(identification)
                del self.requirements[a]
            elif '/' in identification:
                identification_ = identification.strip().split('/')
                if identification_[0].strip() == '#': 
                    self.headerInfo[identification_[1].strip()] = description.strip().split() 
                else:
                    for idx, item in enumerate(identification_):
                        if item.strip() in self.requirements:
                            self.headerInfo[item.strip()] = description.strip().split()[idx]
                            a = self.requirements.index(item.strip())
                            del self.requirements[a]
            if identification == 'END OF HEADER':
                self.cursor = self.f.tell()
                break
            
    def rnxLoad(self):
        ObsType : list
        line : str
        epoch : list
        epoch_ : list
        _time : datetime
        nObs : int
        prns : list
        obs: list
        idx0 : int 
        prn : int 
        idx1 : int
        item : str
         
        self.f.seek(self.cursor)
        
        ObsType = self.headerInfo['TYPES OF OBSERV'][1:]
        if self.headerInfo['RINEX VERSION'] == '2':
            ObsType.insert(1,'S1')
            ObsType.insert(3,'S2')
        elif self.headerInfo['RINEX VERSION'] == '2.20':
            pass
        # epochInfo
        line = self.f.readline()
        if len(line) == 0: return None
        line = line.strip().split()
        epoch = line[:6]

        year = int(epoch[0])
        if int(epoch[0]) < 50: 
            epoch[0] = str(year + 2000)
        else: 
            epoch[0] = str(year + 1900)

        epoch_ = [int(e) for e in epoch[:5]]
        # centisec
        if epoch[5] != (float(epoch[5])//1):
            epoch_.append(int(float(epoch[5])//1))
            epoch_.append(int(float(epoch[5]) - float(epoch[5])//1))
        else:
            epoch_.append(float(epoch[5])//1)
            
        _time = Time(datetime(epoch_[0],epoch_[1],epoch_[2],epoch_[3],epoch_[4],epoch_[5],epoch_[6]))
        
        nObs = int(line[7])
        
        prns = [int(prn) for prn in line[8:]]
        obs = {}
        for item in ObsType:
            obs[item] = np.zeros(nObs)
        obs['prns'] = prns
        obs['mjd'] = _time
        
        for idx0, prn in  enumerate(prns):
            #print(len(prns),prn,idx0,prns, nObs)
            line = self.f.readline().strip().split()
            #print(line)
            while len(line) < len(ObsType):
                line.extend(self.f.readline().strip().split())
            if len(line) > nObs:
                pass
                #raise ValueError('Something is wrong here')
                
            for idx1,item in enumerate(ObsType):
                obs[ObsType[idx1]][idx0] = float(line[idx1])
        self.cursor = self.f.tell()
        return obs
        
    def autolabel(self,rects,showprns = True):
        """
        Attachs a text label above each bar displaying its height
        """
        for rect in rects:
            height = rect.get_height()
            font = {'size': 5}
            if showprns:
                plt.text(rect.get_x() + rect.get_width()/2.0, 0,
                         '%d' % int(rect.get_x()+1),
                         ha='center', va='bottom', fontsize = 5)
            plt.text(rect.get_x() + rect.get_width()/2.0, height,
                    '%d' % int(height),
                    ha='center', va='bottom', fontsize = 5)

    def brdcLoad(self):
        '''
            Broadcast Emepheris from Rinex file
            ============ PRN / EPOCH / SV CLK ============
             Satellite PRN number           : iPRN
             Epoch year                     : iEpochYear
             Epoch month                    : iEpochMonth
             Epoch day                      : iEpochDay
             Epoch hour                     : iEpochHour
             Epoch minute                   : iEpochMinute
             Epoch second                   : iEpochSecond
             Sat Clock Bias (sec)           : dClockBias
             Sat Clock drift(sec/sec)       : dClockDrift
             Sat Clock drift rate (sec/sec2): dClockDriftRate
            ============ BROADCAST ORBIT - 1 ============
             IDOE Issue of Data, Ephemeris  : dIDOE
             Crs (meters)                   : dCrs
             Delta n (radians/sec)          : dDeltaN
             M0 (radians)                   : dM0
            ============ BROADCAST ORBIT - 2 ============
             Cuc (radians)                  : dCuc
             e Eccenricity                  : dEccent
             Cus (radians)                  : dCus
             sqrt(A) (sqrt(m))              : dSqrtA
            ============ BROADCAST ORBIT - 3 ============
             Toe Time of Ephemeris (sec of GPS week): dToe
             Cic (radians)                  : dCic
             OMEGA (radians)                : dOMEGA
             Cis (radians)                  : dCis
            ============ BROADCAST ORBIT - 4 ============
             i0                             : di0
             Crc (radians)                  : dCrc
             omega (radians)                : dOmega
             OMEGA Dot (radians)            : dOMEGADot
            ============ BROADCAST ORBIT - 5 ============
             Idot                           : dIdot
             Codes on L2 channel            : dCodeOnL2
             GPS Week # (to go with TOE)    : dGpsWeek
             L2 P data flag                 : dPDataFlag
            ============ BROADCAST ORBIT - 6 ============
             SV Accuracy (meters)           : dSVaccur
             SV health   (MSB only)         : dSVhealth
             TGD                            : dTGD
             IODC Issue of Data, Clock      : dIODC
            ============ BROADCAST ORBIT - 7 ============
             Transmission time of message   : dTransTime
             Spare1                         : dSpare1
             Spare2                         : dSpare2
             Spare3                         : dSpare3
        '''
        __annotations__ = {'df' : list,
        'line' : str,
        'year' : int,
        'month' : int,
        'day' : int,
        'Hour' : int,
        'Minute' : int,
        'Second_' : float,
        'centisec' : int,
        'Second' : int,
        'epoch' : datetime}
        
        self.f.seek(self.cursor)
        df = pd.DataFrame(columns = self.list)
        while True: 
            # ============ PRN / EPOCH / SV CLK ============   
            line = self.f.readline()
            if len(line) == 0: break
            # Line 1
            self.brdc_list['iPRN'] = int(line[:2])
            year = int(line[2:5])
            if year < 94: 
                year += 2000
            else: 
                year += 1900
            month,day = int(line[5:8]), int(line[8:11])
            Hour, Minute, Second_ = int(line[11:14]), int(line[14:18]), float(line[18:22])
            centisec = 0
            if Second_ != int(Second_):
                centisec = Second_ - int(Second_)
                Second = int(Second_)
            else:
                Second = int(Second_)
                
            epoch = datetime(year,month,day,Hour,Minute,Second, centisec)
            
            self.brdc_list['iEpochYear']    = year
            self.brdc_list['iEpochMonth']   = month
            self.brdc_list['iEpochDay']     = day
            self.brdc_list['iEpochHour']    = Hour
            self.brdc_list['iEpochMinute']  = Minute
            self.brdc_list['iEpochSecond']  = Second_
            
            self.brdc_list['dateTime'] = Time(epoch)
            self.brdc_list['dClockBias'] = float(line[22:41])
            self.brdc_list['dClockDrift'] = float(line[41:60])
            self.brdc_list['dClockDriftRate'] = float(line[60:79])
            # ============ BROADCAST ORBIT - 1 ============
            line = self.f.readline()
            
            self.brdc_list['dIDOE'] = float(line[3:22])
            self.brdc_list['dCrs'] = float(line[22:41])
            self.brdc_list['dDeltaN'] = float(line[41:60])
            self.brdc_list['dM0'] = float(line[60:79])
            # ============ BROADCAST ORBIT - 2 ============
            line = self.f.readline()
            
            self.brdc_list['dCuc'] = float(line[3:22])
            self.brdc_list['dEccent'] = float(line[22:41])
            self.brdc_list['dCus'] = float(line[41:60])
            self.brdc_list['dSqrtA'] = float(line[60:79])
            # ============ BROADCAST ORBIT - 3 ============
            line = self.f.readline()
            
            self.brdc_list['dToe'] = float(line[3:22])
            self.brdc_list['dCic'] = float(line[22:41])
            self.brdc_list['dOMEGA'] = float(line[41:60])
            self.brdc_list['dCis'] = float(line[60:79])
            # ============ BROADCAST ORBIT - 4 ============
            line = self.f.readline()
            
            self.brdc_list['di0'] = float(line[3:22])
            self.brdc_list['dCrc'] = float(line[22:41])
            self.brdc_list['dOmega'] = float(line[41:60])
            self.brdc_list['dOMEGADot'] = float(line[60:79])
            # ============ BROADCAST ORBIT - 5 ============
            line = self.f.readline()
            
            self.brdc_list['dIdot'] = float(line[3:22])
            self.brdc_list['dCodeOnL2'] = float(line[22:41])
            self.brdc_list['dGpsWeek'] = float(line[41:60])
            self.brdc_list['dPDataFlag'] = float(line[60:79])
            # ============ BROADCAST ORBIT - 6 ============
            line = self.f.readline()
            
            self.brdc_list['dSVaccur'] = float(line[3:22])
            self.brdc_list['dSVhealth'] = float(line[22:41])
            self.brdc_list['dTGD'] = float(line[41:60])
            self.brdc_list['dIODC'] = float(line[60:79])
            # ============ BROADCAST ORBIT - 7 ============
            line = self.f.readline()
            
            if len(line) > 78:
                self.brdc_list['dTransTime'] = float(line[3:22])
                self.brdc_list['dSpare1'] = float(line[22:41])
                self.brdc_list['dSpare2'] = float(line[41:60])
                self.brdc_list['dSpare3'] = float(line[60:79])
            elif len(line) > 55:
                self.brdc_list['dTransTime'] = float(line[3:22])
                self.brdc_list['dSpare1'] = float(line[22:41])
                self.brdc_list['dSpare2'] = float(line[41:60])               
            elif len(line) > 23:
                self.brdc_list['dTransTime'] = float(line[3:22])
                self.brdc_list['dSpare1'] = float(line[22:41])               
            elif len(line) < 23:
                self.brdc_list['dTransTime'] = float(line[3:22])
            
            df = df.append(self.brdc_list, ignore_index=True)
        return df
    
    def beEphCoordCalc(self,mData,vObsTime):
        '''
             This function calculates the coordinates from the broadcast ephemeris at
             all aviliable satellits in the the inserted RINEX file
            
             The function takes the following input parameters 
            
                vCoordinateVector = beEphCoordCalc(sFileName,vObsTime)
              
                sFileName - String with the filename
                vObsTime  - time in [FateTime]
            
            
             This function calls the following functions
               # brEphRinexRead(sFileName)
               # brEphCoordCalcOneDataSet(vObs,cObsTime)
        '''
        prns = np.unique(mData.iPRN)
        
        if (vObsTime - self.dStart) < 0 or (vObsTime - self.dEnd) > 0:
            print(vObsTime)
            ValueError('No broadcast ephemeris for this epoch')
            
        NoData = 1
        data_ = {}
        
        #df_ = pd.DataFrame(columns = ['prn','dX','dY','dZ','dDts','dTGD'])
        data_ = {'prn': np.zeros(len(prns)),
                 'X': np.zeros(len(prns)),
                 'Y': np.zeros(len(prns)),
                 'Z':np.zeros(len(prns)),
                 'Dts': np.zeros(len(prns)),
                 'TGD': np.zeros(len(prns))} 
        for i,prn in enumerate(prns):
            prnData = mData.query('iPRN == {}'.format(prn))
            MinDiff = 1e15  #Time difference in [s]
            MinIdx = 0      #index to the closest epoch
        
            for idx, row in  prnData.iterrows():
                dJDSat = row.dateTime
                Tdif = abs(dJDSat - vObsTime)
            
                if Tdif < MinDiff:
                    MinDiff = Tdif
                    MinIdx = idx
                    data = row
                    NoData = 0
            
            if NoData: continue

            data_['prn'][i] = prn
            data_['X'][i], data_['Y'][i], data_['Z'][i], data_['Dts'][i], data_['TGD'][i] =\
              self.brEphCoordCalcOneDataSet( data, vObsTime )
        return data_
                         
    def brEphCoordCalcOneDataSet(self, vObs, cObsTime):
        '''
         This function calculates coordinates of one satellite at observation time
         "cObsTime" from observations in the observation vector "vObs". 
         
         To call the function, use 
        
            [x,y,z,ds,TGD]=brEphCoordCalcOneDataSet(vObs,cObsTime)
        
         where 
           (x,y,z)  - are satellite coordinates in WGS84
           ds       - delta SV PRN code phase time offset in seconds
           TGD      - Differential Group delay in seconds
           vObs     - observation vector
           cObsTime - The current observation time in reciver time
        '''
        F = -2 * np.sqrt(self.my)/self.C**2
        
        prns = vObs.iPRN
        dtTocl = vObs.dateTime
        
        a0 = vObs.dClockBias
        a1 = vObs.dClockDrift
        a2 = vObs.dClockDriftRate
        # BroadcastOrbit - 1
        IODE = vObs.dIDOE         # Issue of data (ephemeris)
        Crs = vObs.dCrs           # Amplitude of second-order harmonic pertubations
        Delta_n = vObs.dDeltaN    # Mean motion difference from computed value
        M0 = vObs.dM0             # Mean anomaly at reference time
        # BroadcastOrbit - 2
        Cuc = vObs.dCuc           # Amplitude of second-order harmonic pertubations
        e = vObs.dEccent          # Eccentricity
        Cus = vObs.dCus           # Amplitude of second-order harmonic pertubations
        a = (vObs.dSqrtA)**2;     # (Square root of the semi major axis)^2
        # BroadcastOrbit - 3
        Toe = vObs.dToe           # Ephemeris reference time
        Cic = vObs.dCic           # Amplitude of second-order harmonic pertubations
        OMEGA = vObs.dOMEGA       # Longitude of ascending node of orbit plane at beginning of week
        Cis = vObs.dCis           # Amplitude of second-order harmonic pertubations
        # BroadcastOrbit - 4
        i0 = vObs.di0             # Inclination angle at reference time
        Crc = vObs.dCrc           # Amplitude of second-order harmonic pertubations
        omega = vObs.dOmega       # Argument of perigee
        OMEGA_DOT = vObs.dOMEGADot# Rate of right ascension
        # BroadcastOrbit - 5
        IDOT = vObs.dIdot                     # Rate of incliniation angle
        Codes_On_L2_channel = vObs.dCodeOnL2
        GPS_WEEK = vObs.dGpsWeek              # To go with TOE
        dtToe = Time(self.weeksecondstoutc(GPS_WEEK,Toe)) ## --> '2014-09-22 21:36:52'
        L2_data_flag = vObs.dPDataFlag 
        # BroadcastOrbit - 6
        SV_accuracy = vObs.dSVaccur       # (meters)
        SV_health = vObs.dSVhealth        # (MSB only)
        TGD = vObs.dTGD                   # (seconds)
        IODC_Issue_of_data = vObs.dIODC    # (Clock)
        # BroadcastOrbit - 7
        tr_time_of_message = vObs.dTransTime # Transmission time of message (sec of GPS week))
                                             # derived e. g. from Z-count in Hand Over Word
        n0 = np.sqrt(self.my/a**3)                # Computed mean motion - rad/sec
        # SV PRN code phase time offset
        diffTcl = (cObsTime - dtTocl).value * 86400
        # Delta SV PRN code phase time offset in seconds determined the first time without relativistic effects.
        delta_ts = a0 + a1*diffTcl + a2*diffTcl ** 2
        # Time from ephemeris reference epoch
        tk = (cObsTime - dtToe).value * 86400 - delta_ts
        # Corrected mean motion
        n = n0 + Delta_n
        # Mean anaomaly
        Mk = M0 + n * tk
        # Itteration to determine Kepler's equation for eccentric anomaly initial values
        Ek = Mk
        diff = 1
        while abs(diff) > 1.0e-13:
            diff = Mk - Ek + e*np.sin(Ek)
            Ek = Ek + diff
        # Run a second time to delta_ts where the relativistic effects are applied
        # Relativistic effects
        dTr = F * e * np.sqrt(a) * np.sin(Ek)
        # delta_ts with relativistic effects
        delta_ts = a0 + a1 * diffTcl + a2 * diffTcl**2 + dTr  # Delta SV PRN code phase time offset in seconds
                                                              # determined the first time without relativistic effects.
        # Time from ephemeris reference epoch
        tk = (cObsTime - dtToe).value * 86400 - delta_ts
        # Itteration to determine Kepler's equation for eccentric anomaly initial values
        diff=1;
        while abs(diff) > 1.0e-13:
            diff = Mk - Ek + e * np.sin(Ek)
            Ek = Ek + diff
        # True anomaly
        Cvk = (np.cos(Ek) - e)/(1 - e * np.cos(Ek))
        Svk = (np.sqrt(1 - e**2) * np.sin(Ek))/(1 - e * np.cos(Ek))
        fk=np.arctan2(Svk,Cvk)
        if fk < 0:
            fk = fk + 2 * np.pi
        # Argument of latituide
        fi_k = fk + omega
        # Second harmonic perturbations
        ra_uk = Cus * np.sin(2 * fi_k) + Cuc * np.cos(2 * fi_k);
        ra_rk = Crc * np.cos(2 * fi_k) + Crs * np.sin(2 * fi_k);
        ra_ik = Cic * np.cos(2 * fi_k) + Cis * np.sin(2 * fi_k);
        # Corrected argument of latitude
        uk = fi_k + ra_uk
        # Corrected radius
        rk = a * (1 - e * np.cos(Ek)) + ra_rk
        # Corrected inclination
        ik = i0 + ra_ik + IDOT * tk
        # Position in orbital plane
        xk = rk * np.cos(uk)
        yk = rk * np.sin(uk)
        # Corrected longitude of ascending node
        OMEGA_k = OMEGA + (OMEGA_DOT - self.OmegaDotE) * tk - self.OmegaDotE * Toe
        # Earth fixed coordinates
        x = xk * np.cos(OMEGA_k) - yk * np.cos(ik) * np.sin(OMEGA_k)
        y = xk * np.sin(OMEGA_k) + yk * np.cos(ik) * np.cos(OMEGA_k)
        z = yk * np.sin(ik)
        ds = delta_ts         
        
        return x,y,z,ds,TGD
        
    def weeksecondstoutc(self,gpsweek,gpsseconds,leapseconds = 0):
        import datetime
        datetimeformat = "%Y-%m-%d %H:%M:%S"
        epoch = datetime.datetime.strptime("1980-01-06 00:00:00",datetimeformat)
        elapsed = datetime.timedelta(days=(gpsweek*7),seconds=(gpsseconds+leapseconds))
        return datetime.datetime.strftime(epoch + elapsed,datetimeformat)
        
    def brdcRead(self, brdcData):
        '''
             This function reads broadcast ephemeris from a RINEX file
             and calculates the satellit position with the wanted intervall
            
             To call the function one writes:
            
                  [A, data] = ReadEphBro(A,sFileName,dInterval)
            
               A - CoordEph instance 
               data - EphData 
               sFileName - filename of the RINEX file
               dInterval - the time intervall

             The function is written by Amir Yeganehsahab
        '''
        __annotations__ = {'dLastEpoch' : list,
                           'dFirstEpoch' : list,
                           'FirstBroadcast': bool,
                           'prns' : list,
                           'prnData' : list,
                           'row' : list,
                           'idx' : int,
                           'dt' : datetime,
                           'dStart': datetime,
                           'dEnd' : datetime,
                           'TimeSpan' : datetime,
                           'dInterval' : datetime,
                           'N_interval' : int,
                           'epoch' : datetime,
                           'df' : list,
                           'i' : int,
                           'vXYZ' : list}
        # Find the first and last Epoch
        dLastEpoch ,dFirstEpoch = [], []  
        FirstBroadcast = 1  
        prns = np.unique(brdcData.iPRN)
        for prn in prns:
            prnData = brdcData.query('iPRN == {}'.format(prn))
           
            for idx, row in prnData.iterrows():
                dt = row.dateTime

                if FirstBroadcast:
                    dFirstEpoch = dt
                    dLastEpoch = dt
                    FirstBroadcast = 0
                elif (dt - dFirstEpoch) < 0:
                    dFirstEpoch = dt
                elif (dt - dLastEpoch) > 0:
                    dLastEpoch = dt
        # beginning iterval 3 hours earlier
        dStart = dFirstEpoch - self.ephOverLap 
        # last iterval 3 hours later
        dEnd = dLastEpoch + self.ephOverLap
        
        self.dStart = dStart
        self.dEnd = dEnd
        # time span (s)
        TimeSpan = np.round((dEnd.mjd - dStart.mjd) * 86400)
        # Number of intervals
        dInterval = np.round(self.dInterval.value * 86400)
        N_interval = int(np.floor(TimeSpan/dInterval))
        # Calculate satellite coordinates for each interval
        epoch = dStart
        df = pd.DataFrame(columns = ['prn','X','Y','Z','Dts','TGD'])
        
        for i in range(N_interval):
            
            vXYZ = self.beEphCoordCalc(brdcData, epoch)
            
            vXYZ['epoch'] = epoch
            
            df = df.append(vXYZ,ignore_index=True, sort = False)
            epoch += self.dInterval
        #df.to_html('df.html')
        return dStart, dEnd,df 

    def CompStdOrb(self,BEph : list, stTgd : list):
        '''
            CompStdOrb computes polynomial coefficients for all satellites available in precise
            ephemeris peEph
            so = CompStdOrb(so, pe)
            so - Standard orbit (class StdOrb)
            pe - Coordinate ephemeris (class CoordEph)
            stTgd = struct('vFateTime', dtTime, 'cTGD',0) - this structure is created by getTgd() function
            Coordinates for an epoch are computed by method GetSatCoord
        '''
        # extract x-coordinate for all satellites

        x = np.vstack(BEph.X.values)
        y = np.vstack(BEph.Y.values)
        z = np.vstack(BEph.Z.values)
        # epoch
        t = BEph.epoch
        # Clock corrections
        cl = np.vstack(BEph.Dts.values)
        # Satellite Numbers
        prn = np.vstack(BEph.prn.values)
        nprn = np.shape(prn)[1]
        # Number of Epochs
        ne = t.__len__()
        # First epoch, for which the coordinates are given
        tb = t[0].mjd * 86400
        # last epoch
        te = t[ne-1].mjd * 86400
        #lead-in and lead-out interval
        tm = (self.StandardOrbit['dFitInt'] - self.StandardOrbit['dInterval'])/2 
        #number of fit intervals
        Nint = int(np.floor((te - tb- 2*tm)/self.StandardOrbit['dInterval']))
        m = 0
        
        self.StandardOrbit['dTimeSet'] = [None for item in range(Nint)]
        self.StandardOrbit['dXCoef'] = np.zeros([nprn,Nint,self.StandardOrbit['nPolynomialCoeff']])
        self.StandardOrbit['dYCoef'] = np.zeros([nprn,Nint,self.StandardOrbit['nPolynomialCoeff']])
        self.StandardOrbit['dZCoef'] = np.zeros([nprn,Nint,self.StandardOrbit['nPolynomialCoeff']])
        
        self.StandardOrbit['dXmu'] = np.zeros([nprn,Nint,2])
        self.StandardOrbit['dYmu'] = np.zeros([nprn,Nint,2])
        self.StandardOrbit['dZmu'] = np.zeros([nprn,Nint,2])
        
        self.StandardOrbit['dTGD'] = np.zeros([nprn,Nint])
        
        for i in range(Nint):
            #time of start of interval
            self.StandardOrbit['dTimeSet'][i] = (Time((tb + tm + (i)*self.StandardOrbit['dInterval'])/86400, format = 'mjd', scale = 'utc'))
            #stTgd = BEph.TGD[0]
            tg = self.FindTGD(stTgd, self.StandardOrbit['dTimeSet'][i]);  #find value of Tgd closest to time so.dTimeSet(i) for all satellites
            tb_ = Time((self.StandardOrbit['dTimeSet'][i].value * 86400 - tm)/86400,format = 'mjd', scale = 'utc')
            [m, n] = self.FindInt(t, tb, self.StandardOrbit['dFitInt'], m) #find vector interval (indexes m,n) that corresponds to the fit interval 
            if n < 0 :    #it was not possible to find data for current interval
                self.StandardOrbit['dTimeSet'][i] = []
                break
            tt = (t[m:n+1] - self.StandardOrbit['dTimeSet'][i])  #reduce time to get better numerical stability
            tt = [(t_.value * 86400) for t_ in tt] # get the mjd of the time grid from datetime
            tt = [round(t_) for t_ in tt]
            for j in range(nprn) : #loop over satellites
                if prn[j][n] < 1:  #no data for satellite j
                    self.StandardOrbit['dXCoef'][j,i,:] =\
                      np.zeros(np.shape(self.StandardOrbit['dXCoef'])[2])   #placeholder for satellite
                    self.StandardOrbit['dYCoef'][j,i,:] =\
                     np.zeros(np.shape(self.StandardOrbit['dYCoef'])[2])
                    self.StandardOrbit['dZCoef'][j,i,:] =\
                      np.zeros(np.shape(self.StandardOrbit['dZCoef'])[2])
                    continue
                mu = [np.mean(tt), np.std(tt, ddof = 1)]
#                 t_hat = (tt-mu[0])/mu[1]
                coef,resids, rank, s, rcond = np.polyfit(tt, x[m:n+1,j], self.StandardOrbit['PolynomialOrder'], full = True)
                #_poly = poly(tt,x[m:n+1,j], self.StandardOrbit['PolynomialOrder'])
                #coef, S, mu = _poly.fit()
                self.StandardOrbit['dXCoef'][j][i] = coef
                self.StandardOrbit['dXmu'][j,i,:] =  mu
                
                coef,resids, rank, s, rcond  = np.polyfit(tt, y[m:n+1,j], self.StandardOrbit['PolynomialOrder'], full = True)
#                 _poly = poly(tt,y[m:n+1,j], self.StandardOrbit['PolynomialOrder'])
#                 coef, S, mu = _poly.fit()
                
                self.StandardOrbit['dYmu'][j,i,:] =  mu
                self.StandardOrbit['dYCoef'][j,i,:] =  coef
                
                coef,resids, rank, s, rcond  = np.polyfit(tt, z[m:n+1,j], self.StandardOrbit['PolynomialOrder'], full = True)
#                 _poly = poly(tt,z[m:n+1,j], self.StandardOrbit['PolynomialOrder'])
#                 coef, S, mu = _poly.fit()
#                 
                self.StandardOrbit['dZCoef'][j,i,:] =  coef
                self.StandardOrbit['dZmu'][j,i,:] =  mu
                
                self.StandardOrbit['dTGD'][j,i] = tg[j]

        #interval, for which the std. orbit is valid
        self.StandardOrbit['dTbeg'] = self.StandardOrbit['dTimeSet'][0] #begin
        self.StandardOrbit['dTend'] = \
        Time(self.StandardOrbit['dTimeSet'][-1:][0].value + self.StandardOrbit['dInterval']/86400, format = 'mjd', scale = 'utc')
        self.StandardOrbit['iPRN'] = prn
        self.StandardOrbit['dtClTime'] = t
        self.StandardOrbit['dClErr'] = cl
        
    def getTgd(self, sFileName):
        '''
        This function collect all the time group delays from a broadcast (TGD)
        navigation file
        
        Input:
        sFileName = file name broadcast navigation file
        
        TGD
        '''
        sz = np.zeros([10,32]) #allocate space for 32 satellites
        TGD = {'vFateTime' : [], 'cTGD' : sz} 
        fid= open(sFileName)
        # ----------------------------------------------------------
        rad=0 # Start value Counter
        num=0 # Start value Counter
        tline= fid.readline()
        z = [] # z is a vector with all the satellites in the file (see below)
        
        while num < 1: # Loop until END OF HEADER
            tline= fid.readline()
            if 'END OF HEADER' in tline:
                num = 1
        # ----------------------------------------------------------
        k = 0;
        while True: # Loop continues until the end of the file
            # PRN / EPOCH / SV CLK
            line = fid.readline()
            rad += 1 # Take a new line from the file
            #print(line)    
            if line[:2] == '': 
                break
            iPRN = int(line[:2])
            year = int(line[2:5])
            if year < 94: 
                year += 2000
            else: 
                year += 1900
            month,day = int(line[5:8]), int(line[8:11])
            Hour, Minute, Second_ = int(line[11:14]), int(line[14:18]), float(line[18:22])
            centisec = 0
            if Second_ != int(Second_):
                centisec = Second_ - int(Second_)
                Second = int(Second_)
            else:
                Second = int(Second_)
                
            epoch = Time(datetime(year,month,day,Hour,Minute,Second, centisec))
                  
            epoch0 = Time(datetime(year, month, day, 0, 0, 0))
            # New day
            if (TGD['vFateTime']) == []:
                TGD['vFateTime'] = epoch
            elif  (epoch - epoch0) >= 86400 : 
                TGD['vFateTime'].ppend(epoch)
                k +=1
                
            for i in range(1,7):
                tline= fid.readline()
                rad=rad+1
        
            TGD['cTGD'][k,iPRN-1]=float(tline[41:60])
            
            tline= fid.readline()
        fid.close()
        '''
        fid1 = open('TGD.txt','w');
        
        fid1.write('TGD data from file :{}\n\n The data covers {} days\n\n',sFileName,k)
        
        for j in range(1,k):
            fid.write('Year-month-day\n')
            fid.write('{}-{}-{} \n\n',year,month,day)
            fid.write('iPRN    TGD \n\n')
            for i in range(1,len(TGD.cTGD)):
                if TGD.cTGD[i] != 0:
                    fid1.write('{}     {}\n',i,TGD.cTGD(i,j) );
        fid1.close()
        '''
        return TGD
    
    def FindInt(self, t, tb, Interval, m):
        '''
            find vector interval (indexes m,n) that corresponds to the fit interval 
            t - vector of epochs (time given in JD)
            tb - time of beginning
            Interval - duration of the interval in JD
            m - index of vector t that corresponds to the beginning of the interval
        '''
        n = -1;
        te = tb + Interval;  # time of end of interval
        for i in range (m,len(t)):
            if (t[i].mjd*86400 - tb) <= 0 :  
                m = i
            if (t[i].mjd*86400 - te) >= 0 : 
                n = i
                return m ,n 

    def FindTGD(self, stTgd, ep):

        # Finds value of group delay (Tgd) closest to epoch ep

        ind = self.FindEn(stTgd['vFateTime'], ep)
        if ind < 0 : 
            ep
            raise ValueError('Could not find any Tgd for given epoch')

        return stTgd['cTGD'][ind,:]  #vector of Tgd for all matrixes
    
    def FindEn(self, vt, t):
        '''
            FindEn finds interval number of epoch t in the vector vt
            vt - vector of epochs (time given in days [Time class]) 
            t - given epoch in [Time class], Unit : day
            en - index of vt, where t falls 
        '''
        en = -1
        try:
            lvt = len(vt)
        except:
            lvt = 1
            
        if lvt < 1 : return en
        if lvt == 1 :
            en = 0
            return en
        interv = (vt[1] - vt[0]) # unit : day
        try:
            vt.append(vt[-1] + interv) # unit : day
        except:
            vt = vt.values.tolist()
            vt.append(vt[-1] + interv)
        for i in range (1,len(vt)) :
            if  (vt[i] - t) >= 0:
                en = i-1
                return en
        
    def getGPSSatParam(self, t : Time,x : list,sv_no : list,recClcBias : float)-> list:
        '''
             FUNCTION
               Computes the GPS position and GPS satellite clock error at
               signal transmission time via  light time iteration
             INPUTS
               epoch : epoch number
               t     : receiver date and time, (astropy.Time class with mjd format in utc scale)
               x     : receiver position vector
               sv_no : satellite vehicle number
               recClcBias : receiver clock bias
             OUTPUTS
               GPS_pos     : GPS positions for given satellites, [m]
               GPSclc_corr : GPS clock corrections for given satellites, [m]
               GPS_Tgd     : Instrumental delays for given satellites, [m]
        '''
        #print(t.iso)
        epo = Time(t.mjd - (recClcBias/self.C)/86400, format = 'mjd', scale = 'utc')
        if self.current_t == 0 or np.floor(self.current_t.value) !=  np.floor(epo.value):
            self.loadObsFile(epo)
        # Compute GPS satellite coordinates using light time iteration
        tau0 = 0.072 * np.ones(len(sv_no)) # seconds
        omega = self.OmegaDotE * tau0
        epo_trans = np.zeros(len(sv_no))
        
        positions = np.zeros([3,len(sv_no)])
        clockCorrections = np.zeros_like(sv_no)
        TimeGroupDelays = np.zeros_like(sv_no)
        for idx,prn in enumerate(sv_no):
            d_p = 1
            while d_p > 0.0001:
                epo_trans = Time((epo.value*86400 - tau0[idx])/86400, format = 'mjd', scale = 'utc')
                # Get GPS sat Coords
                X,Y,Z,clockCorr,Tgd = self.GetSatCoord(self.StandardOrbit,prn,epo_trans)
                # Earth Rotation Correction
                R3 = [[np.cos(omega[idx]), np.sin(omega[idx]), 0],
                      [-np.sin(omega[idx]), np.cos(omega[idx]), 0],
                      [0, 0, 1]]
                pos = np.dot(R3 , [X,Y,Z])
                # Geometric Range
                P = np.sqrt((pos[0] - x[0])**2 +\
                            (pos[1] - x[1])**2 +\
                            (pos[2] - x[2])**2)
                # Time delay
                tau = (P/self.C)
                d_p = abs(self.C * (tau - tau0[idx]))
                tau0[idx] = tau
#             positions[idx] = pos
            clockCorrections[idx] = clockCorr * self.C
            TimeGroupDelays[idx]  = Tgd * self.C
            positions[0:3,idx] = pos
        return {'pos':positions, 'clockCorrections': clockCorrections, 'TimeGroupDelays': TimeGroupDelays, 'prns':sv_no}
             
    def loadObsFile(self, t):
        '''
            Loads the next broadcast observation file  
        '''
        # load header of brdc file
        self.Header()
        # load body of brdc file
        brdcData = self.brdcLoad()
        # calculate the satellit position with the wanted intervall
        dStart, dEnd,BEph = self.brdcRead(brdcData)
        # Read Group delays
        stTgd = self.getTgd(path)
        # compute standard orbit
        self.CompStdOrb(BEph, stTgd)
        self.current_t = t
        
    def GetSatCoord(self, std : list, prn : list, t : Time):
        '''
            GetSatCoord - computes satellite's coordinates and clock correction for a
            given epoch, using standard ephemeris
            ret = GetSatCoord(std, prn, t)
            std - standard orbit in polynom form (class StdOrb) created by CompStdOrb
            prn - satellite number
            t - eopch in [Date_Time]
        '''
        #print(t.iso, prn)
        if (t - std['dTbeg']).value < 0  or (t - std['dTend']).value > 0:
            raise ValueError('Given epoch : "{} mjd" is outside of the standard ephemeris'.format(t))
        en = self.FindEn(std['dTimeSet'], t)  # Finds epoch number en
        if en < 0:
            raise ValueError('Should not be here: something is wrong in findEn for epoch : "{} mjd"'.format(t))
        
        ent = self.FindEn(std['dtClTime'], t)
        if ent < 0:
            raise ValueError('Should not be here: something is wrong in findEn finding dtClTime for epoch : "{} mjd"'.format(t))
        
        Tgd = std['dTGD'][prn-1, en]

        coefX = std['dXCoef'][prn-1, en, :]

#             if abs(coefX[-1]) < 1e-12:
#                 raise ValueError('No data for given prn : {}'.format(prn))
        coefY = std['dYCoef'][prn-1, en, :]
        coefZ = std['dZCoef'][prn-1, en, :]
        
        Xmu = std['dXmu'][prn-1, en, :]
        Ymu = std['dYmu'][prn-1, en, :]
        Zmu = std['dZmu'][prn-1, en, :]

        tt = (t.mjd - std['dTimeSet'][en].mjd)*86400
        #t_hat = (tt - Xmu[0])/Xmu[1]
        
        x = np.polyval(coefX, tt)
        y = np.polyval(coefY, tt)
        z = np.polyval(coefZ, tt)
         
#         coefVX = coefX[:-1]#delete the last coefficient (first derivative = 0)
#         coefVY = coefY[:-1]
#         coefVZ = coefZ[:-1]
#         
#         n = len(coefVX)
#         for idx, coef in enumerate(coefVX):
#             multiplier = (n-(idx+1)+1)
#             coefVX[idx] = coef * multiplier
#             coefVY[idx] = coefVY[idx] * multiplier
#             coefVZ[idx] = coefVZ[idx] * multiplier
#         t_hat = (tt - Xmu[0])/Xmu[1]
#         vx = np.polyval(coefVX, t_hat)
#         t_hat = (tt - Ymu[0])/Ymu[1]
#         vy = np.polyval(coefVY, t_hat)
#         t_hat = (tt - Ymu[0])/Ymu[1]
#         vz = np.polyval(coefVZ, t_hat)
        
        targ = (std['dtClTime'][ent:ent+2] - std['dtClTime'][ent])._values
        targ[0].format = 'sec' 
        targ[0] = targ[0].value
        targ[1].format = 'sec'
        targ[1] = targ[1].value
        targ = np.array(list(targ), dtype=np.float)
        #mu = [np.mean(targ), np.std(targ, ddof = 1)]
        #t_hat = (targ-mu[0])/mu[1]
        coef = np.polyfit( targ,std['dClErr'][ent:ent+2,prn-1], 1)
        
        tt = t - std['dtClTime'][ent]
        tt.format = 'sec'
        dt = np.polyval(coef, tt.value)
        return x,y,z,dt,Tgd 
    
    def Kinematic(self, t, z, sv_no, fetch = 'InitialState', recClcDrift = False):
        '''            
         FUNCTION
           Computes position, velocity and receiver clock bias
         INPUTS
           t    : date and time, such as [year month day hour minute second] 
           z    : pseudo code observation
           sv_no: vehicle number of GPS satellites
         OUTPUTS 
          x     : vector including estimated position and receiver clock 
                  correction, such ad;    x=[x y z clc_rec]
        '''
        if recClcDrift:
            x = np.zeros(6)
        else:
            x = np.zeros(4)
        output = {}
        dx = 1
        while np.linalg.norm(dx) > 0.001:
            GPS = self.getGPSSatParam(t,x[0:3],sv_no,x[3])
            # geomaetric distance
            zg = np.sqrt((GPS['pos'][0,:] - x[0])**2 +\
                         (GPS['pos'][1,:] - x[1])**2 +\
                         (GPS['pos'][2,:] - x[2])**2)
            # measurement partials
            H = np.zeros([len(z),len(x)])
            for j,z_ in enumerate(z):
                H[j,0] = -(GPS['pos'][0,j] - x[0])/zg[j]
                H[j,1] = -(GPS['pos'][1,j] - x[1])/zg[j]
                H[j,2] = -(GPS['pos'][2,j] - x[2])/zg[j]
                H[j,3] = 1
                if recClcDrift:H[j,4],H[j,5] = 1,1
            if recClcDrift:
                zc = zg + x[3] + x[4] + x[5] - GPS['clockCorrections'] # computed range
            else:
                zc = zg + x[3] - GPS['clockCorrections'] # computed range               
            # Least Square Estimation
            dz = (z - zc)
            
            dx , residuals, rank, singularvals = np.linalg.lstsq(H, dz,rcond=None)
            x = x + dx
        return {'pos' : GPS['pos'], 'clockCorrections' : GPS['clockCorrections'], 'prns': sv_no},\
            {'leoPos': x, 'prns':sv_no}
      
    def KinematicLoop(self, interval, nSat, ax, rnx, beginTime, endTime, plot = False, systemInfo = {}, initializeState = True):
        prnLats = {prn:[] for prn in range(1,nSat)}
        prnLons = {prn:[] for prn in range(1,nSat)} #prnLats.copy()
        prnAlts = {prn:[] for prn in range(1,nSat)} #prnLats.copy()
        epochNo = 0
        try:
            Nepochs = np.int((endTime.mjd - beginTime.mjd))*86400/interval
        except:
            Nepochs = ((endTime.mjd - beginTime.mjd))*86400/interval
        if initializeState: Nepochs = 3
        cursor = []
        while True:
            print(epochNo)
            
            Rinexdata = rnx.rnxLoad()
            if Rinexdata is None: break # end of the file
            if epochNo > Nepochs: break # end the loop when process time limit is satisfied
            if Rinexdata['mjd'] > endTime: break # end the loop when process time limit is satisfied
            if Rinexdata['mjd'] < beginTime:
                continue
            else:
                cursor.append(rnx.cursor)
                epochNo += 1
             
            GPS, Leo = self.Kinematic(Rinexdata['mjd'], Rinexdata['C1'], Rinexdata['prns'], recClcDrift = True)
            systemInfo[Rinexdata['mjd'].iso] = {'gps':GPS, 'leo':Leo}
            leo = Leo['leoPos'][0:3]
            
            ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
            lla = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')
            leoLong, leoLat, leoAlt = pyproj.transform(ecef, lla, leo[0], leo[1], leo[2], radians=True)
            prns = Rinexdata['prns']
            gps = GPS['pos']
            elevation, azimuth, azimuth_ = np.zeros_like(prns), np.zeros_like(prns), np.zeros_like(prns)
            #gpsLong, gpsLat, gpsAlt = np.zeros_like(prns), np.zeros_like(prns), np.zeros_like(prns)
    
            allGps = {}
            for idx, prn in enumerate(prns):
                gpsLong, gpsLat, gpsAlt = pyproj.transform(ecef, lla, gps[0][idx], gps[1][idx], gps[2][idx], radians=True)
                prnLons[prn].append(np.rad2deg(gpsLong))
                prnLats[prn].append(np.rad2deg(gpsLat))
                prnAlts[prn].append(np.rad2deg(gpsAlt))
    
                G = gpsLong - leoLong
                #Rearath = 6371000
                #num = np.cos(G)*np.cos(leoAlt)- (Rearath + leoAlt)/(Rearath + gpsAlt)
                #denum = np.sqrt(1 - np.cos(G)**2*np.cos(leoLat))
                 #elevation[idx] = (2* np.pi + (np.arctan(num/denum)))
                # θ = np.arctan2 [(sin Δλ ⋅ cos φ₂), (cos φ₁ ⋅ sin φ₂ − sin φ₁ ⋅ cos φ₂ ⋅ cos Δλ)]
                azimuth[idx] = (np.arctan2(np.sin(G) * np.cos(gpsLat), \
                                           np.cos(leoLat) * np.sin(gpsLat) - \
                                           np.sin(leoLat) * np.cos(gpsLat) * np.cos(G)))
                del G
            if plot:       
                ax = plt.subplot(221,projection = 'polar')
                Snr = Rinexdata['S1']
                colors = [int(i % 23) for i in Snr]
                ax.scatter(azimuth,Rinexdata['C1'], c = colors, s=300)
            
                for i,prn in enumerate(prns):
                    ax.text(azimuth[i], Rinexdata['C1'][i],prn, fontsize = 9 ,color = 'w')
    
                proj = ["lambert", "aitoff", "hammer", "mollweide"]
        
                #fig = plt.subplot(223, projection = proj[3])
                
                ax = plt.subplot(2, 2, 3, projection=ccrs.PlateCarree())
                for prn in range(1,nSat):
                    lon = prnLons[prn]
                    lat = prnLats[prn]
                    if lon != []:
                        ax.plot(lon, lat, '.')
                ax.plot(np.rad2deg(leoLong), np.rad2deg(leoLat), '*')
                ax.stock_img()
                ax.coastlines()
                        
                plt.subplot(222)        
                rects0 = plt.bar(np.array(prns)-0.5,Rinexdata['S1'], width = 0.5)
                rnx.autolabel(rects0,showprns = False)
                  
                rects1 = plt.bar( np.array(prns),Rinexdata['S2'], width = 0.5)
                rnx.autolabel(rects1)
                  
                plt.legend(rnx.SNRs,loc=2,framealpha = 0.5)
                  
                plt.xticks(range(32),color = 'w')
                  
                #ax.set_xticks(prns)
                plt.show()
                plt.pause(0.0001)
                plt.clf()
        return systemInfo, cursor

    def getInitialState(self, data, cursor):
        epo, dt, leo = [], [], []
        for idx, epoch in enumerate(data.keys()):
            epo.append(Time(epoch))
            leo.append(data[epoch]['leo']['leoPos'][:3])
            if idx == 1:
                gpsPos = data[epoch]['gps']['pos']
                clockCorrections = data[epoch]['gps']['clockCorrections']
                prns = data[epoch]['leo']['prns']
                cursor = cursor[idx]
        for idx, t in  enumerate(epo):
            try:
                dt.append((t-epo[0]).value * 86400)
            except: 
                pass
        a = np.dot(leo[0],(2* dt[1]-dt[1]-dt[2])/((dt[0]-dt[1])*(dt[0]-dt[2])))
        b = np.dot(leo[1],(2* dt[1]-dt[0]-dt[2])/((dt[1]-dt[0])*(dt[1]-dt[2])))
        c = np.dot(leo[2],(2* dt[1]-dt[0]-dt[1])/((dt[2]-dt[0])*(dt[2]-dt[1])))
        
        dx_dt = a + b + c #dx_dt
        return {'epoch':epo[1],\
                'position':leo[1],\
                'velocity':dx_dt,\
                'gps': gpsPos,\
                'clockCorrections': clockCorrections,\
                'prns': prns}, cursor

        
        
if __name__ == '__main__':
    
    InPath = '/home/geomatics/Dropbox/Sample_Data/'       #|
    OutPath = '/home/geomatics/Documents/workspace/.I-O/' #|
    #FileName = 'cham0140.06o'                             #|
    FileName = '2010_1.rnx'                             #|
    
    path = InPath+FileName
    f_rnx = open(path,'r')
    rnx = Read(f_rnx,'rinex')
    rnx.Header()

    FileName = 'brdc10.10n'                             #|
    
    path = InPath+FileName
    f_brdc = open(path,'r')
    # brdc Class
    brdc = Read(f_brdc,'brdc')
    beginTime = Time(datetime(2010,1,1,0,0,20))
    endTime = Time(datetime(2010,1,1,12,0,0))
    interval = 10 #sec
    
    plot = False
    if plot:
        plt.ion()
        fig, ax = plt.subplots()
    else:
        ax = None
    nSat = 35
    SystemInfo, cursor = brdc.KinematicLoop(interval, nSat, ax, rnx, beginTime, endTime, plot = plot, initializeState = True)
    InitialSatate, cursor = brdc.getInitialState(SystemInfo, cursor)
    print('done')
    