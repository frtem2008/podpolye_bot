import telebot

from src.logs import logsetup
from src.messages import messages
from src.logs.logsetup import user_fmt
from src.models import database

log = logsetup.new_logger('Print stat handler')


def printStatHandler(mes: telebot.types.Message, bot: telebot.TeleBot) -> None:
    statistic = database.get_stats_by_id(mes.from_user.id)
    stats = messages.format_normal("stat", user=mes.from_user.username, message_count=statistic.message_count, rofl_count=statistic.rofl_count)
    bot.send_message(mes.chat.id, stats)
    log.info(f"Printed {user_fmt(mes.from_user)} stats: {stats}")
