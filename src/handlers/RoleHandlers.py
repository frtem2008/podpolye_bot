import telebot

from src.database import database
from src.handlers.TitleHandler import user_fmt
from src.handlers.handlers import PodpolyeHandler, Handler


# TODO: Права доступа
# TODO: Заменить все проверки на регулярки
# TODO: Ответы бота

def exists(handler: Handler, username: str, role_name: str):
    if username and not database.get_user(username):
        handler.log.info(f"User {username} not found")
        return False
    if role_name and not database.get_role(role_name):
        handler.log.info(f"Role {role_name} does not exist")
        return False
    return True


def role(handler, username: str, role_name: str):
    if not exists(handler, username, role_name):
        return

    user = database.get_user(username)
    if role_name in database.get_user_roles(user.user_id):
        handler.log.info(f"User {user_fmt(user)} already has role {role_name}")
        return

    database.give_role(user.user_id, role_name)
    handler.log.debug(f"Gave role {role_name} to user {user_fmt(user)}")


def unrole(handler, username: str, role_name: str):
    if not exists(handler, username, role_name):
        return
    user = database.get_user(username)
    if not role_name in database.get_user_roles(user.user_id):
        handler.log.info(f"User {user_fmt(user)} does not have role {role_name}")
        return

    database.remove_role(user.user_id, role_name)
    handler.log.debug(f"Removed role {role_name} from user {user_fmt(user)}")


class RoleCreator(PodpolyeHandler):
    def can_handle(self, message: telebot.types.Message) -> bool:
        return super().can_handle(message) and message.text.startswith("/createrole ")

    def handle(self, message: telebot.types.Message):
        role_name = message.text[len("/createrole "):].strip()
        database.create_role(role_name)
        self.log.info(f"Added new role {role_name}")


class RoleDeleter(PodpolyeHandler):
    def can_handle(self, message: telebot.types.Message) -> bool:
        return super().can_handle(message) and message.text.startswith("/deleterole ")

    def handle(self, message: telebot.types.Message):
        role_name = message.text[len("/deleterole "):].strip()
        if not exists(self, None, role_name):
            return
        database.delete_role(role_name)
        self.log.info(f"Deleted role {role_name}")


class SelfRoller(PodpolyeHandler):
    def can_handle(self, message: telebot.types.Message) -> bool:
        return super().can_handle(message) \
            and message.text.startswith("/role ") \
            and len(message.text[len("/role "):].split()) == 1

    def handle(self, message: telebot.types.Message):
        role_name = message.text[len("/role "):].strip()
        role(self, message.from_user.username, role_name)

class SelfUnroller(PodpolyeHandler):
    def can_handle(self, message: telebot.types.Message) -> bool:
        return super().can_handle(message) \
            and message.text.startswith("/unrole ") \
            and len(message.text[len("/unrole "):].split()) == 1

    def handle(self, message: telebot.types.Message):
        role_name = message.text[len("/unrole "):].strip()
        unrole(self, message.from_user.username, role_name)


class UserRoller(PodpolyeHandler):
    def can_handle(self, message: telebot.types.Message) -> bool:
        return super().can_handle(message) \
            and message.text.startswith("/role @") \
            and len(message.text[len("/role "):].split()) > 1

    def handle(self, message: telebot.types.Message):
        username, role_name = message.text[len("/role @"):].strip().split()
        role(self, username, role_name)


class UserUnroller(PodpolyeHandler):
    def can_handle(self, message: telebot.types.Message) -> bool:
        return super().can_handle(message) \
            and message.text.startswith("/unrole @") \
            and len(message.text[len("/unrole "):].split()) > 1

    def handle(self, message: telebot.types.Message):
        username, role_name = message.text[len("/unrole @"):].strip().split()
        unrole(self, username, role_name)


class PingRole(PodpolyeHandler):
    def can_handle(self, message: telebot.types.Message) -> bool:
        return super().can_handle(message) and message.text.startswith("/ping ")

    def handle(self, message: telebot.types.Message):
        ...
