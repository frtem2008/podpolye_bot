import datetime
import logging
import os

# for telebot itself
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)

log_path = f'../logs/{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
os.makedirs(log_path)

def new_logger(name: str, level: int) -> logging.Logger:
    log = logging.Logger(name)
    log.setLevel(level)
    formatter = logging.Formatter('%(name)s (%(asctime)s)[%(levelname)s]: %(message)s')
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    log.addHandler(streamHandler)

    file_handler = logging.FileHandler(f'{log_path}/{name}.log')
    file_handler.setFormatter(formatter)
    log.addHandler(file_handler)

    return log