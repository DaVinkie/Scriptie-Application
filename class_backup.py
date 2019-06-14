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

        questionframe = tk.Frame(self, bg="white", #height=600, width=440,
                                    bd=1, relief=tk.SOLID)
        questionframe.grid(padx=5, pady=5, row=0, column=0, sticky="nsew")
        questionframe.grid_propagate(False)
        question = tk.Message(questionframe, bg="white") # width=430,
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
