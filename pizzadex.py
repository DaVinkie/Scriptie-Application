#!/usr/bin/python
import tkinter as tk

class AppWindow(tk.Tk):

    def __init__(self):

        tk.Tk.__init__(self)
        self.title("PizzaDex - DEV")
        self.geometry("450x800")

        main_window = tk.Frame(self)
        main_window.grid(sticky="nsew")

        label = tk.Label(self, text="HOI")
        label.grid()

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
        tk.Frame.__init__(self, master)

        intro = tk.Label(self, text = "Register new entry:")
        intro.grid(padx=5, pady=5, sticky="nsew")

        button = tk.Button(self, text = "NIEUWE BEVINDING",
                            command = lambda: controller.show_frame(QuestionWindow))
        button.place(relx = 0.5, rely=0.5, anchor=tk.CENTER)


class QuestionWindow(tk.Frame):

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)

        questionframe = tk.Frame(self, height=600, width=440, bg="white",
                                    bd=1, relief=tk.SOLID)
        questionframe.grid(padx=5, pady=5, row=0, column=0, sticky="nsew")
        questionframe.grid_propagate(False)

        question = tk.Message(questionframe, width=430, text = qs["soort"])
        question.grid(padx=5, pady=5, sticky = "nsew")
        #
        # button = tk.Button(self, text = " * Unjerk * ",
        #                     command = lambda: controller.show_frame(MainWindow))
        # button.grid(row = 1, sticky="ns")
        #
        # TEST_OPTIONS = [
        #     ("Thin", "thin"),
        #     ("Thicc", "thicc")
        # ]
        # TEST_VAR = tk.StringVar()
        #
        # self.show_answers(TEST_OPTIONS, TEST_VAR)

    def show_answers(self, options, var):
        for option, value in options:
            b = tk.Radiobutton(self, text = option, variable = var, value = value, anchor=tk.W)
            b.grid(sticky="ew")


soort_q = "Tot welke pizzasoort behoort deze pizza?"
saus_q = "Wat voor saus zit er op deze pizzasoort?"
bodem_q = "Op wat voor bodem zit deze saus?"

qs = {
    "soort": soort_q,
    "saus" : saus_q,
    "bodem": bodem_q
}



app = AppWindow()
app.mainloop()
