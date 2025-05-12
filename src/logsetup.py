import datetime
import logging
import os

log_path = f'../logs/{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
if not os.path.exists(log_path):
    os.makedirs(log_path)
    logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)


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

class Loggable:
    def __init__(self, suffix: str) -> None:
        self.log = new_logger(f'{self.__class__.__name__} {suffix}', logging.DEBUG)
        self.log.info("Initialized")