from io import FileIO
import logging

from yaml import load

import utils
from engine import Engine

if __name__ == '__main__':
    logging.basicConfig(filename='generate.log', level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')
    logger = logging.getLogger(__name__)
    yaml = load(FileIO('./config.yaml', 'r'))
    dishes = utils.parse_dishes(yaml)
    side_dishes = utils.parse_side_dishes(yaml)
    week = utils.parse_calendar(yaml)
    rules = utils.parse_rules(yaml)
    engine = Engine(rules=rules, dishes=dishes, side_dishes=side_dishes, week=week).setup()
    week = engine.generate_week()
    logger.info("Generated week:")
    for day in week:
        logger.info("{}, {}, {}".format(day.name, day.evening_dish, day.evening_side_dish))
        if day.noon:
            logger.info("{}, {}, {}".format(day.name, day.noon_dish, day.noon_side_dish))
