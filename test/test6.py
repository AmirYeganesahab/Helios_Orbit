from tkinter import *
from tkinter import ttk
m1 = ttk.PanedWindow(orient=VERTICAL)
m1.pack(fill=BOTH, expand=1)

left = ttk.Label(m1, text="left pane")
m1.add(left)

m2 = ttk.PanedWindow(m1, orient=VERTICAL)
m1.add(m2)

top = ttk.Label(m2, text="top pane")
m2.add(top)

bottom = ttk.Label(m2, text="bottom pane")
m2.add(bottom)

mainloop()