import random
import re

import telebot

from src.logs import logsetup
from src.messages import messages

log = logsetup.new_logger('Triggered message handler')


# TODO: политика проверки триггеров (any | all)
def check_triggers(name: str, message: telebot.types.Message) -> bool:
    log.debug(f'Checking triggers for {name} on {message.text}')
    if not messages.has_triggers(name):
        log.debug(f'Message {name} has no triggers')
        return True

    triggered = []
    triggers = messages.triggers(name)

    if 'text matches' in triggers:
        if re.search(triggers['regex'], message.text):
            log.debug(f'Text match triggered on {message.text}')
            triggered.append(True)
        else:
            log.debug(f'Text match not triggered on {message.text}')
    # TODO: add more triggers

    return all(triggered) if triggered else False


def send_by_chance(bot: telebot.TeleBot, message: telebot.types.Message, name: str, **kwargs) -> None:
    chance, text, reply = messages.format_random(name, **kwargs)
    if random.uniform(0, 1) <= chance:
        if reply:
            bot.reply_to(message, text)
        else:
            bot.send_message(message.chat.id, text)
        log.info(f'Sent random message {text} with probability of {chance} to {message.chat.id}')


def triggeredMessageHandler(bot: telebot.TeleBot, update: telebot.types.Update) -> None:
    message = update.message
    if not message or not message.text:
        return

    for message_name in messages.random_messages_names():
        if check_triggers(message_name, message):
            send_by_chance(bot, message, message_name)
