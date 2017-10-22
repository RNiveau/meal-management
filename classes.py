import inspect


class Abstract:
    def parseJson(self, json):
        attrs = vars(self)
        for key, value in json.items():
            if key in attrs:
                setattr(self, key, value)
        return self

    def __str__(self):
        return str(vars(self))


class Dish(Abstract):
    def __init__(self):
        self.name = None
        self.meat = False
        self.need_side_dish = False
        self.fish = False
        self.long_preparation = False
        self.vegetarian = False


class SideDish(Abstract):
    def __init__(self):
        self.name = None
