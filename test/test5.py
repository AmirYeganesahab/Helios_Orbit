import tkinter as tk

root = tk.Tk()

pw = tk.PanedWindow(root)
pw.pack(fill="both", expand=True)

f1 = tk.Frame(width=200, height=200, background="bisque")
f2 = tk.Frame(width=200, height=200, background="pink")

pw.add(f1)
pw.add(f2)

# adding some widgets to the left...
text = tk.Text(f1, height=20, width=20, wrap="none")
ysb = tk.Scrollbar(f1, orient="vertical", command=text.yview)
xsb = tk.Scrollbar(f1, orient="horizontal", command=text.xview)
text.configure(yscrollcommand=ysb.set, xscrollcommand=xsb.set)

f1.grid_rowconfigure(0, weight=1)
f1.grid_columnconfigure(0, weight=1)

xsb.grid(row=1, column=0, sticky="ew")
ysb.grid(row=0, column=1, sticky="ns")
text.grid(row=0, column=0, sticky="nsew")

# and to the right...
b1 = tk.Button(f2, text="Click me!")
s1 = tk.Scale(f2, from_=1, to=20, orient="horizontal")

b1.pack(side="top", fill="x")
s1.pack(side="top", fill="x")

root.mainloop()