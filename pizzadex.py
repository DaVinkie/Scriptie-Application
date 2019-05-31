#!/usr/bin/python
import tkinter as tk
import tkinter.font as tkF
import pandas as pd

# Geraamte van de applicatie
class AppWindow(tk.Tk):

    def __init__(self):

        tk.Tk.__init__(self)
        self.title("LinneausDex - DEV")
        self.geometry("450x800")
        global used_font
        used_font = tkF.Font(family="Courier", size=12)

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

        ranklist = ["Soort", "Familie", "Orde", "Klasse", "Stam", "Rijk"]
        n_ranks = len(ranklist)

        soort_q = "Wat is de Nederlandse naam van de soort die je wilt classificeren?"
        familie_q = "Tot welke familie behoort deze soort?"
        orde_q = "Wat is de naam van de orde waar deze familie toe behoort?"

        QUESTIONS = {
            "Soort": soort_q,
            "Familie" : familie_q,
            "Orde": orde_q
        }

        PARENTS = {
            "Start": "Soort",
            "Soort": "Familie",
            "Familie": "Orde",
            "Orde": "Klasse",
            "Klasse": "Stam",
            "Stam": "Rijk"
        }

        questionframe = tk.Frame(self, height=600, width=440, bg="white",
                                    bd=1, relief=tk.SOLID)
        questionframe.grid(padx=5, pady=5, row=0, column=0, sticky="nsew")
        # questionframe.grid_propagate(False)
        question = tk.Message(questionframe, width=430, bg="white")
        question.grid(sticky="nsew")
        rank = PARENTS["Start"]
        self.update_question(question, QUESTIONS, rank, PARENTS)

        # ans = tk.IntVar()
        ans = tk.StringVar()

        field = tk.Entry(self, textvariable = ans)
        field.grid(padx=5, pady=5, sticky = "nsew")

        # s = tk.Button(self, text="submit",
        #     command = lambda: self.update_question(question, QUESTIONS, PARENTS[rank], PARENTS))
        # s.grid(sticky="nsew")
        s = tk.Button(self, text="submit",
            command = lambda: self.get_full_answer(ranklist, ans.get(), PARENTS))
        s.grid(sticky="nsew")

        # print(self.retrieve_answer(soort_df, familie_df, "Bosmuis"))

        button = tk.Button(self, text = " Home ",
                            command = lambda: controller.show_frame(MainWindow))
        button.grid(sticky="nsew")

        canvas = TreeDisplay(self)
        canvas.grid(row=0, column=1)

    # Nu nog naam LA
    def get_full_answer(self, ranklist, name, parents):
        answer = [name]
        for i in ranklist[:-1]:
            parent = parents[i]+'_ID'
            row = dataframes[i].loc[dataframes[i]['Naam_LA'] == name]
            parent_ID = row[parent].values[0]
            parent_row = dataframes[parents[i]].loc[dataframes[parents[i]]['ID'] == parent_ID]
            name = parent_row['Naam_LA'].values[0]
            answer.append(name)
        print(answer)
        return answer

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

# Herbruikbaar canvas waar taxonomische bomen in getekend kunnen worden.
class TreeDisplay(tk.Canvas):

    def __init__(self, master):
        tk.Canvas.__init__(self, master)
        canvas = tk.Canvas(self, bg="white", height=800, width=450)
        colors = ['#99ccff', '#b3ff66', '#ffd699', '#00b3b3', '#ff9999', '#ffff99']
        canvas.grid()
        nodes = []
        curr_X  = tk.IntVar()
        curr_Y = tk.IntVar()
        curr_X.set(6), curr_Y.set(6)
        b = tk.Button(self, text="square",
            command = lambda: self.draw_node(canvas, "Kaasmakker", colors[2], curr_X, curr_Y, nodes))
        b.grid(column=0, row=1)
        b2 = tk.Button(self, text="squarespace",
            command = lambda: self.draw_nodes(canvas, colors, nodes, curr_X, curr_Y))
        b2.grid(column=1, row=1)

    def draw_node(self, canvas, rank, color, X, Y, nodelist):
        x = X.get()
        y = Y.get()
        node_width = used_font.measure(rank) + 10
        # print("Width = ", node_width)
        node = canvas.create_rectangle(x, y, x + node_width, y + NODE_HEIGHT, fill = color)
        nodelist.append(node)
        canvas.create_text(x + (node_width/2), y + (NODE_HEIGHT/2), text = rank, font = used_font)
        Y.set(y+NODE_HEIGHT*2)
        self.connect_nodes(canvas, nodelist)

    def draw_nodes(self, canvas, colors, nodelist, X, Y):
        x = X.get()
        y = Y.get()
        for i in range(len(ranklist)):
            self.draw_node(canvas, ranklist[i], colors[i], X, Y, nodelist)


    def connect_nodes(self, canvas, nodelist):
        if len(nodelist) > 1:
            for i in range(len(nodelist)-1):
                xa0, ya0, xa1, ya1 = canvas.bbox(nodelist[i])
                xb0, yb0, xb1, yb1 = canvas.bbox(nodelist[i+1])
                # print(xb0, xb1, yb0, yb1)
                # print(xa0, xa1, ya0, ya1)
                # print((xa0+xa1)/2, ya1-1, (xb0+xb1)/2, yb0+1)
                canvas.create_line((xa0+xa1)/2, ya1-1, (xb0+xb1)/2, yb0+1)


NODE_WIDTH = 50
NODE_HEIGHT = 30
BRANCH_LENGTH = 25

ranklist = ["Soort", "Familie", "Orde", "Klasse", "Stam", "Rijk"]
dataframes = {}
for i in ranklist:
    db = pd.read_excel("data\\" + i + ".xlsx")
    dataframes[i] = pd.DataFrame(db)

app = AppWindow()
app.mainloop()
# input() # debugging
