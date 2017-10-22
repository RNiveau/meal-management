from io import FileIO
from yaml import load

from classes import Dish
from classes import SideDish


def parse_dishes(yaml):
    dishes = []
    for dish in yaml['dishes']:
        dishes.append(Dish().parseJson(dish))
    return dishes


def parse_side_dishes(yaml):
    side_dishes = []
    for side_dish in yaml['side_dishes']:
        side_dishes.append(SideDish().parseJson(side_dish))
    return side_dishes


if __name__ == '__main__':
    yaml = load(FileIO('./config.yaml', 'r'))
    dishes = parse_dishes(yaml)
    sideDishes = parse_side_dishes(yaml)
    print(dishes)
    print(sideDishes)