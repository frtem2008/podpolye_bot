import logging

import telebot

from src.database import database, models
from src.handlers.handlers import PodpolyeHandler


def user_fmt(user: telebot.types.User | models.Users) -> str:
    if hasattr(user, 'user_id'):
        return f'@{user.username}({user.user_id})'
    return f'@{user.username}({user.id})'


def get_title(bot: telebot.TeleBot, message: telebot.types.Message):
    for admin in bot.get_chat_administrators(message.chat.id):
        if admin.user.id == message.from_user.id:
            return admin.custom_title
    return None


class TitleAdder(PodpolyeHandler):
    def __init__(self):
        super().__init__()
        self.user_titles = {}
        for user in database.get_users():
            self.user_titles[user.user_id] = None

        self.log.level = logging.INFO

        self.log.info(f"Users: {self.user_titles}")

    def handle(self, message: telebot.types.Message):
        title = get_title(self.bot, message)
        self.log.debug(f'Title for {user_fmt(message.from_user)}: {title}')
        user_id = message.from_user.id

        if user_id not in self.user_titles:
            database.create_user(user_id, message.from_user.username, title)
            self.log.info(f'User {user_fmt(message.from_user)} added to database with title {title}')
        elif self.user_titles[user_id] != title:
            database.update_user(user_id, message.from_user.username, title)
            self.log.info(f'User {user_fmt(message.from_user)} title updated from {self.user_titles[user_id]} to {title}')

        self.user_titles[user_id] = title
