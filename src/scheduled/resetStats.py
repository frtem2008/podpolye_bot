import time

import schedule

from res.credentials import PODPOLYE_ID
from src import bot
from src.logs import logsetup
from src.messages import messages
from src.models import database

log = logsetup.new_logger('Stats reset')


# TODO: Add better and unified support for scheduling

def reset_daily_stats():
    users_stat = database.get_all_stats()
    text_mes = messages.daily_statistics_message() + messages.text_separator()
    for user in users_stat:
        text_mes += messages.format_normal(
            "stat", user=user.username, message_count=user.message_count, rofl_count=user.rofl_count
        ) + messages.text_separator()
        database.reset_user_stats(user.user_id)
    # TODO: Support for more groups (read chats to send daily stats from messages.json)
    bot.bot.send_message(PODPOLYE_ID, text_mes)
    log.info('Daily stats reset')


def start_schedule():
    schedule.every().day.at("00:00").do(reset_daily_stats)

    while True:
        schedule.run_pending()
        time.sleep(1)
