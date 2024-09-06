# import config
# import numpy as np
# Configs = ['mathConstants','physConstants','astroConstants','process','GNSS','LEO']
# fname = 'mathConstants'
# 
# val = {}
# discription = {}
# # with open(config.inputDirs['workspace'].get()+'/.Constants/'+fname+'.conf', 'rb') as fp0:
# for fname in Configs:
#     with open('/home/geomatics/Documents/workspace'+'/.Constants/'+fname+'.conf','rb') as fp0:
#         for line in fp0:
#             if len(line)==1: continue
#             else:
#                 if line[0]=='#': 
#                     line_ = line[1:]
#                     print(line_)
#                 else: 
#                     line = str.split(line)
#                     print(line)
#                     val[line[0]] = np.double(line[2]) 
#                     discription[line[0]] = line_
#     Defaults = { fname: { 'val':val , 'discription': discription } }
#     fp0.close()
