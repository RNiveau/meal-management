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
            day.evening_dish = get_dish_by_name(dishes, day.fix_evening)
            dishes.remove(day.evening_dish)
        if day.fix_noon is not None:
            day.noon_dish = get_dish_by_name(dishes, day.fix_noon)
            dishes.remove(day.noon_dish)


def generate_week(dishes, side_dishes, week):
    fixed_day(dishes, week)
    for day in week:
        if day.evening and day.evening_dish is None:
            dish = get_dish(day, dishes)
            day.evening_dish = dish
            dishes.remove(dish)
        if day.noon and day.noon_dish is None:
            dish = get_dish(day, dishes)
            day.noon_dish = dish
            dishes.remove(dish)


def get_dish(day, dishes):
    dish_is_ok = False
    dish = None
    while dish_is_ok is False:
        dish = get_random_dish(dishes)
        dish_is_ok = True
        if dish.long_preparation and day.can_long_preparation is False:
            dish_is_ok = False
    return dish


def get_random_dish(dishes):
    rand = randint(0, len(dishes) - 1)
    return dishes[rand]


if __name__ == '__main__':
    yaml = load(FileIO('./config.yaml', 'r'))
    dishes = parse_dishes(yaml)
    side_dishes = parse_side_dishes(yaml)
    week = parse_calendar(yaml)
    generate_week(dishes, side_dishes, week)
    for day in week:
        print("{}, {}".format(day.name, day.evening_dish))
        if day.noon:
            print("{}, {}".format(day.name, day.noon_dish))