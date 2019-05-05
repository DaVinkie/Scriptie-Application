#!/usr/bin/python
import tkinter as tk
from pizzaclasses import *

class AppWindow(tk.Tk):

    def __init__(self):

        tk.Tk.__init__(self)
        self.title("LinneausDex")
        self.geometry("450x800")

        main = tk.Frame(self)
        main.grid(sticky = "nsew")

        frame = TestFrame(main, self)
        frame.grid(sticky = "nsew")

        frame.tkraise()

class TestFrame(tk.Frame):

    def __init__(self, master, controller):

        tk.Frame.__init__(self, master)

        ENTRY = Pizza()

        textframe = tk.Frame(self, height=600, width = 440, bg="white", bd=1,
                                relief=tk.SOLID)
        textframe.grid(padx=5, pady=5, row=0, column=0, sticky="nsew")
        textframe.grid_propagate(False)

        message = tk.Message(textframe, width = 430, bg = "white", text= qs["base"])
        message.grid(padx=5, pady=5, sticky="nsew")

        ans = tk.StringVar()

        radio1 = tk.Radiobutton(self, text="Thin", variable=ans, value = "thin")
        radio1.grid(row = 1, padx=5, pady=5)
        radio2 = tk.Radiobutton(self, text="Thicc", variable=ans, value = "thicc")
        radio2.grid(row = 2, padx=5, pady=5)

        button = tk.Button(self, text = "Submit",
                            command = lambda: self.buttonpress(message, ans, ENTRY))
        button.grid(row=3)

    def buttonpress(self, Message, StringVar, Pizza):
        answer = StringVar.get()
        Pizza.set_base(answer)
        Message.configure(text = qs["topping"])
        # label = tk.Message(self, width = 400, text = "Wow, you're using an actual test file. You are such an expert programmer very cool.")
        # label.grid(padx=5, pady=5, sticky="nsew")


base_Q = "Does the entry have thin or thick crust?"
topping_Q = "What kind of topping does the entry have?"
country_Q = "From which country does the entry originate?"
qs = {"base": base_Q, "topping": topping_Q, "country": country_Q}

cheese_pizza = Pizza("thick", "cheese", "italy")
pepperoni_pizza = Pizza("thick", "pepperoni", "italy")
mushroom_pizza = Pizza("thin", "mushroom", "france")
pizzas = [cheese_pizza, pepperoni_pizza, mushroom_pizza]

categories = ["base", "topping", "country"]



root = AppWindow()
root.mainloop()
