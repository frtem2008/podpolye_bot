import telebot
from telebot import apihelper
from telebot.custom_filters import ChatFilter

from res.credentials import BOT_TOKEN, PODPOLYE_ID
from src.filters.filters import OneArgumentFilter, TwoArgumentsFilter
from src.handlers.RoleHandlers import createRoleHandler, deleteRoleHandler, selfRollerHandler, selfUnrollerHandler, userRollerHandler, userUnrollerHandler, pingRoleHandler
from src.middleware.UserHandlers import userMessageHandler
from src.handlers.stat_hendlers import *

apihelper.ENABLE_MIDDLEWARE = True

bot = telebot.TeleBot(BOT_TOKEN, num_threads=5)


def register_handlers():
    bot.register_message_handler(createRoleHandler, commands=["createrole"], chat_id=[PODPOLYE_ID], pass_bot=True)
    bot.register_message_handler(deleteRoleHandler, commands=["deleterole"], chat_id=[PODPOLYE_ID], pass_bot=True)
    bot.register_message_handler(userRollerHandler, commands=["role"], twoarguments=True, chat_id=[PODPOLYE_ID], pass_bot=True)
    bot.register_message_handler(userUnrollerHandler, commands=["unrole"], twoarguments=True, chat_id=[PODPOLYE_ID], pass_bot=True)
    bot.register_message_handler(selfRollerHandler, commands=["role"], oneargument=True, chat_id=[PODPOLYE_ID], pass_bot=True)
    bot.register_message_handler(selfUnrollerHandler, commands=["unrole"], oneargument=True, chat_id=[PODPOLYE_ID], pass_bot=True)
    bot.register_message_handler(pingRoleHandler, commands=["ping"], oneargument=True, chat_id=[PODPOLYE_ID], pass_bot=True)
    bot.register_message_handler(statictic_hendlers, chat_id=[PODPOLYE_ID], pass_bot=True)


bot.register_middleware_handler(userMessageHandler, update_types=['message'])

bot.add_custom_filter(ChatFilter())
bot.add_custom_filter(OneArgumentFilter())
bot.add_custom_filter(TwoArgumentsFilter())

register_handlers()
