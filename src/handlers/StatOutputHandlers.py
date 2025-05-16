import telebot

from src.messages import messages
from src.middleware.TitleHandler import bot_logger
from src.models import database


def printStatHandler(mes: telebot.types.Message, bot: telebot.TeleBot) -> None:
    statistic = database.get_stats_by_id(mes.from_user.id)
    bot.send_message(mes.chat.id, messages.format_normal("stat", user=mes.from_user.username, message_count=statistic.message_count, rofl_count=statistic.rofl_count))
    bot_logger.debug(f"user {mes.from_user.username} print stat")
