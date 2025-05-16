import re

import telebot

from src.messages import messages
from src.middleware.TitleHandler import bot_logger, user_fmt
from src.models import database


def statCollector(bot: telebot.TeleBot, message: telebot.types.Message) -> None:
    user_id = message.from_user.id

    user = database.get_stats_by_id(user_id)

    if not user:
        database.create_user_stats(user_id, message.from_user.username)
        bot_logger.debug(f"created stats for {user_fmt(message.from_user)}")

    database.inc_message_count(user_id)
    bot_logger.debug(f"user {user_fmt(message.from_user)} message")

    if not message.text:
        return

    for trigger in messages.rofl_triggers():
        bot_logger.debug(f"trigger {trigger}, text: {message.text}")
        if re.search(re.compile(trigger), message.text):
            database.inc_rofl_count(user_id)
            bot_logger.debug(f"user {message.from_user.username} rofl++")
