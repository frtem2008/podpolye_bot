import logging

import telebot
import handlers.handlers
from res.credentials import BOT_TOKEN, PODPOLYE_ID
from src import log_setup

bot = telebot.TeleBot(BOT_TOKEN)
bot_logger = log_setup.new_logger('main', logging.DEBUG)
bot_handlers = []

def add_handler(handler: handlers.handlers.Handler):
    bot_handlers.append(handler)
    handler.bot = bot


@bot.message_handler()
def handle_message(message: telebot.types.Message):
    for handler in bot_handlers:
        handler.handle(message)
