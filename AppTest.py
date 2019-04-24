#!/usr/bin/python
import tkinter as tk

class mainWindow(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        master.title("GraphyBoy")
        self.init_window()

    def init_window(self):
        self.pack(fill=tk.BOTH, expand=1)

        self.testLabel = tk.Label(self, text="Skidaddle skidoodle your dick is now a noodle.")
        self.testLabel.grid(columnspan=3, sticky=tk.E+tk.W)

        self.quitButton = tk.Button(self, text="Nope", command=self.print_bullshit())
        self.quitButton.grid(row=1, columnspan=3, sticky=tk.E+tk.W)

    def print_bullshit(self):
        print("Bullshit !")

root = tk.Tk()
root.geometry("800x450")

app = mainWindow(root)
root.mainloop()
