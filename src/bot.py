import telebot
from telebot import apihelper
from telebot.custom_filters import ChatFilter

from res.credentials import BOT_TOKEN, PODPOLYE_ID
from src.filters.filters import OneArgumentFilter, TwoArgumentsFilter, RolePingFilter
from src.handlers.RoleHandlers import createRoleHandler, deleteRoleHandler, selfRollerHandler, selfUnrollerHandler, userRollerHandler, userUnrollerHandler, pingCommandRoleHandler, \
    pingAtRoleHandler
from src.handlers.StatOutputHandlers import printStatHandler
from src.logs import logsetup
from src.middleware.StatCollector import statCollector
from src.middleware.TitleHandler import userTitleHandler
from src.middleware.TriggeredMessageHandler import triggeredMessageHandler

log = logsetup.new_logger('Bot')

apihelper.ENABLE_MIDDLEWARE = True

bot = telebot.TeleBot(BOT_TOKEN, num_threads=5)

bot.register_message_handler(printStatHandler, commands=["stat"], chat_id=[PODPOLYE_ID], pass_bot=True)

bot.register_message_handler(createRoleHandler, commands=["createrole"], chat_id=[PODPOLYE_ID], pass_bot=True)
bot.register_message_handler(deleteRoleHandler, commands=["deleterole"], chat_id=[PODPOLYE_ID], pass_bot=True)
bot.register_message_handler(userRollerHandler, commands=["role"], twoarguments=True, chat_id=[PODPOLYE_ID], pass_bot=True)
bot.register_message_handler(userUnrollerHandler, commands=["unrole"], twoarguments=True, chat_id=[PODPOLYE_ID], pass_bot=True)
bot.register_message_handler(selfRollerHandler, commands=["role"], oneargument=True, chat_id=[PODPOLYE_ID], pass_bot=True)
bot.register_message_handler(selfUnrollerHandler, commands=["unrole"], oneargument=True, chat_id=[PODPOLYE_ID], pass_bot=True)
bot.register_message_handler(pingCommandRoleHandler, commands=["ping"], oneargument=True, chat_id=[PODPOLYE_ID], pass_bot=True)
bot.register_message_handler(pingAtRoleHandler, roleping=True, chat_id=[PODPOLYE_ID], pass_bot=True)
log.info('Message handlers registered')

bot.register_middleware_handler(userTitleHandler)
bot.register_middleware_handler(triggeredMessageHandler)
bot.register_middleware_handler(statCollector, update_types=['message'])
log.info('Middleware handlers registered')

bot.add_custom_filter(ChatFilter())
bot.add_custom_filter(OneArgumentFilter())
bot.add_custom_filter(TwoArgumentsFilter())
bot.add_custom_filter(RolePingFilter())
log.info('Custom filters added')
