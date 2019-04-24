#!/usr/bin/python
import tkinter as tk

root = tk.Tk()

sideFrame = tk.Frame(root)
canvasFrame = tk.Frame(root)
bottomFrame = tk.Frame(root)
sideFrame.pack(side=tk.LEFT, expand=0)
canvasFrame.pack(side=tk.RIGHT,expand=1, fill=tk.BOTH)
bottomFrame.pack(side=tk.BOTTOM, expand=0, fill=tk.Y)

button = tk.Button(sideFrame, text="LFC", fg="red")
button.pack()

label = tk.Label(bottomFrame, fg="red", text= "Follied once more! I was merely pretending to be retarded.")
label.pack(fill=tk.X)
# canvas = tk.Canvas(top, height=900, width=1600, bg="white")
# button.pack()
# canvas.pack()

canvas = tk.Canvas(canvasFrame, bg="white")
canvas.pack(fill=tk.BOTH)

#
# window = PanedWindow(top, bg="e6dfdd", height=750, width=1334)
# window.pack(fill=BOTH, expand=True)
#
# area = Canvas(window, bg="white")
# window.add(area)

root.mainloop()
