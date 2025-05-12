import telebot

from src.middleware.UserHandlers import user_fmt, bot_logger
from src.models import database


# TODO: Права доступа
# TODO: Заменить все проверки на регулярки
# TODO: Ответы бота

def exists(username: str, role_name: str):
    if username and not database.get_user(username):
        bot_logger.info(f"User {username} not found")
        return False
    if role_name and not database.get_role(role_name):
        bot_logger.info(f"Role {role_name} does not exist")
        return False
    return True


def role(username: str, role_name: str):
    username = username.replace("@", "")
    if not exists(username, role_name):
        return

    user = database.get_user(username)
    if role_name in database.get_user_roles(user.user_id):
        bot_logger.info(f"User {user_fmt(user)} already has role {role_name}")
        return

    database.give_role(user.user_id, role_name)
    bot_logger.debug(f"Gave role {role_name} to user {user_fmt(user)}")


def unrole(username: str, role_name: str):
    username = username.replace("@", "")
    if not exists(username, role_name):
        return
    user = database.get_user(username)
    if not role_name in database.get_user_roles(user.user_id):
        bot_logger.info(f"User {user_fmt(user)} does not have role {role_name}")
        return

    database.remove_role(user.user_id, role_name)
    bot_logger.debug(f"Removed role {role_name} from user {user_fmt(user)}")


def createRoleHandler(message: telebot.types.Message, bot: telebot.TeleBot):
    role_name = telebot.util.extract_arguments(message.text).strip()
    database.create_role(role_name)
    bot_logger.info(f"Created role {role_name}")


def deleteRoleHandler(message: telebot.types.Message, bot: telebot.TeleBot):
    role_name = telebot.util.extract_arguments(message.text).strip()
    if not exists(None, role_name):
        return
    database.delete_role(role_name)
    bot_logger.info(f"Deleted role {role_name}")


def selfRollerHandler(message: telebot.types.Message, bot: telebot.TeleBot):
    bot_logger.info(f"Self role: {message.text}")
    role_name = telebot.util.extract_arguments(message.text).strip()
    role(message.from_user.username, role_name)


def selfUnrollerHandler(message: telebot.types.Message, bot: telebot.TeleBot):
    role_name = telebot.util.extract_arguments(message.text).strip()
    unrole(message.from_user.username, role_name)


def userRollerHandler(message: telebot.types.Message, bot: telebot.TeleBot):
    username, role_name = telebot.util.extract_arguments(message.text).strip().split()
    role(username, role_name)


def userUnrollerHandler(message: telebot.types.Message, bot: telebot.TeleBot):
    username, role_name = telebot.util.extract_arguments(message.text).strip().split()
    unrole(username, role_name)

def pingRoleHandler(message: telebot.types.Message, bot: telebot.TeleBot):
    role_name = telebot.util.extract_arguments(message.text).strip()
    if not database.get_role(role_name):
        bot_logger.info(f'Role {role_name} does not exist')
        return

    to_ping = database.get_role_users(role_name)
    msg = ''
    for user in to_ping:
        msg += f'[@{user.username}](tg://user?id={user.user_id}) '

    if msg:
        bot_logger.info(f"Ping message for {role_name}: {msg}")
        bot.send_message(message.chat.id, msg.strip(), parse_mode='Markdown')
    else:
        bot_logger.info(f"Nobody to ping for {role_name}")
