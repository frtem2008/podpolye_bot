import logging

import telebot

from res.credentials import PODPOLYE_ID
from src import log_setup
from src.database import database

class Handler:
    def __init__(self):
        self.log = log_setup.new_logger(f'{self.__class__.__name__} handler', logging.INFO)
        self.log.info("Initialized")
        self.bot = None

    def can_handle(self, message: telebot.types.Message) -> bool:
        return True

    def handle(self, message: telebot.types.Message):
        raise Exception("Not implemented")


class Ping(Handler):
    def handle(self, message: telebot.types.Message):
        self.log.info(f"Got message {message}")
        roles = database.get_roles()
        self.log.info(f"Roles: {roles}")
        self.log.info(f"Users: {database.get_users()}")


def user_fmt(message: telebot.types.Message) -> str:
    return f'@{message.from_user.username}({message.from_user.id})'

def get_title(bot: telebot.TeleBot, message: telebot.types.Message):
    for admin in bot.get_chat_administrators(message.chat.id):
        if admin.user.id == message.from_user.id:
            return admin.custom_title
    return None

class TitleAdder(Handler):
    def __init__(self):
        super().__init__()
        self.user_titles = {}
        for user in database.get_users():
            self.user_titles[user.user_id] = None

        self.log.info(f"Users: {self.user_titles}")

    def can_handle(self, message: telebot.types.Message) -> bool:
        return message.chat.id == PODPOLYE_ID

    def handle(self, message: telebot.types.Message):
        title = get_title(self.bot, message)
        self.log.info(f'Title for {user_fmt(message)}: {title}')
        user_id = message.from_user.id

        if user_id not in self.user_titles:
            database.add_user(user_id, message.from_user.username, title)
            self.log.info(f'User {user_fmt(message)} added to database with title {title}')

        if self.user_titles[user_id] != title:
            database.update_user(user_id, message.from_user.username, title)
            self.log.info(f'User {user_fmt(message)} title updated from {self.user_titles[user_id]} to {title}')

        self.user_titles[user_id] = title
