from src import bot
from src.logs import logsetup
from src.middleware import TitleHandler
from src.models import database
from src.scheduled.resetStats import start_schedule
import threading

if __name__ == '__main__':
    database.init_db()
    TitleHandler.import_users()

    main_logger = logsetup.new_logger('Main')
    main_logger.info("Bot started")

    p1 = threading.Thread(target=start_schedule, args=(), daemon=True).start()

    bot.bot.polling(none_stop=True, interval=0, timeout=60)
