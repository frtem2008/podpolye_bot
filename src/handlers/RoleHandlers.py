import telebot

from src.database import database
from src.handlers.TitleHandler import user_fmt
from src.handlers.handlers import PodpolyeHandler
from src.logsetup import Loggable


# TODO: Права доступа
# TODO: Заменить все проверки на регулярки
# TODO: Ответы бота

class Roller(Loggable):
    def __init__(self):
        Loggable.__init__(self, 'roller')

    def exists(self, username, role):
        if username and not database.get_user(username):
            self.log.info(f"User {username} not found")
            return False
        if role and not database.get_role(role):
            self.log.info(f"Role {role} does not exist")
            return False
        return True

    def create(self, role: str):
        database.create_role(role)
        self.log.info(f"Added new role {role}")

    def delete(self, role: str):
        if not self.exists(None, role):
            return
        database.delete_role(role)
        self.log.info(f"Deleted role {role}")

    def role(self, username: str, role: str):
        if not self.exists(username, role):
            return

        user = database.get_user(username)
        if role in database.get_user_roles(user.user_id):
            self.log.info(f"User {user_fmt(user)} already has role {role}")
            return

        database.give_role(user.user_id, role)
        self.log.debug(f"Gave role {role} to user {user_fmt(user)}")

    def unrole(self, username: str, role: str):
        if not self.exists(username, role):
            return
        user = database.get_user(username)
        if not role in database.get_user_roles(user.user_id):
            self.log.info(f"User {user_fmt(user)} does not have role {role}")
            return

        database.remove_role(user.user_id, role)
        self.log.debug(f"Removed role {role} from user {user_fmt(user)}")


class RoleCreator(Roller, PodpolyeHandler):
    def can_handle(self, message: telebot.types.Message) -> bool:
        return super().can_handle(message) and message.text.startswith("/createrole ")

    def handle(self, message: telebot.types.Message):
        role = message.text[len("/createrole "):].strip()
        self.create(role)


class RoleDeleter(Roller, PodpolyeHandler):
    def can_handle(self, message: telebot.types.Message) -> bool:
        return super().can_handle(message) and message.text.startswith("/deleterole ")

    def handle(self, message: telebot.types.Message):
        role = message.text[len("/deleterole "):].strip()
        self.delete(role)


class SelfRoller(Roller, PodpolyeHandler):
    def can_handle(self, message: telebot.types.Message) -> bool:
        return super().can_handle(message) \
            and message.text.startswith("/role ") \
            and len(message.text[len("/role "):].split()) == 1

    def handle(self, message: telebot.types.Message):
        role = message.text[len("/role "):].strip()
        self.role(message.from_user.username, role)


class SelfUnroller(Roller, PodpolyeHandler):
    def can_handle(self, message: telebot.types.Message) -> bool:
        return super().can_handle(message) \
            and message.text.startswith("/unrole ") \
            and len(message.text[len("/unrole "):].split()) == 1

    def handle(self, message: telebot.types.Message):
        role = message.text[len("/unrole "):].strip()
        self.unrole(message.from_user.username, role)


class UserRoller(Roller, PodpolyeHandler):
    def can_handle(self, message: telebot.types.Message) -> bool:
        return super().can_handle(message) \
            and message.text.startswith("/role @") \
            and len(message.text[len("/role "):].split()) > 1

    def handle(self, message: telebot.types.Message):
        username, role = message.text[len("/role @"):].strip().split()
        self.role(username, role)


class UserUnroller(Roller, PodpolyeHandler):
    def can_handle(self, message: telebot.types.Message) -> bool:
        return super().can_handle(message) \
            and message.text.startswith("/unrole @") \
            and len(message.text[len("/unrole "):].split()) > 1

    def handle(self, message: telebot.types.Message):
        username, role = message.text[len("/unrole "):].strip().split()
        self.unrole(username, role)


class PingRole(PodpolyeHandler):
    def can_handle(self, message: telebot.types.Message) -> bool:
        return super().can_handle(message) and message.text.startswith("/ping ")

    def handle(self, message: telebot.types.Message):
        ...
