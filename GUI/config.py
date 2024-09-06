'''
Created on Jan 27, 2019

@author: root
'''
# initial strings ===========================================================================
WorkspaceDirs = ['.Constants','.I-O','.I-O/inputs','.I-O/outputs','.I-O/logs']
# Configs = ['mathConstants','physConstants','astroConstants','process','GNSS','LEO', 'DefaultValues']
Configs = ['DefaultValues']
filteType = ['Kalman_Filter', 'Extended_Kalman_Filter','Unscented_Kalman_Filter', 'Particle_Filter', 'Neural_Networks']
obsType = ['Code', 'Phase', 'Navsol', 'Graphic', 'IonosphereFree_Code', 'IonosphereFree_Pahase', 'IonosphereFree_Combined', 'Hybrid']
processor = ['Single Core','Dual Core', 'Multi-Core']
dynamicMod = ['None', 'Atmospher-Drag-SolarP','Atmospher-Drag-SolarP-EmpiricalAcc','Atmospher-Drag-SolarP-EmpiricalAcc_MarkovProcess']
pathes = ['rinex','brdc','peph','jpl','eop','almanac','gravity', 'tle','workspace']
dataeditingmode = ['Recursive_Outlier_Detection', 'Outlier_Detection_for_RUKF', 'Adaptive_Robust']
dataEditing = {}
inputDirs = {}
settings = {}
currentDT = []
path2consts = []
logs = []
DefaultValues = {}
master = []
recentWorkspace = ['']
#initial values =============================================================================
dynamicForces = {}
satConsts = {}
garvityOrder = {}
timeSystems = {}
PropagationConsts = {}
measuremnetInits = {}
processNoise = {}
#Default values =============================================================================
enableSaveFilterOutput={}
permanentWorkspace = None
OntheFly = ''
Mainpath = ''
# Loop variables (refresh before each loop (variable = [])===================================
entries = []
buttons = []
labels = []
password = []
rnxcmpPath = []
tempPath = []
terminal = []