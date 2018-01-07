from io import FileIO
import logging

from yaml import load
from messager_client import MessagerClient

import utils
from engine import Engine

if __name__ == '__main__':
    logging.basicConfig(filename='generate.log', level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')
    logger = logging.getLogger(__name__)
    yaml = load(FileIO('./config.yaml', 'r'))
    app = load(FileIO('./app.yaml', 'r'))
    dishes = utils.parse_dishes(yaml)
    side_dishes = utils.parse_side_dishes(yaml)
    week = utils.parse_calendar(yaml)
    rules = utils.parse_rules(yaml)
    engine = Engine(rules=rules, dishes=dishes, side_dishes=side_dishes, week=week).setup()
    week = engine.generate_week()
    logger.info("Generated week:")
    message = ""
    for day in week:
        if day.noon:
            message += "{} midi: {}".format(day.name, day.noon_dish.name)
            if day.noon_dish.need_side_dish:
                message += " avec {}".format(day.noon_side_dish.name)
            message += "\n"
        if day.evening:
            message += "{} soir: {}".format(day.name, day.evening_dish.name)
            if day.evening_dish.need_side_dish and day.evening_side_dish is not None:
                message += " avec {}".format(day.evening_side_dish.name)
            elif day.evening_dish.need_side_dish:
                message += " avec ???"
            message += "\n"
    logger.info(message)
    client = MessagerClient(app['facebook_id'])
    client.send_message(app['sender_id'][0], message)
    client.send_message(app['sender_id'][1], message)