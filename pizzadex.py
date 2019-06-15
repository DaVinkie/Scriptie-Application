#!/usr/bin/python
import tkinter as tk
import tkinter.font as tkF
import pandas as pd
import math
from random import randint

# Geraamte van de applicatie
class AppWindow(tk.Tk):

    def __init__(self):

        tk.Tk.__init__(self)
        self.title("LinneausDex - DEV")
        # self.geometry("900x800")
        # self.update_idletasks()
        # rh = self.winfo_height()
        # rw = self.winfo_width()

        global used_font
        used_font = tkF.Font(family="Courier", size=12)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=8)

        side = tk.Frame(self, bd=2, relief=tk.SOLID) # width=(rw/8)
        sidebar = SideMenu(side, self)

        side.grid(row=0, column=0, sticky="nsew")
        sidebar.grid(column=0, sticky="nsew")

        main_window = tk.Frame(self, bd=2, relief=tk.SOLID) #width=450
        main_window.grid(row=0, column=1, sticky="nsew")

        self.main = main_window
        # pages = ["Classificeer", "Vergelijk", "Modelleer", "Verbeter"]
        self.frames = {}
        # in een pages loop
        main_frame = MainWindow(main_window, self)
        self.frames[MainWindow] = main_frame
        question_frame = QuestionWindow(main_window, self)
        self.frames[QuestionWindow] = question_frame
        compare_frame = CompareWindow(main_window, self)
        self.frames[CompareWindow] = compare_frame

        main_frame.grid(row=0, column=1, sticky="nsew")
        question_frame.grid(row=0, column=1, sticky="nsew")
        compare_frame.grid(row=0, column=1, sticky="nsew")
        # main_frame.grid_propagate(False) // Heeft geen size dus werkt niet
        # question_frame.grid_propagate(False)

        self.show_frame(MainWindow)

    def show_frame(self, frame):
        selected = self.frames[frame]
        print(selected)
        selected.tkraise()

    def top_window(self, frame):
        top = frame.winfo_children()
        return top[-1]


class SideMenu(tk.Frame):
    def __init__(self, controller, master):
        tk.Frame.__init__(self, controller)
        self.parent = master
        controller.grid_columnconfigure(0, weight=1)

        home = tk.Button(controller, text=" home ", command=self.go_home)
        back = tk.Button(controller, text=" refresh ", command=self.refresh)

        home.grid(row=0, sticky="ew")
        back.grid(row=1, sticky="ew")

        self.bind("<Button-1>", self.show_event)

    def show_event(event):
        print(event.x, event.y)

    def refresh(self):
        active = self.parent.top_window(self.parent.main)
        print(self.parent.main, active)
        active.clean_page()

    def go_home(self):
        self.refresh()
        self.parent.show_frame(MainWindow)
        # self.parent.

# Hoofdscherm / Hoofdmenu
class MainWindow(tk.Frame):

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)

        # QuestionWindow vervangen door correcte waarde
        pages = [
            ("Classificeer", "DarkSlategray2", QuestionWindow),
            ("Vergelijk", "khaki2", CompareWindow),
            ("Modelleer", "light pink", QuestionWindow),
            ("Verbeter", "firebrick1", QuestionWindow)
        ]

        frames = []
        for i in range(4): # make variable
            f = tk.Frame(self, height=215, width=215)
            f.pack_propagate(False)
            frames.append(f)

        buttons = []
        for i in range(len(frames)):
            buttons.append(tk.Button(frames[i], text=pages[i][0], bg=pages[i][1],
                            command = lambda i=i: controller.show_frame(pages[i][2])))
            buttons[i].pack(expand=True, fill=tk.BOTH)

        # Misschien in een loop.
        frames[0].grid(row=0, column=0, padx=5, pady=5)
        frames[1].grid(row=0, column=1, padx=5, pady=5)
        frames[2].grid(row=1, column=0, padx=5, pady=5)
        frames[3].grid(row=1, column=1, padx=5, pady=5)

