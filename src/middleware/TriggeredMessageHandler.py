import random
import re

import telebot

from src import messages
from src.middleware.UserHandlers import bot_logger


# TODO: политика проверки триггеров (any | all)
def check_triggers(name: str, message: telebot.types.Message) -> bool:
    bot_logger.info(f'Checking triggers for {name} on {message.text}')
    if not messages.has_triggers(name):
        bot_logger.info(f'Message {name} has no triggers')
        return True

    triggered = []
    triggers = messages.triggers(name)

    if 'text matches' in triggers:
        if re.search(triggers['regex'], message.text):
            bot_logger.info(f'Text match triggered on {message.text}')
            triggered.append(True)
        else:
            bot_logger.info(f'Text match not triggered on {message.text}')
    # TODO: add more triggers

    return all(triggered) if triggered else False


def send_by_chance(bot: telebot.TeleBot, message: telebot.types.Message, name: str, **kwargs) -> None:
    chance, text, reply = messages.format_random(name, **kwargs)
    if random.uniform(0, 1) <= chance:
        if reply:
            bot.reply_to(message, text)
        else:
            bot.send_message(message.chat.id, text)
        bot_logger.info(f'Sent chanced message {text} to {message.chat.id}')


def triggeredMessageHandler(bot: telebot.TeleBot, update: telebot.types.Update) -> None:
    message = update.message
    if not message or not message.text:
        return

    for message_name in messages.random_messages_names():
        if check_triggers(message_name, message):
            send_by_chance(bot, message, message_name)
