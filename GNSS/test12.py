'''
Created on Mar 1, 2019

@author: geomatics
'''
#!/usr/bin/env python3
import FileReaders2
#from SatWare_v017.GNSS import FileReaders2
Read = FileReaders2.Read

InPath = '/home/geomatics/Dropbox/Sample_Data/'       #|
OutPath = '/home/geomatics/Documents/workspace/.I-O/' #|
FileName = 'cham0140.06o'                             #|

path = InPath+FileName
f_rnx = open(path,'r')
rnx = Read(f_rnx,'rinex')
rnx.Header()

FileName = 'brdc0140.06n'                             #|
path = InPath+FileName
f_brdc = open(path,'r')

brdc = Read(f_brdc,'brdc')
brdc.Header()
brdcData = brdc.brdcLoad()
brdc.brdcRead(brdcData)
    