# FrameWork for all the Windows to inherit from
class FrameWork(tk.Frame):

    def __init__(self, parent, host):
        tk.Frame.__init__(self, parent)
        # main components of every window
        self.parent     = parent
        self.host      = host
        self.real_answer = []
        self.user_answer = []

        self.SUPER_RANKS = {
            "Start": "Soort",
            "Soort": "Familie",
            "Familie": "Orde",
            "Orde": "Klasse",
            "Klasse": "Stam",
            "Stam": "Rijk",
            "Rijk": None
        }

    # Returns a random entry from the base dataframe, in this case Soort
    def get_random(self):
        base = "Soort" # variable for future variations of base layer
        base_layer = dataframes[base]
        max = len(base_layer)
        r = randint(0, max)
        row = base_layer.iloc[[r]]

        if isinstance(row['Naam_NL'].values[0], str):
            print("NL", row['Naam_NL'].values[0])
            return row['Naam_NL'].values[0]
        else:
            print("LA", row['Naam_LA'].values[0])
            return row['Naam_LA'].values[0]

# Voor het classificatie gedeelte
class QuestionWindow(tk.Frame):

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.master = master
        self.controller = controller
        self.first = True

        self.user_ans = []
        self.real_ans = []
        self.current_rank = ranklist[0]

        soort_q = "Wat is de Nederlandse naam van de soort die je wilt classificeren?"
        familie_q = "Tot welke familie behoort deze soort?"
        orde_q = "Wat is de naam van de orde waar deze familie toe behoort?"
        klasse_q = "Wat is de naam van de klasse boven deze orde?"
        stam_q = "Tot welke stam behoort deze klasse?"
        rijk_q = "Tot slot: Wat is de naam van het rijk waar deze klasse toe behoort?"

        self.QUESTIONS = {
            "Soort": soort_q,
            "Familie" : familie_q,
            "Orde": orde_q,
            "Klasse": klasse_q,
            "Stam": stam_q,
            "Rijk": rijk_q
        }

        self.PARENTS = {
            "Start": "Soort",
            "Soort": "Familie",
            "Familie": "Orde",
            "Orde": "Klasse",
            "Klasse": "Stam",
            "Stam": "Rijk",
            "Rijk": None
        }
        # Waarom staat dit hier?
        # self.real_ans = self.get_full_answer("Canis aureus")

        questionframe = tk.Frame(self, bg="white", #height=600, width=440,
                                    bd=1, relief=tk.SOLID)
        questionframe.grid(padx=5, pady=5, row=0, column=0, sticky="nsew")
        questionframe.grid_propagate(False)
        self.question = tk.Message(questionframe, bg="white") # width=430,
        self.question.grid(sticky="nsew")

        ans = tk.StringVar()

        self.field = tk.Entry(self, textvariable = ans)
        self.field.grid(padx=5, pady=5, sticky = "nsew")
        self.init_question()

        s = tk.Button(self, text="submit", command=self.update_question)
        # s = tk.Button(self, text="submit",
        #     command = lambda: self.get_full_answer(ans.get(), ranklist, PARENTS))
        # s = tk.Button(self, text="submit",
        #     command = lambda: self.get_answer(PARENTS, "Soort", ans.get()))
        s.grid(sticky="nsew")


        button = tk.Button(self, text=" Home ", command=self.clean_page)
        button.grid(sticky="nsew")

        self.canvas = TreeDisplay(self)
        self.canvas.grid(row=0, column=1, columnspan=2)

        # Bosmuis = Apodemus sylvaticus

    # Nu nog naam LA
    def get_answer(self, name, rank):
        parent = self.PARENTS[rank]
        db = dataframes[rank]
        row = db.loc[db['Naam_LA'] == name]
        parent_ID = row[parent+'_ID'].values[0]
        parent_row = dataframes[parent].loc[dataframes[parent]['ID'] == parent_ID]
        answer = parent_row['Naam_LA'].values[0]
        # print(answer)
        return answer

    def get_full_answer(self, name):
        answer = [name]
        for i in ranklist[:-1]:
            print(name, i)
            name = self.get_answer(name, i)
            answer.append(name)
        # print(answer)
        return answer

    def init_question(self):
        self.question.config(text = self.QUESTIONS[self.current_rank])

    def update_question(self):
        name = self.field.get()
        if self.first:
            print("cucked")
            self.real_ans = self.get_full_answer(name)
            self.first = False

        self.user_ans.append(name)
        if self.PARENTS[self.current_rank] == None:
            print(self.user_ans)
            return
        self.current_rank = self.PARENTS[self.current_rank]
        self.question.config(text = self.QUESTIONS[self.current_rank])
        self.field.delete(0, tk.END)

    def clean_page(self):
        self.user_ans = []
        self.real_ans = []
        self.first = True
        self.current_rank = ranklist[0]
        self.field.delete(0, tk.END)
        self.init_question()
        self.canvas.clear()

