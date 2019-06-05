#!/usr/bin/python
import tkinter as tk
import tkinter.font as tkF
import pandas as pd

# Geraamte van de applicatie
class AppWindow(tk.Tk):

    def __init__(self):

        tk.Tk.__init__(self)
        self.title("LinneausDex - DEV")
        self.geometry("900x800")
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

        self.user_ans = []
        # self.real_ans = []
        self.current_rank = ranklist[0]

        soort_q = "Wat is de Nederlandse naam van de soort die je wilt classificeren?"
        familie_q = "Tot welke familie behoort deze soort?"
        orde_q = "Wat is de naam van de orde waar deze familie toe behoort?"
        klasse_q = "Wat is de naam van de klasse boven deze orde?"
        stam_q = "Tot welke stam behoort deze klasse?"
        rijk_q = "Tot slot: Wat is de naam van het rijk waar deze klasse toe behoort?"

        QUESTIONS = {
            "Soort": soort_q,
            "Familie" : familie_q,
            "Orde": orde_q,
            "Klasse": klasse_q,
            "Stam": stam_q,
            "Rijk": rijk_q
        }

        PARENTS = {
            "Start": "Soort",
            "Soort": "Familie",
            "Familie": "Orde",
            "Orde": "Klasse",
            "Klasse": "Stam",
            "Stam": "Rijk",
            "Rijk": None
        }
        self.real_ans = self.get_full_answer("Canis aureus", PARENTS)

        questionframe = tk.Frame(self, height=600, width=440, bg="white",
                                    bd=1, relief=tk.SOLID)
        questionframe.grid(padx=5, pady=5, row=0, column=0, sticky="nsew")
        questionframe.grid_propagate(False)
        question = tk.Message(questionframe, width=430, bg="white")
        question.grid(sticky="nsew")

        ans = tk.StringVar()

        field = tk.Entry(self, textvariable = ans)
        field.grid(padx=5, pady=5, sticky = "nsew")
        self.init_question(question, QUESTIONS)

        s = tk.Button(self, text="submit",
            command = lambda: self.update_question(question, field, QUESTIONS, PARENTS))
        # s = tk.Button(self, text="submit",
        #     command = lambda: self.get_full_answer(ans.get(), ranklist, PARENTS))
        # s = tk.Button(self, text="submit",
        #     command = lambda: self.get_answer(PARENTS, "Soort", ans.get()))
        s.grid(sticky="nsew")


        button = tk.Button(self, text = " Home ",
                            command = lambda: self.clean_page(controller, question, field, QUESTIONS))
        button.grid(sticky="nsew")

        canvas = TreeDisplay(self)
        canvas.grid(row=0, column=1, columnspan=2)


    # Nu nog naam LA
    def get_answer(self, name, rank, parents):
        parent = parents[rank]
        db = dataframes[rank]
        row = db.loc[db['Naam_LA'] == name]
        parent_ID = row[parent+'_ID'].values[0]
        parent_row = dataframes[parent].loc[dataframes[parent]['ID'] == parent_ID]
        answer = parent_row['Naam_LA'].values[0]
        # print(answer)
        return answer

    def get_full_answer(self, name, parents):
        answer = [name]
        for i in ranklist[:-1]:
            name = self.get_answer(name, i, parents)
            answer.append(name)
        # print(answer)
        return answer

    def init_question(self, message, questions):
        message.config(text = questions[self.current_rank])

    def update_question(self, message, entry, questions, parents):
        self.user_ans.append(entry.get())
        if parents[self.current_rank] == None:
            print(self.user_ans)
            return
        self.current_rank = parents[self.current_rank]
        message.config(text = questions[self.current_rank])
        entry.delete(0, tk.END)

    def clean_page(self, controller, message, entry, questions):
        self.user_ans = []
        self.real_ans = []
        self.current_rank = ranklist[0]
        entry.delete(0, tk.END)
        self.init_question(message, questions)
        controller.show_frame(MainWindow)

    def show_answers(self, options, var):
        for option, value in options:
            b = tk.Radiobutton(self, text = option, variable = var, value = value, anchor=tk.W)
            b.grid(sticky="ew")



# Herbruikbaar canvas waar taxonomische bomen in getekend kunnen worden.
class TreeDisplay(tk.Canvas):

    def __init__(self, master):
        tk.Canvas.__init__(self, master)
        canvas = tk.Canvas(self, bg="white", height=600, width=440)
        colors = ['#99ccff', '#b3ff66', '#ffd699', '#00b3b3', '#ff9999', '#ffff99']
        canvas.grid(columnspan=3, padx=5, pady=5)
        curr_X  = tk.IntVar()
        curr_Y = tk.IntVar()
        curr_X.set(6), curr_Y.set(6)
        self.answer_list = []
        self.node_list = []


        b = tk.Button(self, text="square",
            command = lambda: self.draw_node(canvas, "Bosmuis", colors[2], curr_X, curr_Y))
        b.grid(column=0, row=1)
        b2 = tk.Button(self, text="squarespace",
            command = lambda: self.draw_nodes(canvas, colors, self.answer_list, curr_X, curr_Y))
        b2.grid(column=1, row=1)
        b3 = tk.Button(self, text="spacesquare",
            command = lambda: self.draw_answer(master, canvas, colors, curr_X, curr_Y))
        b3.grid(column=2, row=1)

    def draw_node(self, canvas, rank, color, X, Y):
        anchor_X = ((canvas.winfo_width()-2)/4) # alligns nodes
        x = X.get()
        y = Y.get()
        node_width = used_font.measure(rank) + 10
        start_X = anchor_X - (node_width/2) - 6
        node = canvas.create_rectangle(start_X, y, start_X + node_width, y + NODE_HEIGHT, fill = color)
        self.node_list.append(node)
        self.answer_list.append(rank)
        canvas.create_text(anchor_X - 3, y + (NODE_HEIGHT/2), text = rank, font = used_font)
        Y.set(y+NODE_HEIGHT*2)
        self.connect_nodes(canvas)

    def draw_nodes(self, canvas, colors, answers, X, Y):
        x = X.get()
        y = Y.get()
        for i in range(len(answers)):
            self.draw_node(canvas, answers[i], colors[i], X, Y)


    def connect_nodes(self, canvas):
        if len(self.node_list) > 1:
            for i in range(len(self.node_list)-1):
                xa0, ya0, xa1, ya1 = canvas.bbox(self.node_list[i])
                xb0, yb0, xb1, yb1 = canvas.bbox(self.node_list[i+1])
                # print(xb0, xb1, yb0, yb1)
                # print(xa0, xa1, ya0, ya1)
                # print((xa0+xa1)/2, ya1-1, (xb0+xb1)/2, yb0+1)
                canvas.create_line((xa0+xa1)/2, ya1-1, (xb0+xb1)/2, yb0+1)

    def get_answer_list(self, master):
        answers = master.real_ans
        return answers

    def draw_answer(self, master, canvas, colors, X, Y):
        answers = self.get_answer_list(master)
        print(answers)
        self.draw_nodes(canvas, colors, answers, X, Y)

NODE_WIDTH = 50
NODE_HEIGHT = 30
BRANCH_LENGTH = 25

ranklist = ["Soort", "Familie", "Orde", "Klasse", "Stam", "Rijk"]
dataframes = {}
for i in ranklist:
    db = pd.read_excel("data/" + i + ".xlsx") # Unix
    #db = pd.read_excel("data\\" + i + ".xlsx") # Windows
    dataframes[i] = pd.DataFrame(db)

app = AppWindow()
app.mainloop()
# input() # debugging
