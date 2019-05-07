#!/usr/bin/python
import tkinter as tk

class AppWindow(tk.Tk):

    def __init__(self):

        tk.Tk.__init__(self)
        main_window = tk.Frame(self)

        self.title("PizzaDex")
        main_window.pack(fill = "both", expand = True)

        # main_window.grid_rowconfigure(0, weight = 1)
        # main_window.grid_columnconfigure(0, weight = 1)

        self.frames = {}

        main_frame = MainWindow(main_window, self)
        self.frames[MainWindow] = main_frame
        question_frame = QuestionWindow(main_window, self)
        self.frames[QuestionWindow] = question_frame

        main_frame.grid(row = 0, column = 0, sticky="nsew")
        main_frame.grid_propagate(False)
        question_frame.grid(row = 0, column = 0, sticky="nsew")
        question_frame.grid_propagate(False)
        self.show_frame(MainWindow)

    def show_frame(self, frame):
        selected = self.frames[frame]
        selected.tkraise()


class MainWindow(tk.Frame):

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master, height=800, width=450)
        intro = tk.Label(self, text = "Register new entry:")
        intro.grid(padx = 10, pady = 10, sticky = "nsew")

        button = tk.Button(self, text = " REGISTER NEW ",
                            command = lambda: controller.show_frame(QuestionWindow))
        button.grid(row = 1, sticky="ns")


class QuestionWindow(tk.Frame):

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master, height=800, width=450)
        text = tk.Label(self, text = "What kind of crust does the entry have?")
        text.grid(padx = 10, pady = 10, sticky = "nsew")

        button = tk.Button(self, text = " * Unjerk * ",
                            command = lambda: controller.show_frame(MainWindow))
        button.grid(row = 1, sticky="ns")

        TEST_OPTIONS = [
            ("Thin", "thin"),
            ("Thicc", "thicc")
        ]
        TEST_VAR = tk.StringVar()

        # self.show_answers(TEST_OPTIONS, TEST_VAR)

    def show_answers(self, options, var):
        for option, value in options:
            b = tk.Radiobutton(self, text = option, variable = var, value = value, anchor=tk.W)
            b.grid(sticky="ew")




app = AppWindow()
app.mainloop()
