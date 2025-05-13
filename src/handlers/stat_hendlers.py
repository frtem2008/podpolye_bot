from email import message

import telebot
from src.middleware.UserHandlers import user_fmt, bot_logger
from src.models import database
from untils import word_in_mes


def statictic_hendlers(message: telebot.types.Message, bot: telebot.TeleBot) -> None:
    users = [i.id for i in database.get_statistics()]
    user_id = message.from_user.id

    if message.from_user.id not in users:
        database.create_user_statistics(user_id, message.from_user.username)
        bot_logger.debug(f"user {message.from_user.username} created statistics")

    database.count_mes_pl(user_id)
    bot_logger.debug(f"user {message.from_user.username} messege++")

    if word_in_mes("гойда", str(message.text)):
        database.count_goida_pl(user_id)
        bot_logger.debug(f"user {message.from_user.username} goida++")


def print_stat_hendlers(mes: telebot.types.Message, bot: telebot.TeleBot):
    text_pattern = "{} роль {}\n\tколичество сообщений: {}\n\tКоличество гойд: {}"

