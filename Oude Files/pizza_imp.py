#!/usr/bin/python
import tkinter as tk
import random

class AppWindow(tk.Tk):

    def __init__(self):

        tk.Tk.__init__(self)
        self.title("PizzaDex - DEV")
        self.geometry("450x800")

        main = tk.Frame(self)
        main.grid(sticky = "nsew")

        frame = TestFrame(main, self)
        frame.grid(sticky = "nsew")

        frame.tkraise()

class TestFrame(tk.Frame):

    def __init__(self, master, controller):

        tk.Frame.__init__(self, master)

        textframe = tk.Frame(self, height=600, width = 440, bg="white", bd=1,
                                relief=tk.SOLID)
        textframe.grid(padx=5, pady=5, row=0, column=0, sticky="nsew")
        textframe.grid_propagate(False)

        message = tk.Message(textframe, width = 430, bg = "white", text= qs["base"])
        message.grid(padx=5, pady=5, sticky="nsew")

        ans = tk.StringVar()

        options = multiple_choice("bellpepper", 2)
        for option in options:
            b = tk.Radiobutton(self, text = option, variable = ans, value = option,
                                anchor=tk.N)
            b.grid(sticky="ew")


        button = tk.Button(self, text = "Submit",
                            command = lambda: self.buttonpress(message, ans))
        button.grid(row=3)

    def buttonpress(self, Message, StringVar):
        answer = StringVar.get()
        Message.configure(text = qs["topping"])
        # label = tk.Message(self, width = 400, text = "Wow, you're using an actual test file. You are such an expert programmer very cool.")
        # label.grid(padx=5, pady=5, sticky="nsew")


base_Q = "Does the pizza have thin or thick crust?"
sauce_Q = "What kind of sauce makes up the base?"
meat_Q = "Is there any kind of meat on the pizza?"
topping_Q = "What kind of topping does the entry have?"
country_Q = "From which country does the entry originate?"
qs = {"base": base_Q, "sauce": sauce_Q, "meat":meat_Q, "topping": topping_Q, "country": country_Q}

import random

class Rank:
    def __init__(self, name, type, super):
        self.name = name
        self.type = type
        self.super = super

entries = [
    ("pepperoni", "pizza", "meat"),
    ("chicken", "pizza", "meat"),
    ("doner", "pizza", "meat"),
    ("sausage", "pizza", "meat"),
    ("bacon", "pizza", "meat"),
    ("mushroom", "pizza", "veg"),
    ("pepper", "pizza", "veg"),
    ("onion", "pizza", "veg"),
    ("bellpepper", "pizza", "veg"),
    ("olives", "pizza", "veg"),
    ("mozzarella", "pizza", "cheese"),
    ("cheddar", "pizza", "cheese"),
    ("feta", "pizza", "cheese"),
    ("gorgonzola", "pizza", "cheese"),
    ("bluecheese", "pizza", "cheese"),
    ("meat", "pizzatype", "barbecuesauce"),
    ("veg", "pizzatype", "tomatosauce"),
    ("cheese", "pizzatype", "tomatosauce"),
    ("meat", "pizzatype", "sauce"),
    ("tomatosauce", "sauce", "crust"),
    ("barbecuesauce", "sauce", "crust"),
    ("crust", "base", None)
]
db = {}

for i in range(len(entries)):
    db[str(i)] = Rank(entries[i][0], entries[i][1], entries[i][2])

def get_answer(input):
    for d in db:
        if db[d].name == input:
            answer = db[d].super
    return answer

def multiple_choice(input, n):
    answer = get_answer(input)
    for d in db:
        if db[d].name == input:
            type = db[d].type
    viables = list(set([db[d].super for d in db if db[d].type == type]))
    viables.remove(answer)
    possibles = random.choices(viables, k=(n-1))
    possibles.append(answer)
    random.shuffle(possibles)
    return possibles


root = AppWindow()
root.mainloop()
