#!/usr/bin/python
import tkinter as tk
import tkinter.font as tkF
import pandas as pd
import math
from random import randint, shuffle

# Geraamte van de applicatie
class AppWindow(tk.Tk):

    def __init__(self):

        tk.Tk.__init__(self)
        self.title("LinneausDex - DEV")
        # self.update_idletasks()
        # rh = self.winfo_height()
        # rw = self.winfo_width()

        global used_font
        used_font = tkF.Font(family="Courier", size=12)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=7)

        side = tk.Frame(self, bd=2, relief=tk.SOLID) # width=(rw/8)
        sidebar = SideMenu(side, self)

        side.grid(row=0, column=0, sticky="nsew")
        sidebar.grid(column=0, sticky="nsew")

        main_window = tk.Frame(self, bd=2, relief=tk.SOLID) #width=450
        main_window.grid_rowconfigure(0, weight=1)
        main_window.grid_columnconfigure(0, weight=1)
        main_window.grid(row=0, column=1, sticky="nsew")

        self.main = main_window
        # pages = ["Classificeer", "Vergelijk", "Modelleer", "Verbeter"]
        self.frames = {}
        # in een pages loop
        main_frame      = MainWindow(main_window, self) # menu
        question_frame  = QuestionWindow(main_window, self) # quizmodel
        compare_frame   = CompareWindow(main_window, self) # vergelijk
        explore_frame   = ExploreWindow(main_window, self) # ontdek db

        self.frames[MainWindow]     = main_frame
        self.frames[QuestionWindow] = question_frame
        self.frames[CompareWindow]  = compare_frame
        self.frames[ExploreWindow]  = explore_frame

        # unfinished
        correct_frame   = CorrectWindow(main_window, self) # corrigeer!
        classify_frame  = ClassifyWindow(main_window, self) # classificeer!
        infer_frame     = InferWindow(main_window, self) # groepeer op basis van iets
        quiz_frame      = QuizWindow(main_window, self) # ook quiz?
        inter_frame     = InterWindow(main_window, self) # modelleer op basis van tekst
        differ_frame    = DifferWindow(main_window, self) # geef relevantie aan
        create_frame    = CreateWindow(main_window, self) # modelleer

        self.frames[CorrectWindow]  = correct_frame
        self.frames[ClassifyWindow] = classify_frame
        self.frames[InferWindow]    = infer_frame
        self.frames[QuizWindow]     = quiz_frame
        self.frames[InterWindow]    = inter_frame
        self.frames[DifferWindow]   = differ_frame
        self.frames[CreateWindow]   = create_frame

        main_frame.grid(row=0, column=0, sticky="nsew")
        question_frame.grid(row=0, column=0, sticky="nsew")
        compare_frame.grid(row=0, column=0, sticky="nsew")
        explore_frame.grid(row=0, column=0, sticky="nsew")
        correct_frame.grid(row=0, column=0, sticky="nsew")
        classify_frame.grid(row=0, column=0, sticky="nsew")
        infer_frame.grid(row=0, column=0, sticky="nsew")
        quiz_frame.grid(row=0, column=0, sticky="nsew")
        inter_frame.grid(row=0, column=0, sticky="nsew")
        differ_frame.grid(row=0, column=0, sticky="nsew")
        create_frame.grid(row=0, column=0, sticky="nsew")


        self.show_frame(MainWindow)

    def show_frame(self, frame):
        selected = self.frames[frame]
        # print(selected)
        selected.tkraise()
        selected.start()

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
        # print(self.parent.main, active)
        active.clean_page()

    def go_home(self):
        self.refresh()
        self.parent.show_frame(MainWindow)


# Hoofdscherm / Hoofdmenu
class MainWindow(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)

        pages = [
            ("Classificeer","DarkSlategray2",   ClassifyWindow),
            ("Vergelijk",   "khaki2",           CompareWindow),
            ("Verbeter",    "firebrick1",       CorrectWindow),
            # ("Beantwoord",  "DarkSlategray2",   QuestionWindow),
            ("Quiz",        "khaki2",           QuizWindow),
            ("Ontdek",      "light pink",       ExploreWindow),
            ("Groepeer",    "firebrick1",       InferWindow),
            ("Maak",        "DarkSlategray2",   CreateWindow),
            ("Interpreteer","khaki2",           InterWindow),
            ("Relevantie",  "light pink",       DifferWindow)
        ]

        for i in range(3):
            self.grid_rowconfigure(i, weight=1)
            self.grid_columnconfigure(i, weight=1)
            for j in range(3):
                k = (i*3) + j
                f = tk.Frame(self)
                b = tk.Button(f, text=pages[k][0], bg=pages[k][1],
                    command=lambda k=k: controller.show_frame(pages[k][2]))
                b.pack(expand=True, fill="both")
                f.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")

    def start(self):
        print("Start ", self)

