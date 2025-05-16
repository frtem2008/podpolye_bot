import bot
import schedule
import time

import logsetup
from src.models import database
from multiprocessing import *
from res.credentials import PODPOLYE_ID
from src import messages

main_logger = logsetup.new_logger('schedule', logging.DEBUG)

def stat_day_update():
    users_stat = database.get_all_statistics()
    text_mes = str()
    for user in users_stat:
        text_mes += messages.format_normal("stat", user=user.username, count_mes=user.count_messege, count_rofl=user.count_rolfs) + messages.get_text_sep()
        database.zeroing_statistics(user.id)

    bot.bot.send_message(PODPOLYE_ID, text_mes)
    main_logger.debug('stat_day_update')


def start_schedule():
    schedule.every().day.at("00:00").do(stat_day_update)

    while True:
        schedule.run_pending()
        time.sleep(1)


def start_process():
    p1 = Process(target=P_schedule.start_schedule, args=()).start()
    main_logger.debug('Scheduled process ')



