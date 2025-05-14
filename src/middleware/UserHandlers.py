import logging

import telebot

from src import logsetup
from src.models import models, database

bot_logger = logsetup.new_logger('bot', logging.INFO)


def user_fmt(to_format: telebot.types.User | models.Users) -> str:
    if hasattr(to_format, 'user_id'):
        return f'@{to_format.username}({to_format.user_id})'
    return f'@{to_format.username}({to_format.id})'


def get_title(bot: telebot.TeleBot, message: telebot.types.Message) -> str | None:
    for admin in bot.get_chat_administrators(message.chat.id):
        if admin.user.id == message.from_user.id:
            return admin.custom_title
    return None


user_titles = {}


def import_users() -> None:
    for user in database.get_users():
        user_titles[user.user_id] = None


def userMessageHandler(bot: telebot.TeleBot, update: telebot.types.Update) -> None:
    message = update.message
    if not message:
        return

    title = get_title(bot, message)
    bot_logger.debug(f'Title for {user_fmt(message.from_user)}: {title}')
    user_id = message.from_user.id

    if user_id not in user_titles:
        database.create_user(user_id, message.from_user.username, title)
        bot_logger.info(f'User {user_fmt(message.from_user)} added to database with title {title}')
    elif user_titles[user_id] != title:
        database.update_user(user_id, message.from_user.username, title)
        bot_logger.info(f'User {user_fmt(message.from_user)} title updated from {user_titles[user_id]} to {title}')

    user_titles[user_id] = title