# FrameWork for all the Windows to inherit from
class FrameWork(tk.Frame):

    def __init__(self, parent, host):
        tk.Frame.__init__(self, parent)
        # main components of every window
        self.debug  = True
        self.score  = 0
        self.parent = parent
        self.host   = host
        self.real_answer = []
        self.user_answer = []

        self.SUPER_RANKS = {
            "Start":    None,
            "Soort":    "Familie",
            "Familie":  "Orde",
            "Orde":     "Klasse",
            "Klasse":   "Stam",
            "Stam":     "Rijk",
            "Rijk":     "Start"
        }
        self.SUB_RANKS = {
            "Soort":    None,
            "Familie":  "Soort",
            "Orde":     "Familie",
            "Klasse":   "Orde",
            "Stam":     "Klasse",
            "Rijk":     "Stam",
            "Start":    "Rijk"
        }
        self.COLORS = {
            "Start":    '#ffffff',
            "Soort":    '#99ccff',
            "Familie":  '#b3ff66',
            "Orde":     '#ffd699',
            "Klasse":   '#00b3b3',
            "Stam":     '#ff9999',
            "Rijk":     '#ffff99'
        }

    # Returns a random entry from the base dataframe, in this case Soort
    def get_random(self, rank="Soort"):
        # base        = ranklist[0] # variable for future variations of base layer
        base_layer  = dataframes[rank]
        max         = len(base_layer)-1
        r           = randint(0, max)
        row         = base_layer.iloc[[r]]

        if isinstance(row['Naam_NL'].values[0], str):
            return row['Naam_NL'].values[0]
        else:
            return row['Naam_LA'].values[0]

    # Returns the row from a dataframe given the right name.
    def get_row(self, name, df):
        if df['Naam_NL'].str.contains(name).any():
            row = df.loc[df['Naam_NL'] == name]
            return row
        elif df['Naam_LA'].str.contains(name).any():
            row = df.loc[df['Naam_LA'] == name]
            return row
        else:
            print("Error: Naam niet bekend in database.")
            return

    # Retrieves the Dutch name from a row if it's there, returns the Latin name otherwise.
    def get_name(self, row):
        if isinstance(row['Naam_NL'].values[0], str):
            return row['Naam_NL'].values[0]
        else:
            return row['Naam_LA'].values[0]

    # Picks the Dutch name if it has a value, returns Latin otherwise.
    def get_name_frame(self, dutch, latin):
        if isinstance(dutch, str):
            return dutch
        else:
            return latin

    # Returns the -Dutch if present- name of the parent taxon of a given name.
    def get_parent(self, name, rank):
        print("DEBUG: ", name, rank)
        super   = self.SUPER_RANKS[rank]
        df      = dataframes[rank]
        df_s    = dataframes[super]

        row         = self.get_row(name, df)
        super_id    = row[super + '_ID'].values[0]
        super_row   = df_s.loc[df_s['ID'] == super_id]
        print("DEBUG", rank, name)
        parent = self.get_name(super_row)
        return parent

    # Returns a list containing the entire branch ending at the given name.
    def get_branch(self, name):
        branch = [name]
        for rank in ranklist[:-1]:
            name = self.get_parent(name, rank)
            branch.append(name)
        branch.reverse()
        return branch

    # Returns a list of all sub taxons that have the given name as parent.
    def get_children(self, name, rank):
        sub     = self.SUB_RANKS[rank]
        df      = dataframes[rank]
        df_sub  = dataframes[sub]

        row     = self.get_row(name, df)
        id      = row['ID'].values[0]
        sub_rows = df_sub.loc[df_sub[rank + '_ID'] == id]

        children = [self.get_name_frame(dutch, latin) for dutch, latin in
                    zip(sub_rows['Naam_NL'], sub_rows['Naam_LA'])]
        return children

    def show_result(self):
        window = tk.Toplevel(self, width=160, height=90)
        r = "Je hebt een "+str(round((self.score), 2))+" van de 10 gescoord."
        result = tk.Message(window, text=r, font=used_font, aspect=300)
        button = tk.Button(window, text="Probeer opnieuw",
                    command = lambda: self.start(window))
        result.pack(padx=5, pady=5, expand=True, fill="both")
        button.pack()
        window.grab_set()

    def start(self, window=None):
        print("Start: ", self)

    def clean_page(self):
        print("Clean: ", self)

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
    def start(self):
        print("Start ", self)
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
        self.turn = 0
        self.correct = 0
        self.wrong_answer = []
        # self.ricardo    = tk.PhotoImage(file="ricardo.png")
        # self.siem       = tk.PhotoImage(file="siem.png")

        self.description = tk.Label(self, font=used_font,
                                text="Welke van de twee bomen is de juiste?")
        self.left = tk.Canvas(self, bd=1, bg="white", relief="solid")
        self.right = tk.Canvas(self, bd=1, bg="white", relief="solid")

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=9)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.description.grid(row=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.left.grid(row=1, column=0, sticky="nsew")
        self.right.grid(row=1, column=1, sticky="nsew")

        self.left.bind("<Button-1>", self.take_turn)
        self.right.bind("<Button-1>", self.take_turn)

    def start(self):
        self.setup_comp()

    # Debug function
    def testprint(self, event):
        if event.widget == self.left:
            event.widget.create_image(event.x, event.y, image=self.siem)
        elif event.widget == self.right:
            event.widget.create_image(event.x, event.y, image=self.ricardo)
        if event.widget == self.left:
            print("DEBUG: SWITCHED CORRECTLY")

    # Retrieves the branch of a random entry and edits a random element to
    # create a right and a wrong answer.
    def create_options(self):
        self.real_answer = self.get_branch(self.get_random())
        self.fake_answer = self.real_answer[:]

        r = randint(0, len(ranklist)-1)
        reverse_ranks = ranklist[::-1]
        fake = self.get_random(reverse_ranks[r])
        while (fake == self.real_answer[r]): # safety net for generating the same answer
            fake = self.get_random(reverse_ranks[r])
        self.fake_answer[r] = fake

    # Clears visual feedback and shuffles the options in place.
    def shuffle_answers(self):
        self.left.config(bg="white")
        self.right.config(bg="white")
        columns = [0,1]
        shuffle(columns)
        self.left.grid_configure(column=columns[0])
        self.right.grid_configure(column=columns[1])

    # Shows the user their results
    def show_result(self):
        print("showing_results: ", self.turn, self.correct)
        self.clean_page()

    # Does the setup for every round
    def setup_comp(self):
        self.turn+=1
        self.create_options()
        self.draw_branches()
        self.shuffle_answers()

    # Gives visual feedback to the user
    def give_feeback(self, event):
        if event.widget == self.left:
            event.widget.config(bg="green")
            self.correct+=1
        else:
            event.widget.config(bg="red")

    # Takes a turn
    def take_turn(self, event):
        if self.turn >= 10:
            self.show_result()
        elif self.turn > 0:
            self.give_feeback(event)
            self.after(500, self.setup_comp)

    # Draws the two potential branches on the canvas
    def draw_branches(self):
        self.left.delete("all")
        self.right.delete("all")
        self.draw_branch(self.left, self.real_answer)
        self.draw_branch(self.right, self.fake_answer)
        print("drawing branches")

    def draw_node(self, canvas, name, color, anchor, node_height, num):
        node_width  = (used_font.measure(text=name) + 10)/2
        pos = list(range(1, 12, 2))
        canvas.create_rectangle((anchor-node_width), (node_height*pos[num]), (anchor+node_width),
                                (node_height*(pos[num]+1)), fill=color)
        canvas.create_text(anchor, (node_height*(pos[num])+(node_height/2)), text=name, font=used_font)

    def draw_branch(self, canvas, branch):
        anchor      = (canvas.winfo_width()-2)/2
        node_height = (canvas.winfo_height()-2)/13

        for i in range(len(branch)):
            self.draw_node(canvas, branch[i], self.COLORS[ranklist[i]], anchor, node_height, i)
        self.connect_nodes(canvas)

    def connect_nodes(self, canvas):
        anchor = (canvas.winfo_width()-2)/2
        con_height = (canvas.winfo_height()-2)/13
        pos = list(range(2, 11, 2))
        for i in pos:
            canvas.create_line(anchor, (con_height*i), anchor, (con_height*(i+1)))

    # Refreshes the page
    def clean_page(self):
        self.turn = 0
        self.correct = 0
        self.user_answer = []
        self.real_answer = []
        self.wrong_answer = []
        self.left.delete("all")
        self.right.delete("all")
        self.setup_comp()

class ExploreWindow(FrameWork):
    def __init__(self, parent, host):
        FrameWork.__init__(self, parent, host)
        self.top_node = None
        self.bottom_nodes = []
        self.current_rank = None

        self.description = tk.Label(self, font=used_font,
            text="Klik op een dochter om die tak te ontdekken, klik op de wortel om een stap terug te doen.")
        self.canvas = tk.Canvas(self, bd=1, bg="white", relief="solid")

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=9)
        self.grid_columnconfigure(0, weight=1)

        self.description.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.canvas.grid(row=1, column=0, sticky="nsew")

    def start(self):
        self.draw_start()

    # Opens the next or the previous node
    def explore(self, event):
        selected = self.canvas.find_closest(event.x, event.y)
        name = self.canvas.gettags(selected)[0]

        if name == "Wortel":
            print("Error: Root has no parents.")
            return
        elif name == self.top_node:
            if self.current_rank == "Rijk":
                self.draw_start()
            self.top_node = self.get_parent(name, self.current_rank)
            self.current_rank = self.SUPER_RANKS[self.current_rank]
            self.bottom_nodes = self.get_children(self.top_node, self.current_rank)
            self.draw_selection()
        elif name in self.bottom_nodes:
            if self.current_rank == self.SUPER_RANKS["Soort"]:
                print("Error: Leaf nodes have no children.")
                return
            self.top_node = name
            self.current_rank = self.SUB_RANKS[self.current_rank]
            self.bottom_nodes = self.get_children(self.top_node, self.current_rank)
            self.draw_selection()

    def clean_page(self):
        self.canvas.delete("all")
        self.draw_start()

    def draw_node(self, text, color, width, height, X_anchor, Y_anchor):
        self.canvas.create_rectangle((X_anchor-(width/2)), (Y_anchor-(height/2)),
                                    (X_anchor+(width/2)), (Y_anchor+(height/2)),
                                    fill=color, tag=text)
        self.canvas.create_text(X_anchor, Y_anchor, text=text, tag=text)

    def draw_selection(self):
        self.canvas.delete("all")
        # Basically the amount of rows and columns except in coordinates
        X_div = (len(self.bottom_nodes)*2)+1
        Y_div = 5
        # Size of the nodes
        X_rel = self.canvas.winfo_width() / X_div
        Y_rel = self.canvas.winfo_height() / Y_div
        # Anchor points for parent and child nodes
        PX_anchor = self.canvas.winfo_width() / 2
        PY_anchor = (1.5*Y_rel)
        CY_anchor = (3.5*Y_rel)
        # Horizontal step size for the children nodes
        step = list(range(1, X_div, 2))
        step = [x+0.5 for x in step]
        sub_rank = self.SUB_RANKS[self.current_rank]

        self.draw_node(self.top_node, self.COLORS[self.current_rank], X_rel, Y_rel,
            PX_anchor, PY_anchor)
        if self.top_node != "Wortel":
            self.canvas.create_line(PX_anchor, 0, PX_anchor, Y_rel, width=2)
        self.canvas.tag_bind(self.top_node, '<Button-1>', self.explore)
        for i in range(len(self.bottom_nodes)):
            self.draw_node(self.bottom_nodes[i], self.COLORS[sub_rank],
                X_rel, Y_rel, (step[i]*X_rel), CY_anchor)
            self.canvas.create_line((step[i]*X_rel), (3*Y_rel), PX_anchor, (2*Y_rel),
                width=2)
            self.canvas.tag_bind(self.bottom_nodes[i], '<Button-1>', self.explore)

    def draw_start(self):
        self.top_node = "Wortel"
        self.bottom_nodes = ["Dieren", "Planten", "Schimmels"]
        self.current_rank = "Start"
        self.draw_selection()

