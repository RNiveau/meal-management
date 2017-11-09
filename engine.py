import utils


class Engine:
    def __init__(self, **kwargs):
        self.rules = kwargs.get("rules")
        self.dishes = kwargs.get("dishes")
        self.side_dishes = kwargs.get("side_dishes")
        self.week = kwargs.get("week")
        self._dishes_poll = []

    def setup(self):
        vegetarians = self._get_vegetarian_dishes()
        fishes = self._get_fish_dishes()
        min_vegetarian = utils.get_element_by_name(self.rules, 'min_vegetarian')
        min_fish = utils.get_element_by_name(self.rules, 'min_fish')
        max_cold_meat = utils.get_element_by_name(self.rules, 'max_cold_meat')

        dishes_number, long_preparation = self._get_dishes_number_and_long_preparation()
        manage long_preparation in rule
        self._min_rules(min_vegetarian.value, vegetarians)
        self._min_rules(min_fish.value, fishes)
        self._set_fix_days()

        for i in range(len(self._dishes_poll) - 1, dishes_number):
            dish_is_ok = False
            while dish_is_ok is False:
                dish = utils.get_random_element(self.dishes)
                dish_is_ok = True
                if dish.long_preparation and long_preparation == 0:
                    dish_is_ok = False
                elif dish.long_preparation:
                    long_preparation -= 1
                self._dishes_poll.append(dish)
                self.dishes.remove(dish)

        for dish in self._dishes_poll:
            print(dish)

        return self

    def _get_vegetarian_dishes(self):
        return filter(lambda x: x.vegetarian, self.dishes)

    def _get_fish_dishes(self):
        return filter(lambda x: x.fish, self.dishes)

    def _min_rules(self, mini, tab):
        for i in range(0, mini):
            if len(tab) > 0:
                element = utils.get_random_element(tab)
                self._dishes_poll.append(element)
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
                self._dishes_poll.append(dish)
                self.dishes.remove(dish)
            if day.fix_evening is not None:
                dish = utils.get_element_by_name(self.dishes, day.fix_evening)
                self._dishes_poll.append(dish)
                self.dishes.remove(dish)
