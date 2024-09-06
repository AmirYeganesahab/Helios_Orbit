from tkinter import *
import os
 
root = Tk()

termf = Frame(root, height=200, width=200, bg = 'white')
txt = Text(termf, height=140, width=200, bg = 'white')
e = Entry(termf, width=200)
termf.pack(fill=BOTH, expand=YES)
e.pack(fill=X, expand=YES, ipady=3)
txt.pack(fill = BOTH, expand = YES)
wid = termf.winfo_id()
os.system('xterm -into %d -geometry 400x200 -e /root/.bashrc&' % wid)
 
root.mainloop()