class CorrectWindow(FrameWork):
    def __init__(self, master, controller):
        FrameWork.__init__(self, master, controller)
        self.score = 0
        self.turn = 0
        self.user_ans = None
        self.curr_ans = None
        self.replaced = None
        self.replaced_i = None
        self.selected_i = None
        self.fake_answer = []
        self.start_q = "Geef de onjuiste taxon aan."

        self.description= tk.Label(self, font=used_font, text="   Verbeteren   ")

        self.left = tk.Frame(self)
        self.canvas     = tk.Canvas(self.left, bd=1, bg="white", relief="solid")
        self.selection  = self.canvas.create_rectangle(0, 0, 100, 100, outline="red",
                            fill="blue")

        self.right_q = tk.Frame(self)
        self.question   = tk.Message(self.right_q, bd=1, relief="solid", # anchor="n",
                            aspect=300, font=used_font, #bg="white",
                            text=self.start_q)
        self.entry      = tk.Entry(self.right_q, bd=1, relief="solid", font=("Arial 16"))
        self.sb         = tk.Button(self.right_q, text="SUBMIT",
                            command=self.ask_confirmation)
        self.can         = tk.Button(self.right_q, text="Terug",
                            command=self.cancel)
        self.cb         = tk.Button(self.right_q, text="Bevestig",
                            command=self.confirm_selection)
        self.entry.bind('<Return>', self.ask_confirmation)

        self.right_a = tk.Frame(self)
        self.ans_canvas = tk.Canvas(self.right_a, bd=1, bg="white", relief="solid")
        self.next   = tk.Button(self.right_a, text="Volgende",
                        command=self.start)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=9)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.right_q.grid_rowconfigure(0, weight=9)
        self.right_q.grid_rowconfigure(1, weight=1)
        self.right_q.grid_columnconfigure(0, weight=1)
        self.right_q.grid_columnconfigure(1, weight=1)

        self.right_a.grid_rowconfigure(0, weight=1)
        self.right_a.grid_columnconfigure(0, weight=1)
        self.right_a.grid_columnconfigure(1, weight=9)

        self.description.grid(row=0, column=0, padx=5, pady=5, columnspan=2, sticky="nsew")

        self.left.grid(row=1, column=0, sticky="nsew")
        self.canvas.pack(expand=True, fill="both")


        self.right_a.grid(row=1, column=1, sticky="nsew")
        self.next.grid(row=0, column=0, sticky="ew")
        self.ans_canvas.grid(row=0, column=1, sticky="nsew")

        self.right_q.grid(row=1, column=1, sticky="nsew")
        self.question.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.entry.grid(row=1, column=0, sticky="nsew")
        self.sb.grid(row=1, column=1, sticky="nsew")
        self.right_q.lift()

    def draw_node(self, canvas, name, color, anchor, node_height, num):
        node_width  = (used_font.measure(text=name) + 10)/2
        pos = list(range(1, 12, 2))
        canvas.create_rectangle((anchor-node_width), (node_height*pos[num]), (anchor+node_width),
                                (node_height*(pos[num]+1)), fill=color, tag=(name, name+'box', str(num)))
        canvas.create_text(anchor, (node_height*(pos[num])+(node_height/2)),
                            text=name, font=used_font, tag=(name, name+'txt', str(num)))

    def draw_branch(self, canvas, branch):
        anchor      = (canvas.winfo_width()-2)/2
        node_height = (canvas.winfo_height()-2)/13
        for i in range(len(branch)):
            self.draw_node(canvas, branch[i], self.COLORS[ranklist[i]], anchor, node_height, i)
            self.canvas.tag_bind(branch[i], '<Button-1>', self.show_selection)
        self.connect_nodes(canvas)

    def connect_nodes(self, canvas):
        anchor = (canvas.winfo_width()-2)/2
        con_height = (canvas.winfo_height()-2)/13
        pos = list(range(2, 11, 2))
        for i in pos:
            canvas.create_line(anchor, (con_height*i), anchor, (con_height*(i+1)))

    def create_option(self):
        self.real_answer = self.get_branch(self.get_random())
        self.fake_answer = self.real_answer[:]

        r = randint(0, len(ranklist)-1)
        reverse_ranks = ranklist[::-1]

        fake = self.get_random(reverse_ranks[r])
        while (fake == self.real_answer[r]): # safety net for generating the same answer
            fake = self.get_random(reverse_ranks[r])
        self.replaced_i = r
        self.replaced = self.real_answer[r]
        self.fake_answer[r] = fake

    def ask_question(self):
        q = "Wat zou " + self.curr_ans + " moeten zijn?"
        self.question.configure(text=q)

    def show_selection(self, event):
        selected = self.canvas.find_closest(event.x, event.y)
        self.curr_ans = self.canvas.gettags(selected)[0]
        box = self.canvas.find_withtag(self.curr_ans+'box')[0]
        self.canvas.delete(self.selection)
        x0, y0, x1, y1 = self.canvas.bbox(box)
        self.selection  = self.canvas.create_rectangle(x0-5, y0-5, x1+5, y1+5,
                            outline="red", width=2)
        self.ask_question()

    def show_answer(self):
        self.right_a.lift()
        self.update_idletasks()
        self.draw_branch(self.ans_canvas, self.real_answer)
        self.show_correct()

    def show_correct(self):
        box = self.ans_canvas.find_withtag(self.replaced)[0]
        x0, y0, x1, y1 = self.ans_canvas.bbox(box)
        self.ans_canvas.create_rectangle(x0-5, y0-5, x1+5, y1+5, outline="green",
            width=2)

    def ask_confirmation(self, event=None):
        self.user_ans = self.entry.get()
        if (self.user_ans == ""): # Catches random return presses and empty suggestions
            return
        self.question.config(
        text=self.curr_ans + " zou " + self.user_ans + " moeten zijn?")
        self.cb.grid(row=1, column=0, sticky="nsew")
        self.can.grid(row=1, column=1, sticky="nsew")

    def cancel(self):
        self.cb.grid_forget()
        self.can.grid_forget()

    def confirm_selection(self, event=None):
        self.cb.grid_forget()
        self.can.grid_forget()
        self.entry.delete(0, "end")
        node = self.canvas.find_withtag(self.curr_ans+'txt')[0]
        self.selected_i = int(self.canvas.gettags(node)[2])
        self.canvas.itemconfig(node, text=self.user_ans)

        self.calculate_score()
        self.show_answer()

    def calculate_score(self):
        print(self.turn)
        self.turn += 1
        if self.user_ans == self.replaced:
            self.score += 1
        if self.selected_i == self.replaced_i:
            self.score += 1
        if self.turn == 10:
            self.calculate_result()

    def calculate_result(self):
        self.score = round((self.score/2), 2)
        self.show_result()

    def start(self, window=None):
        if window:
            window.destroy()
            self.clean_page()
        self.question.config(text = self.start_q)
        self.right_a.lower()
        self.canvas.delete("all")
        self.ans_canvas.delete("all")
        self.create_option()
        self.draw_branch(self.canvas, self.fake_answer)

    def clean_page(self):
        self.score = 0
        self.turn = 0
        self.user_ans = None
        self.curr_ans = None
        self.replaced = None
        self.replaced_i = None
        self.selected_i = None
        self.fake_answer = []
        self.start()

