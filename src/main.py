import logging

import bot
import logsetup
from src.database import database
from src.handlers.RoleHandlers import RoleCreator, RoleDeleter, UserRoller, UserUnroller, PingRole, SelfRoller, SelfUnroller
from src.handlers.TitleHandler import TitleAdder
from src.handlers.handlers import Ping

if __name__ == '__main__':
    database.init_db()

    main_logger = logsetup.new_logger('main', logging.DEBUG)
    main_logger.info("Bot started")

    bot.add_handler(Ping())
    bot.add_handler(TitleAdder())
    bot.add_handler(RoleCreator())
    bot.add_handler(RoleDeleter())
    bot.add_handler(SelfRoller())
    bot.add_handler(SelfUnroller())
    bot.add_handler(UserRoller())
    bot.add_handler(UserUnroller())
    bot.add_handler(PingRole())

    bot.bot.polling(none_stop=True, interval=0)
