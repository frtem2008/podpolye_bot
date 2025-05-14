import random

import telebot

from src.messages import chanced, is_conditional, chancedNames
from src.middleware.UserHandlers import bot_logger


def send_by_chance(bot: telebot.TeleBot, chat_id: int, name: str, **kwargs):
    chance, text = chanced(name, **kwargs)
    if random.uniform(0, 1) <= chance:
        bot.send_message(chat_id=chat_id, text=text)
        bot_logger.info(f'Sent chanced message {text} to {chat_id}')
        return True
    return False


def unconditionalHandler(bot: telebot.TeleBot, message: telebot.types.Message):
    for message_name in chancedNames():
        if not is_conditional(message_name):
            sent = send_by_chance(bot, message.chat.id, message_name)
            if sent:
                break

def avAsleepHandler(bot: telebot.TeleBot, message: telebot.types.Message):
    send_by_chance(bot, message.chat.id, 'av sleep')