class ClassifyWindow(FrameWork):
    def __init__(self, master, controller):
        FrameWork.__init__(self, master, controller)
        self.turn = 0
        self.bottom_node = None #"Bosmuis"
        self.top_nodes = []#["Muizen", "Cavia's", "Mensen"]

        self.current_rank = None #"Soort"
        self.super_rank = None #self.SUPER_RANKS[self.current_rank]
        self.labeltext = None #"Geef aan tot welke "+self.super_rank+" deze "+self.current_rank+" hoort."

        self.description = tk.Label(self, font=used_font, text=self.labeltext)
        self.canvas = tk.Canvas(self, bd=1, bg="white", relief="solid")
        self.canvas.bind('<Button-2>', self.print_tag)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=9)
        self.grid_columnconfigure(0, weight=1)

        self.description.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.canvas.grid(row=1, column=0, sticky="nsew")

    def draw_node(self, name, color, width, height, X_anchor, Y_anchor):
        self.canvas.create_rectangle((X_anchor-(width/2)), (Y_anchor-(height/2)),
                                    (X_anchor+(width/2)), (Y_anchor+(height/2)),
                                    fill=color, tag=name)
        self.canvas.create_text(X_anchor, Y_anchor, text=name, tag=name)

    def update_label(self):
        self.labeltext = "Geef aan tot welke "+self.super_rank+" deze "+self.current_rank+" hoort."
        self.description.config(text=self.labeltext)

    def draw_selection(self):
        self.update_label()
        self.canvas.delete("all")
        # Basically the amount of rows and columns except in coordinates
        X_div = (len(self.top_nodes)*2)+1
        Y_div = 5
        # Size of the nodes
        X_rel = self.canvas.winfo_width() / X_div
        Y_rel = self.canvas.winfo_height() / Y_div
        # Anchor points for parent and child nodes
        PY_anchor = (1.5*Y_rel)
        CX_anchor = self.canvas.winfo_width() / 2
        CY_anchor = (3.5*Y_rel)
        # Horizontal step size for the children nodes
        step = list(range(1, X_div, 2))
        step = [x+0.5 for x in step]
        top_rank = self.SUPER_RANKS[self.current_rank]
        self.draw_node(self.bottom_node, self.COLORS[self.current_rank], X_rel, Y_rel,
            CX_anchor, CY_anchor)
        # if self.top_node != "Wortel":
            # self.canvas.create_line(PX_anchor, 0, PX_anchor, Y_rel, width=2)
        self.canvas.tag_bind(self.bottom_node, '<Button-1>', self.classify)
        for i in range(len(self.top_nodes)):
            self.draw_node(self.top_nodes[i], self.COLORS[top_rank],
                X_rel, Y_rel, (step[i]*X_rel), PY_anchor)
            # self.canvas.create_line((step[i]*X_rel), (3*Y_rel), PX_anchor, (2*Y_rel),
                # width=2)
            tags = self.top_nodes[i].split()
            for t in tags:
                self.canvas.tag_bind(t, '<Button-1>', self.classify)

    def print_tag(self, event):
        sel=self.canvas.find_closest(event.x, event.y)
        tags = self.canvas.gettags(sel)

    def draw_start(self):
        self.current_rank = ranklist[0]
        self.super_rank = self.SUPER_RANKS[self.current_rank]
        self.bottom_node = self.get_random()
        self.top_nodes = self.get_selection()
        self.draw_selection()

    def get_selection(self, n=2): # Amount of answers = n+1
        self.real_answer = self.get_parent(self.bottom_node, self.current_rank)
        sel = [self.real_answer.replace('\xa0', '')]
        for i in range(n):
            r = self.get_random(self.super_rank)
            while (r == self.real_answer or r in sel): # counter measurement for duplicates
                r = self.get_random(self.super_rank).replace('\xa0', '')
            sel.append(r)
        shuffle(sel)
        return sel

    def classify(self, event):
        print("Turn: ", self.turn)
        selected = self.canvas.find_closest(event.x, event.y)
        name = self.canvas.gettags(selected)
        print(selected, name)

        if name[0] in self.real_answer:
            self.canvas.itemconfig(selected, fill="green")
            if self.super_rank == ranklist[-1]:
                self.calculate_result()
            else:
                self.update_selection()
        elif name[0] not in self.bottom_node:
            self.canvas.itemconfig(selected, fill="red")
            self.turn += 1
            if name[0] in self.top_nodes:
                self.top_nodes.remove(name[0])
            else:
                self.top_nodes.remove(" ".join(name[:-1]))

        self.after(700, self.draw_selection)

    def update_selection(self):
        self.current_rank = self.SUPER_RANKS[self.current_rank]
        self.super_rank = self.SUPER_RANKS[self.super_rank]
        self.bottom_node = self.real_answer
        self.top_nodes = self.get_selection()
        self.top_nodes = [node.replace('\xa0', '') for node in self.top_nodes]

    def calculate_result(self):
        self.score = round((6/(6+self.turn))*10, 2)
        self.show_result()

    def start(self, window=None):
        if window:
            window.destroy()
            self.clean_page()
        self.draw_start()

    def clean_page(self):
        self.score  = 0
        self.turn   = 0


