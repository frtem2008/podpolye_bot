import logging

import telebot

from res.credentials import PODPOLYE_ID
from src.database import database
from src.logsetup import Loggable


class Handler(Loggable):
    def __init__(self):
        super().__init__(suffix='handler')
        self.bot = None

    def can_handle(self, message: telebot.types.Message) -> bool:
        return True

    def handle(self, message: telebot.types.Message):
        raise Exception("Not implemented")


class Ping(Handler):
    def __init__(self):
        super().__init__()
        self.log.level = logging.INFO

    def handle(self, message: telebot.types.Message):
        self.log.debug(f"Got message {message}")
        roles = database.get_roles()
        self.log.debug(f"Roles: {roles}")
        self.log.debug(f"Users: {database.get_users()}")


class PodpolyeHandler(Handler):
    def can_handle(self, message: telebot.types.Message) -> bool:
        return message.chat.id == PODPOLYE_ID
