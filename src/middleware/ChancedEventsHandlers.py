import random
import re

import telebot

from src import messages
from src.middleware.UserHandlers import bot_logger


# TODO: политика проверки триггеров (any | all)

def send_by_chance(bot: telebot.TeleBot, message: telebot.types.Message, name: str, **kwargs) -> bool:
    chance, text, reply = messages.format_chanced(name, **kwargs)
    if random.uniform(0, 1) <= chance:
        if reply:
            bot.reply_to(message, text)
        else:
            bot.send_message(message.chat.id, text)
        bot_logger.info(f'Sent chanced message {text} to {message.chat.id}')
        return True

    return False


def check_triggers(name: str, message: telebot.types.Message):
    bot_logger.info(f'Checking triggers for {name} on {message.text}')
    triggered = []
    triggers = messages.triggers(name)
    if 'text matches' in triggers:
        if re.search(triggers['regex'], message.text):
            bot_logger.info(f'Text match triggered on {message.text}')
            triggered.append(True)
        else:
            bot_logger.info(f'Text match not triggered on {message.text}')

    return all(triggered) if triggered else False


def send_by_trigger(bot: telebot.TeleBot, message: telebot.types.Message, name: str, **kwargs) -> bool:
    if check_triggers(name, message):
        send_by_chance(bot, message, name, **kwargs)
        return True
    return False


def message_chanse_trigger_hanlder(bot: telebot.TeleBot, message: telebot.types.Message) -> None:
    if not message.text:
        return

    for message_name in messages.chancedNames():
        if messages.is_conditional(message_name) == False:
            sent = send_by_chance(bot, message, message_name)
        else:
            sent = send_by_trigger(bot, message, message_name)

        if sent:
            return
