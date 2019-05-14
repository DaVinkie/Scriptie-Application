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

def get_classification(input, chain):
    for d in db:
        if db[d].super == None:
            return chain
        elif db[d].name == input:
            chain.append(db[d].super)
            get_classification(db[d].super, chain)

input = "sausage"
print(get_classification(input, [input]))