class InferWindow(FrameWork):
    def __init__(self, master, controller):
        FrameWork.__init__(self, master, controller)
        self.score          = 0
        self.debug          = True
        self.copied         = False
        self.steps          = [1, 1, 1, 1]
        self.groups         = []
        self.options        = []
        self.n_groups       = 3
        self.n_options      = 2
        self.group_rank     = None
        self.option_rank    = None

        self.description    = tk.Label(self, font=used_font,
                                text="Deel de opties bij de juiste groepen in:")
        self.group_canvas0  = tk.Canvas(self, bd=1, bg="white", relief="solid")
        self.group_canvas1  = tk.Canvas(self, bd=1, bg="white", relief="solid")
        self.group_canvas2  = tk.Canvas(self, bd=1, bg="white", relief="solid")
        self.option_canvas  = tk.Canvas(self, bd=1, bg="white", relief="solid")
        self.confirm        = tk.Button(self, text="Bevestig", font=used_font,
                                command=self.confirm_selection)

        self.group_canvases = [self.group_canvas0, self.group_canvas1, self.group_canvas2]
        self.option_canvas.bind('<Button-1>', lambda event, c=self.option_canvas:
            self.paste_node(event, c))
        for gc in self.group_canvases:
            gc.bind('<Button-1>', lambda event, c=gc: self.paste_node(event, c))

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=9)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=9)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.description.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
        self.group_canvas0.grid(row=1, column=0, sticky="nsew")
        self.group_canvas1.grid(row=1, column=1, sticky="nsew")
        self.group_canvas2.grid(row=1, column=2, sticky="nsew")
        self.confirm.grid(row=2, columnspan=3, sticky="nsew")
        self.option_canvas.grid(row=3, column=0, columnspan=3, sticky="nsew")

    # Get the given amount of groups the user has to recognize
    def get_groups(self):
        self.group_rank = ranklist[randint(1, len(ranklist)-1)] # get groups from the same rank
        print(self.group_rank)
        for i in range(self.n_groups):
            # rank = ranklist[randint(1, len(ranklist)-1)] # get groups from different ranks
            self.groups.append((self.get_random(self.group_rank)))

        if self.debug:
            print(self.groups)

    # Get a given amount of children of the pre specified groups.
    def get_options(self):
        self.option_rank = self.SUB_RANKS[self.group_rank]
        for group in self.groups:
            options = self.get_children(group, self.group_rank)
            shuffle(options)
            if len(options) > 1:
                for i in range(self.n_options):
                    self.options.append(options[i])
            elif len(options) == 1:
                self.options.append(options[0])
        self.options = [op.replace('\xa0', '') for op in self.options]
        if self.debug:
            print(self.options)

    # Draw a node on a canvas.
    def draw_node(self, canvas, name, rank, step):
        if self.debug:
            print(self, canvas, name, rank, step)
        if canvas == self.option_canvas:
            width       = (used_font.measure(text=name)+20)
            height      = (used_font.metrics("linespace")+20)
            stepsize    = canvas.winfo_width()/((len(self.options)*2)+1)
            X_anchor    = (step*stepsize) + (stepsize/2)
            Y_anchor    = canvas.winfo_height()/2
        else:
            width       = (used_font.measure(text=name)+10)
            height      = (used_font.metrics("linespace")+10)
            stepsize    = canvas.winfo_height()/(((self.n_options+1)*2)+1)
            X_anchor    = canvas.winfo_width()/2
            Y_anchor    = (step*height) + (height/2)

        canvas.create_rectangle((X_anchor-(width/2)), (Y_anchor-(height/2)),
            (X_anchor+(width/2)), (Y_anchor+(height/2)), fill=self.COLORS[rank],
            tag=name)
        canvas.create_text(X_anchor, Y_anchor, text=name, font=used_font, tag=name)
        if rank == self.option_rank:
            tags = name.split()
            print("TAG DEBUG: ", tags)
            for t in tags:
                canvas.tag_bind(t, '<Button-1>', lambda event, c=canvas: self.copy_node(event, c))

    def copy_node(self, event, canvas):
        selected    = canvas.find_closest(event.x, event.y)
        self.copy_canvas = canvas
        self.copy_name = " ".join(canvas.gettags(selected)[:-1])
        self.copied = True
        # self.draw_node(canvas, name, self.option_rank, 3)
        if self.debug:
            print(selected, self.copy_name)

    def paste_node(self, event, canvas):
        if canvas == self.copy_canvas:
            return
        elif self.copied:
            print(self.copy_name)
            self.copy_canvas.delete(self.copy_name.split()[0])

            if self.copy_canvas == self.option_canvas:
                i = 3
            else:
                i = self.group_canvases.index(self.copy_canvas)
            self.update_step(self.copy_canvas, i, size=-2)

            if canvas == self.option_canvas:
                j = 3
            else:
                j = self.group_canvases.index(canvas)
            print(j, self.steps[j])
            self.draw_node(canvas, self.copy_name, self.option_rank, self.steps[j])
            self.update_step(canvas, j)
            self.copied = False

    def update_step(self, canvas, index, size=2):
        # print(self.group_canvases)
        if (self.steps[index]+size) >= 1:
            self.steps[index] += size

    def confirm_selection(self):
        for gc in self.group_canvases:
            ids = gc.find_all()[::2]
            for id in ids[1:]:
                print("TAG DEBUG 2: ", gc.gettags(id))
                if self.get_parent(" ".join(gc.gettags(id)), self.option_rank) == " ".join(gc.gettags(ids[0])):
                    self.score += 1
        self.calculate_score()
            # print(ids, gc.gettags(ids[-1]))

    def calculate_score(self):
        self.score = round((self.score/len(self.options))*10, 2)
        self.show_result()

    def start(self, window=None):
        if window:
            window.destroy()
            self.clean_page()
            return

        self.get_groups()
        self.get_options()
        for i in range(len(self.options)):
            self.draw_node(self.option_canvas, self.options[i], self.option_rank,
                self.steps[3])
            self.update_step(self.option_canvas, 3)
        for j in range(len(self.groups)):
            self.draw_node(self.group_canvases[j], self.groups[j], self.group_rank,
                self.steps[j])
            self.update_step(self.group_canvases[j], j)

    def clean_page(self):
        self.score          = 0
        self.groups         = []
        self.options        = []
        self.steps          = [1, 1, 1, 1]
        self.n_groups       = 3
        self.n_options      = 2
        self.group_rank     = None
        self.option_rank    = None
        self.option_canvas.delete("all")
        for c in self.group_canvases:
            c.delete("all")
        self.start()

