from io import FileIO
from yaml import load
from random import shuffle
from random import randint

import utils

def fixed_day(dishes, week):
    for day in week:
        if day.fix_evening is not None:
            day.evening_dish = utils.get_element_by_name(dishes, day.fix_evening)
            dishes.remove(day.evening_dish)
        if day.fix_noon is not None:
            day.noon_dish = utils.get_element_by_name(dishes, day.fix_noon)
            dishes.remove(day.noon_dish)


def generate_week(dishes, side_dishes, week):
    fixed_day(dishes, week)
    for day in week:
        shuffle(dishes)
        if day.evening and day.evening_dish is None:
            dish = get_dish(day, dishes)
            day.evening_dish = dish
            if dish.need_side_dish:
                side_dish = get_random_element(side_dishes)
                day.evening_side_dish = side_dish
                side_dish.utilisability -= 1
                if side_dish.utilisability <= 0:
                    side_dishes.remove(side_dish)
            dishes.remove(dish)
        if day.noon and day.noon_dish is None:
            dish = get_dish(day, dishes)
            day.noon_dish = dish
            if dish.need_side_dish:
                side_dish = get_random_element(side_dishes)
                day.noon_side_dish = side_dish
                side_dish.utilisability -= 1
                if side_dish.utilisability <= 0:
                    side_dishes.remove(side_dish)
            dishes.remove(dish)


def get_dish(day, dishes):
    dish_is_ok = False
    dish = None
    while dish_is_ok is False:
        dish = get_random_element(dishes)
        dish_is_ok = True
        if dish.long_preparation and day.can_long_preparation is False:
            dish_is_ok = False
    return dish


def get_random_element(dishes):
    rand = randint(0, len(dishes) - 1)
    return dishes[rand]


if __name__ == '__main__':
    yaml = load(FileIO('./config.yaml', 'r'))
    dishes = utils.parse_dishes(yaml)
    side_dishes = utils.parse_side_dishes(yaml)
    week = utils.parse_calendar(yaml)
    rules = utils.parse_rules(yaml)
    generate_week(dishes, side_dishes, week)
    for day in week:
        print("{}, {}, {}".format(day.name, day.evening_dish, day.evening_side_dish))
        if day.noon:
            print("{}, {}, {}".format(day.name, day.noon_dish, day.noon_side_dish))