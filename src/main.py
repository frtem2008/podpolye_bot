import logging

import log_setup
import bot
from src.database import database
from src.handlers.handlers import Ping, UserAdder

if __name__ == '__main__':
    database.init_db()

    main_logger = log_setup.new_logger('main', logging.DEBUG)
    main_logger.info("Bot started")

    bot.add_handler(Ping())
    bot.add_handler(UserAdder())


    bot.bot.polling(none_stop=True, interval=0)
