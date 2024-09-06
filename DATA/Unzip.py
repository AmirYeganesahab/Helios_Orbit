import os
import georinex
path0 = '/home/geomatics/Documents/test/.I-O/inputs/'
ws = '/home/geomatics/Documents/test/'
zipname = 'cham0050.08d.Z'
destname = zipname[:-2]
path = path0 + zipname
dest = path0 + destname
backupDir = path0 + 'rawData/'
# ================== Backup data ==================
os.system('mkdir '+backupDir)
os.system('cp ' + path + ' ' + backupDir)
os.system('uncompress ' + path + ' ' + dest)
# rnxcpmPath = '/home/geomatics/Dropbox/eclipse-workspace/OTK/GNSS/georinex/rnxcmp/'
# os.system('make {}install -C rnxcmp'.format(rnxcpmPath))
tempPath = ws + '.I-O/' + 'temp.tmp'
os.system('whereis crx2rnx > ' + tempPath)
with open(tempPath) as fp0:
    rnxcmp = fp0.read().split()[1]
    fp0.close()
os.system('/home/geomatics/.local/bin/crx2rnx -h')
# os.system('echo {}|sudo -S {} {}'.format('geomatics1985', output , dest))
from georinex import *
os.system('{} {}'.format(rnxcmp , dest))
obs = georinex.load("/home/geomatics/Documents/test/.I-O/inputs/cham0050.08o")
os.system('ReadRinex "/home/geomatics/Documents/test/.I-O/inputs/cham0050.08o"')