import json
import logging
from random import shuffle
from os import path

import utils
from classes import Rule

END_SAVE_FILE = '.last_week.json'


class Engine:
    def __init__(self, **kwargs):
        self.rules = kwargs.get("rules")
        self.dishes = kwargs.get("dishes")
        self.side_dishes = kwargs.get("side_dishes")
        self.week = kwargs.get("week")
        self.config_file = kwargs.get("config_file")
        self._save_file = path.basename(self.config_file) + END_SAVE_FILE
        self._dishes_poll = []
        self._dishes_number = 0
        self._long_preparation = 0
        self._max_cold_meat = 0
        self._logger = logging.getLogger(__name__)

    def setup(self):
        vegetarians = self._get_vegetarian_dishes()
        fishes = self._get_fish_dishes()
        min_vegetarian = utils.get_element_by_name(self.rules, 'min_vegetarian', Rule(value=0))
        min_fish = utils.get_element_by_name(self.rules, 'min_fish', Rule(value=0))
        max_cold_meat = utils.get_element_by_name(self.rules, 'max_cold_meat', Rule(value=7))

        self._max_cold_meat = max_cold_meat.value
        self._dishes_number, self._long_preparation = self._get_dishes_number_and_long_preparation()
        self._min_rules(min_vegetarian.value, vegetarians)
        self._min_rules(min_fish.value, fishes)
        self._set_fix_days()

        if path.exists(self._save_file):
            with open("./{}".format(self._save_file), 'r') as file:
                save = json.loads(file.read())
                self.dishes = list(filter(lambda x: x.name not in save, self.dishes))

        for i in range(len(self._dishes_poll) - 1, self._dishes_number):
            dish_is_ok = False
            while dish_is_ok is False:
                dish = utils.get_random_element(self.dishes)
                dish_is_ok = True
                if dish.long_preparation and self._long_preparation <= 0:
                    dish_is_ok = False
                elif dish.cold_meat and self._max_cold_meat <= 0:
                    dish_is_ok = False
                else:
                    if dish.long_preparation:
                        self._long_preparation -= 1
                    if dish.cold_meat:
                        self._max_cold_meat -= 1
            self._dishes_poll.append(dish)
            self.dishes.remove(dish)
        self._logger.info("Dishes poll:")
        for dish in self._dishes_poll:
            self._logger.info(dish)
        return self

    def generate_week(self):
        self._generate_fix_day()
        for day in self.week:
            shuffle(self._dishes_poll)
            if day.evening and day.evening_dish is None:
                self._generate_dish(day, self._dishes_poll, self.side_dishes, 'evening')
            if day.noon and day.noon_dish is None:
                self._generate_dish(day, self._dishes_poll, self.side_dishes, 'noon')
        return self.week

    def write_week(self):
        with open("./{}".format(self._save_file), 'w+') as file:
            file.write("[")
            for day in self.week:
                if day.evening and day.fix_evening is None:
                    file.write('"{}",'.format(day.evening_dish.name))
                if day.noon and day.fix_noon is None:
                    file.write('"{}",'.format(day.noon_dish.name))
            file.write('""]')

    def _generate_dish(self, day, dishes, side_dishes, part_day):
        dish = self._get_dish(day, dishes)
        side_dish = None
        if dish.need_side_dish:
            side_dish = utils.get_random_element(side_dishes)
            side_dish.utilisability -= 1
            if side_dish.utilisability <= 0:
                side_dishes.remove(side_dish)
        dishes.remove(dish)
        if part_day == 'evening':
            day.evening_dish = dish
            day.evening_side_dish = side_dish
        else:
            day.noon_dish = dish
            day.noon_side_dish = side_dish

    def _get_dish(self, day, dishes):
        dish_is_ok = False
        dish = None
        while dish_is_ok is False:
            dish = utils.get_random_element(dishes)
            dish_is_ok = True
            if dish.long_preparation and day.can_long_preparation is False:
                dish_is_ok = False
        return dish

    def _get_vegetarian_dishes(self):
        return list(filter(lambda x: x.vegetarian, self.dishes))

    def _get_fish_dishes(self):
        return list(filter(lambda x: x.fish, self.dishes))

    def _min_rules(self, mini, tab):
        for i in range(0, mini):
            if len(tab) > 0:
                dish_is_ok = False
                while dish_is_ok is False:
                    element = utils.get_random_element(tab)
                    dish_is_ok = True
                    if element.long_preparation and self._long_preparation <= 0:
                        dish_is_ok = False
                    elif element.long_preparation:
                        self._long_preparation -= 1
                self._dishes_poll.append(element)
                self.dishes.remove(element)
                tab.remove(element)

    def _get_dishes_number_and_long_preparation(self):
        number = 0
        long_preparation = 0
        for day in self.week:
            if day.can_long_preparation:
                long_preparation += 1
            if day.evening:
                number += 1
            if day.noon:
                number += 1
        return number, long_preparation


    def _set_fix_days(self):
        for day in self.week:
            if day.fix_noon is not None:
                dish = utils.get_element_by_name(self.dishes, day.fix_noon)
                if dish.long_preparation:
                    self._long_preparation -= 1
                if dish.cold_meat:
                    self._max_cold_meat -= 1
                self._dishes_poll.append(dish)
                self.dishes.remove(dish)
            if day.fix_evening is not None:
                dish = utils.get_element_by_name(self.dishes, day.fix_evening)
                if dish.long_preparation:
                    self._long_preparation -= 1
                if dish.cold_meat:
                    self._max_cold_meat -= 1
                self._dishes_poll.append(dish)
                self.dishes.remove(dish)

    def _generate_fix_day(self):
        for day in self.week:
            if day.fix_evening is not None:
                day.evening_dish = utils.get_element_by_name(self._dishes_poll, day.fix_evening)
                self._dishes_poll.remove(day.evening_dish)
            if day.fix_noon is not None:
                day.noon_dish = utils.get_element_by_name(self._dishes_poll, day.fix_noon)
                self._dishes_poll.remove(day.noon_dish)
