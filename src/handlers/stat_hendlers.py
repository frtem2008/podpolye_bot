from email import message

import telebot
from src.middleware.UserHandlers import user_fmt, bot_logger
from src.models import database
from src import messages



def staticticHendlers(message: telebot.types.Message, bot: telebot.TeleBot) -> None:
    users = [i.id for i in database.get_statistics_by_id()]
    user_id = message.from_user.id

    if message.from_user.id not in users:
        database.create_user_statistics(user_id, message.from_user.username)
        bot_logger.debug(f"user {message.from_user.username} created statistics")

    database.count_mes_pl(user_id)
    bot_logger.debug(f"user {message.from_user.username} messege++")



def printStatHendlers(mes: telebot.types.Message, bot: telebot.TeleBot):
    statistic = database.get_statistics_by_id(mes.from_user.id)
    bot.send_message(mes.chat.id, messages.format_normal("stat", user=mes.from_user.username, count_mes=statistic.count_messege, count_rofl=statistic.count_goida))