class Node():
    def __init__(self, canvas):
        self.rec = canvas.create_rectangle(1, 1, 99, 49, fill="#ffffff")
        self.txt = canvas.create_text(50, 25, text="Node") #font = used_font)

class CompareWindow(FrameWork):
    def __init__(self, parent, host):
        FrameWork.__init__(self, parent, host)

        self.question = tk.Label(self,
                                text="Welke van de twee bomen is de juiste?")
        self.left = tk.Canvas(self, bd=1, bg="white", relief="solid")
        self.right = tk.Canvas(self, bd=1, bg="white", relief="solid")
        self.testbutton = tk.Button(self, text="TEST", command=self.get_random)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=10)

        self.question.grid(row=0, sticky="nsew", columnspan=2)
        self.left.grid(row=1, column=0, sticky="nsew")
        self.right.grid(row=1, column=1, sticky="nsew")
        self.testbutton.grid(row=2)
    #
    # def foobar(self):
    #     print(self.SUPER_RANKS)

    def clean_page(self):
        self.user_answer = []
        self.real_answer = []
        self.left.delete("all")
        self.right.delete("all")

class ExploreWindow(tk.Frame):
    def __init__(self, master, controller):
        self.user_answer = []
        self.real_answer = []
        self.canvas = TreeDisplay(self)
        self.canvas.grid(row=0, column=0)

class ClassifyWindow(tk.Frame):
    def __init__(self, master, controller):
        self.user_answer = []
        self.real_answer = []

class QuizWindow(tk.Frame):
    def __init__(self, master, controller):
        self.user_answer = []
        self.real_answer = []


# Herbruikbaar canvas waar taxonomische bomen in getekend kunnen worden.
class TreeDisplay(tk.Canvas):

    def __init__(self, master):
        tk.Canvas.__init__(self, master)
        self.canvas = tk.Canvas(self, bg="white") #, height=600, width=440)
        colors = ['#99ccff', '#b3ff66', '#ffd699', '#00b3b3', '#ff9999', '#ffff99']
        self.canvas.grid(columnspan=3, padx=5, pady=5)
        curr_X  = tk.IntVar()
        curr_Y = tk.IntVar()
        curr_X.set(6), curr_Y.set(6)
        self.answer_list = []
        self.node_list = []


        b = tk.Button(self, text="square",
            command = lambda: self.draw_node(self.canvas, master.field.get(), colors[2], curr_X, curr_Y))
        b.grid(column=0, row=1)
        b2 = tk.Button(self, text="squarespace",
            command = lambda: self.draw_nodes(self.canvas, colors, self.answer_list, curr_X, curr_Y))
        b2.grid(column=1, row=1)
        b3 = tk.Button(self, text="spacesquare",
            command = lambda: self.draw_answer(self.master, self.canvas, colors, curr_X, curr_Y))
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
        fig = Node(canvas)

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

    def clear(self):
        self.node_list = []
        self.answer_list = []
        self.canvas.delete("all") # iets anders dan all

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
