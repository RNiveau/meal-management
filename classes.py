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
        self.cold_meat = False


class SideDish(Abstract):
    def __init__(self):
        self.name = None
        self.utilisability = 1


class Day(Abstract):
    def __init__(self):
        self.name = None
        self.evening = False
        self.noon = False
        self.can_long_preparation = False
        self.fix_evening = None
        self.fix_noon = None
        self.evening_dish = None
        self.noon_dish = None
        self.evening_side_dish = None
        self.noon_side_dish = None


class Rule(Abstract):
    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.value = kwargs.get('value')