class DifferWindow(FrameWork):
    def __init__(self, master, controller):
        FrameWork.__init__(self, master, controller)

        self.description = tk.Label(self, font=used_font, text="description")
        self.canvas = tk.Canvas(self, bd=1, bg="white", relief="solid")

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=9)
        self.grid_columnconfigure(0, weight=1)

        self.description.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.canvas.grid(row=1, column=0, sticky="nsew")

class QuizWindow(FrameWork):
    def __init__(self, master, controller):
        FrameWork.__init__(self, master, controller)

        self.description = tk.Label(self, font=used_font, text="description")
        self.canvas = tk.Canvas(self, bd=1, bg="white", relief="solid")
        self.canvas.create_rectangle(0, 0, 50, 50, fill="teal", tag="big dick")
        self.canvas.create_rectangle(100, 100, 150, 150, fill="yellow", tag="small peepee")
        self.canvas.bind('<Button-1>', self.print_tag)
        self.canvas.tag_bind('big dick', '<Button-1>', self.print_tag)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=9)
        self.grid_columnconfigure(0, weight=1)

        self.description.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.canvas.grid(row=1, column=0, sticky="nsew")

    def print_tag(self, event):
        sel = self.canvas.find_closest(event.x, event.y)
        print(self.canvas.gettags(sel))

    def generate_open(self):
        if self.debug:
            print("Generating open")

    def generate_mc(self):
        if self.debug:
            print("Generating multiple choice")

class InterWindow(FrameWork):
    def __init__(self, master, controller):
        FrameWork.__init__(self, master, controller)

        self.description = tk.Label(self, font=used_font, text="description")
        self.canvas = tk.Canvas(self, bd=1, bg="white", relief="solid")

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=9)
        self.grid_columnconfigure(0, weight=1)

        self.description.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.canvas.grid(row=1, column=0, sticky="nsew")

class CreateWindow(FrameWork):
    def __init__(self, master, controller):
        FrameWork.__init__(self, master, controller)

        self.description = tk.Label(self, font=used_font, text="description")
        self.canvas = tk.Canvas(self, bd=1, bg="white", relief="solid")

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=9)
        self.grid_columnconfigure(0, weight=1)

        self.description.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.canvas.grid(row=1, column=0, sticky="nsew")


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

ranklist = ["Soort", "Familie", "Orde", "Klasse", "Stam", "Rijk"]
dataframes = {}
for i in ranklist:
    db = pd.read_excel("data/" + i + ".xlsx") # Unix
    #db = pd.read_excel("data\\" + i + ".xlsx") # Windows
    dataframes[i] = pd.DataFrame(db)

app = AppWindow()
app.mainloop()
# input() # debugging
