import inspect


class Abstract:
    def parse_json(self, json):
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


class Day(Abstract):
    def __init__(self):
        self.name = None
        self.evening = False
        self.noon = False
        self.can_long_preparation = False
        self.fix_evening = None
        self.fix_noon = None
        self.evening_food = None
        self.noon_food = None
