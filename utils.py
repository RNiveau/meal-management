from random import shuffle
from random import randint

from classes import Day
from classes import Dish
from classes import Rule
from classes import SideDish


def get_element_by_name(elements, name, default_value=None):
    tab = list(filter(lambda x: x.name == name, elements))
    if len(tab) > 0:
        return tab[0]
    return default_value


def get_random_element(elements):
    rand = randint(0, len(elements) - 1)
    return elements[rand]


def parse_dishes(yaml):
    dishes = []
    for dish in yaml['dishes']:
        dishes.append(Dish().parse_json(dish))
    shuffle(dishes)
    return dishes


def parse_calendar(yaml):
    week = []
    for day in yaml['calendar']:
        week.append(Day().parse_json(day))
    return week


def parse_side_dishes(yaml):
    side_dishes = []
    if 'side_dishes' in yaml:
        for side_dish in yaml['side_dishes']:
            side_dishes.append(SideDish().parse_json(side_dish))
        shuffle(side_dishes)
    return side_dishes


def parse_rules(yaml):
    rules = []
    if 'rules' in yaml:
        for key, value in yaml['rules'].items():
            rules.append(Rule(name=key, value=value))
    return rules
