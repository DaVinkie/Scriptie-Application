#!/usr/bin/python
import tkinter as tk
import pandas as pd

# Geraamte van de applicatie
class AppWindow(tk.Tk):

    def __init__(self):

        tk.Tk.__init__(self)
        self.title("LinneausDex - DEV")
        self.geometry("450x800")

        main_window = tk.Frame(self, width=450)
        main_window.grid(sticky="nsew")

        # pages = ["Classificeer", "Vergelijk", "Modelleer", "Verbeter"]
        self.frames = {}
        # in een pages loop
        main_frame = MainWindow(main_window, self)
        self.frames[MainWindow] = main_frame
        question_frame = QuestionWindow(main_window, self)
        self.frames[QuestionWindow] = question_frame

        main_frame.grid(row = 0, column = 0, sticky="nsew")
        question_frame.grid(row = 0, column = 0, sticky="nsew")
        # main_frame.grid_propagate(False) // Heeft geen size dus werkt niet
        # question_frame.grid_propagate(False)

        self.show_frame(MainWindow)

    def show_frame(self, frame):
        selected = self.frames[frame]
        selected.tkraise()

# Hoofdscherm / Hoofdmenu
class MainWindow(tk.Frame):

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)

        # QuestionWindow vervangen door correcte waarde
        pages = [
            ("Classificeer", "DarkSlategray2", QuestionWindow),
            ("Vergelijk", "khaki2", QuestionWindow),
            ("Modelleer", "light pink", QuestionWindow),
            ("Verbeter", "firebrick1", QuestionWindow)
        ]

        frames = []
        for i in range(4):
            f = tk.Frame(self, height=215, width=215)
            f.pack_propagate(False)
            frames.append(f)

        for i in range(len(frames)):
            b = tk.Button(frames[i], text=pages[i][0], bg=pages[i][1],
                            command = lambda: controller.show_frame(pages[i][2]))
            b.pack(expand=True, fill=tk.BOTH)

        # Misschien in een loop.
        frames[0].grid(row=0, column=0, padx=5, pady=5)
        frames[1].grid(row=0, column=1, padx=5, pady=5)
        frames[2].grid(row=1, column=0, padx=5, pady=5)
        frames[3].grid(row=1, column=1, padx=5, pady=5)

# Voor het classificatie gedeelte
class QuestionWindow(tk.Frame):

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)

        ranklist = ["soort", "familie", "orde", "klasse", "stam", "rijk"]

        soort_q = "Wat is de Nederlandse naam van de soort die je wilt classificeren?"
        familie_q = "Wat is de naam van de familie waar deze soort toe behoort?"
        orde_q = "Wat is de naam van de orde waar deze familie toe behoort?"

        QUESTIONS = {
            "soort": soort_q,
            "familie" : familie_q,
            "orde": orde_q
        }

        PARENTS = {
            "start": "soort",
            "soort": "familie",
            "familie": "orde",
            "orde": "klasse",
            "klasse": "stam",
            "stam": "rijk"
        }

        soort_data = pd.read_excel(r'data\Soort.xlsx')
        familie_data = pd.read_excel(r'data\Familie.xlsx')
        soort_df = pd.DataFrame(soort_data)
        familie_df = pd.DataFrame(familie_data)
        # Soort: ID, Familie_ID, Naam_NL, Naam_LA
        # Familie: ID, Orde_ID, Naam_NL, Naam_LA
        # print(soort_data[soort_data['Naam_NL'].notnull()])

        questionframe = tk.Frame(self, height=600, width=440, bg="white",
                                    bd=1, relief=tk.SOLID)
        questionframe.grid(padx=5, pady=5, row=0, column=0, sticky="nsew")
        questionframe.grid_propagate(False)
        question = tk.Message(questionframe, width=430, bg="white")
        question.grid(sticky="nsew")
        rank = PARENTS["start"]
        self.update_question(question, QUESTIONS, rank, PARENTS)

        # ans = tk.IntVar()
        ans = tk.StringVar()

        field = tk.Entry(self, textvariable = ans)
        field.grid(padx=5, pady=5, sticky = "nsew")

        s = tk.Button(self, text="submit",
            command = lambda: self.update_question(question, QUESTIONS, PARENTS[rank], PARENTS))
        s.grid(sticky="nsew")

        print(self.retrieve_answer(soort_df, familie_df, "Bosmuis"))

        button = tk.Button(self, text = " Home ",
                            command = lambda: controller.show_frame(MainWindow))
        button.grid(sticky="nsew")

    # Hardcoded ID weghalen
    def retrieve_answer(self, rank_df, parent_df, name):
        soort = rank_df.loc[rank_df['Naam_NL'] == name]
        parent_ID = soort['Familie_ID'].values[0]
        familie = parent_df.loc[parent_df['ID'] == parent_ID]
        answer = familie['Naam_LA'].values[0]
        return answer

    def update_question(self, message, questions, rank, parents):
        parent = parents[rank]
        message.config(text = questions[parent])

    def show_answers(self, options, var):
        for option, value in options:
            b = tk.Radiobutton(self, text = option, variable = var, value = value, anchor=tk.W)
            b.grid(sticky="ew")


app = AppWindow()
app.mainloop()
