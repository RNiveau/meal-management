from io import FileIO
import argparse
import logging

from yaml import load
from messager_client import MessagerClient

import utils
from engine import Engine

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create meal for a week")
    parser.add_argument('--config', action="store", dest="config_file", default="./config.yaml" ,type=str)
    argument = parser.parse_args()

    logging.basicConfig(filename='generate.log', level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')

    logger = logging.getLogger(__name__)
    yaml = load(FileIO(argument.config_file, 'r'))
    app = load(FileIO('./app.yaml', 'r'))
    dishes = utils.parse_dishes(yaml)
    side_dishes = utils.parse_side_dishes(yaml)
    week = utils.parse_calendar(yaml)
    rules = utils.parse_rules(yaml)
    engine = Engine(rules=rules, dishes=dishes, side_dishes=side_dishes, week=week).setup()
    week = engine.generate_week()
    logger.info("Generated week:")
    message = "{}\n".format(yaml['hello'])
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
    for sender in app['sender_id']:
        client.send_message(sender, message)
