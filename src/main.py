from src import bot
from src.logs import logsetup
from src.middleware import TitleHandler
from src.models import database
from src.scheduled.resetStats import start_schedule

if __name__ == '__main__':
    database.init_db()
    TitleHandler.import_users()

    main_logger = logsetup.new_logger('Main')
    main_logger.info("Bot started")

    # TODO: scheduling does not work with bot updates
    bot.bot.polling(none_stop=True, interval=0, timeout=60)
    # TODO: start schedule is now NEVER called. Invent a new way of scheduling
    start_schedule()
