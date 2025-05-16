import datetime
import logging
import os

import telebot

from src.models import models

log_path = f'logs/{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'

LOG_LEVEL = logging.INFO

if not os.path.exists(log_path):
    os.makedirs(log_path)
    logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)
    logging.getLogger('Log setup').info(f'Created log directory: {log_path}')


# TODO: Add logger for each trigger
def new_logger(name: str, level=LOG_LEVEL) -> logging.Logger:
    log = logging.Logger(name)
    log.setLevel(level)
    formatter = logging.Formatter('%(name)s (%(asctime)s)[%(levelname)s]: %(message)s')
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    log.addHandler(streamHandler)

    file_handler = logging.FileHandler(f'{log_path}/bot.log')
    file_handler.setFormatter(formatter)
    log.addHandler(file_handler)

    return log


def user_fmt(to_format: telebot.types.User | models.Users) -> str:
    if hasattr(to_format, 'user_id'):
        return f'@{to_format.username}({to_format.user_id})'
    return f'@{to_format.username}({to_format.id})'
