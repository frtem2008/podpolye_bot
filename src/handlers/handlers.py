import logging

import telebot

from src import log_setup
from src.database import database


class Handler:
    def __init__(self):
        self.log = log_setup.new_logger(f'{self.__class__.__name__} handler', logging.INFO)
        self.log.info("Initialized")
        self.bot = None

    def handle(self, message: telebot.types.Message):
        raise Exception("Not implemented")


class Ping(Handler):
    def handle(self, message: telebot.types.Message):
        self.log.info(f"Got message {message}")
        roles = database.get_roles()
        self.log.info(f"Roles: {roles}")

class UserAdder(Handler):
    def handle(self, message: telebot.types.Message):
        admins = self.bot.get_chat_administrators(message.chat.id)
        title = ''
        for admin in admins:
            if admin.user.id == message.from_user.id:
                 title = admin.custom_title

        database.add_user(message.from_user.id, message.from_user.username, title)
        self.log.info(f"User {message.from_user.id} added to database with title {title}")