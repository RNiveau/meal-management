from io import FileIO
from yaml import load
from random import shuffle
from random import randint

from classes import Day
from classes import Dish
from classes import SideDish


def get_dish_by_name(dishes, name):
    return next(iter(filter(lambda x: x.name == name, dishes)))


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
    for side_dish in yaml['side_dishes']:
        side_dishes.append(SideDish().parse_json(side_dish))
    shuffle(side_dishes)
    return side_dishes


def fixed_day(dishes, week):
    for day in week:
        if day.fix_evening is not None:
            day.evening_food = get_dish_by_name(dishes, day.fix_evening)
        if day.fix_noon is not None:
            day.noon_food = get_dish_by_name(dishes, day.fix_noon)


def generate_week(dishes, side_dishes, week):
    fixed_day(dishes, week)
    for day in week:
        if day.evening and day.evening_food is None:
            rand = randint(0, len(dishes))
            day.evening_food = dishes[rand]



if __name__ == '__main__':
    yaml = load(FileIO('./config.yaml', 'r'))
    dishes = parse_dishes(yaml)
    side_dishes = parse_side_dishes(yaml)
    week = parse_calendar(yaml)
    generate_week(dishes, side_dishes, week)
    for day in week:
        print("{}, {}".format(day.name, day.evening_food))