'''
Created on Feb 14, 2019

@author: gravity
'''
from tkinter import *
import os

root = Tk()
termf = Frame(root, height=400, width=500)

termf.pack(fill=BOTH, expand=YES)
wid = termf.winfo_id()
os.system('xterm -into %d -geometry 200x100 -bg "#300A24" -sb &' % wid)

root.mainloop()