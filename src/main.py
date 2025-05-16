import logging

import bot
import logsetup
from src.middleware import UserHandlers
from src.models import database
from src.schedule_statistics import start_schedule
from multiprocessing import *


# TODO возвращаемые значения для всех методов

def start_bot():
    bot.bot.polling(none_stop=True, interval=0, timeout=60)


if __name__ == '__main__':
    database.init_db()
    UserHandlers.import_users()

    main_logger = logsetup.new_logger('main', logging.DEBUG)
    main_logger.info("Bot started")

    p2 = Process(target=start_bot, args=()).start()
    start_schedule()

