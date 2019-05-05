

class Pizza:

    def __init__(self, base = "", topping = "", country = ""):
        self.base = PizzaBase(base)
        self.topping = PizzaTopping(topping)
        self.country = PizzaOrigin(country)

    def show_base(self):
        return self.base.base

    def set_base(self, base):
        self.base = PizzaBase(base)

    def show_topping(self):
        return self.topping.topping

    def show_country(self):
        return self.country.country

class PizzaTopping:

    def __init__(self, topping):
        self.topping = topping


class PizzaBase:

    def __init__(self, base):
        self.base = base


class PizzaOrigin:

    def __init__(self, country):
        self.country = country
