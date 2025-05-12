import logging

import bot
import logsetup
from src.middleware import UserHandlers
from src.models import database

if __name__ == '__main__':
    database.init_db()
    UserHandlers.import_users()

    main_logger = logsetup.new_logger('main', logging.DEBUG)
    main_logger.info("Bot started")
    bot.bot.polling(none_stop=True, interval=0)
