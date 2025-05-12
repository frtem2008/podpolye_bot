import logging

import telebot
import handlers.handlers
from res.credentials import BOT_TOKEN
from src import logsetup

bot = telebot.TeleBot(BOT_TOKEN)
bot_logger = logsetup.new_logger('main', logging.DEBUG)
bot_handlers = []


def add_handler(handler: handlers.handlers.Handler):
    bot_handlers.append(handler)
    handler.bot = bot


@bot.message_handler()
def handle_message(message: telebot.types.Message):
    for handler in bot_handlers:
        if handler.can_handle(message):
            handler.handle(message)
