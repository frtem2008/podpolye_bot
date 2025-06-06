import re

import telebot

from src.logs import logsetup
from src.logs.logsetup import user_fmt
from src.messages import messages
from src.models import database

log = logsetup.new_logger('Stat collector')


def statCollector(bot: telebot.TeleBot, message: telebot.types.Message) -> None:
    user_id = message.from_user.id

    user = database.get_stats_by_id(user_id)

    if not user:
        log.debug(message.from_user)
        database.create_user_stats(user_id, message.from_user.username)
        log.info(f"Created stats for {user_fmt(message.from_user)}")

    database.inc_message_count(user_id)
    log.debug(f"User {user_fmt(message.from_user)} message count incremented")

    if not message.text:
        return

    # TODO: compile rofl triggers with message triggers on json reload
    for trigger in messages.rofl_triggers():
        log.debug(f"Checking rofl trigger {trigger} for message text: {message.text}")
        if re.search(re.compile(trigger), message.text):
            database.inc_rofl_count(user_id)
            log.debug(f"user {message.from_user.username} rofl++")
