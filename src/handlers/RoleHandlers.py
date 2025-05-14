import telebot

from src import messages
from src.middleware.UserHandlers import user_fmt, bot_logger
from src.models import database
from src.models.models import Users


# TODO: Права доступа
# TODO: Заменить все проверки на регулярки
# TODO: Сообщения об ошибках в пользовательском вводе

def link_to(user: Users) -> str:
    return f'[@{user.username}](tg://user?id={user.user_id})'


def send_message(bot: telebot.TeleBot, chat_id: int, name: str, **kwargs) -> None:
    bot.send_message(chat_id, messages.format_normal(name, **kwargs), parse_mode='Markdown')


def exists(
        bot: telebot.TeleBot, message: telebot.types.Message, username: str | None, role_name: str | None,
        send_username_message=True, send_role_message=True
) -> bool:
    if username and not database.get_user(username):
        bot_logger.info(f"User {username} not found")
        if send_username_message:
            send_message(bot, message.chat.id, 'user not found', username=username)
        return False
    if role_name and not database.get_role(role_name):
        bot_logger.info(f"Role {role_name} does not exist")
        if send_role_message:
            send_message(bot, message.chat.id, 'role does not exist', role_name=role_name)
        return False
    return True


def role(bot: telebot.TeleBot, message: telebot.types.Message, username: str, role_name: str) -> None:
    username = username.replace("@", "")
    if not exists(bot, message, username, role_name):
        return

    user = database.get_user(username)
    if role_name in database.get_user_role_names(user.user_id):
        bot_logger.info(f"User {user_fmt(user)} already has role {role_name}")
        send_message(bot, message.chat.id, 'user already has role', user=link_to(user), role_name=role_name)
        return

    database.give_role(user.user_id, role_name)
    bot_logger.info(f"Gave role {role_name} to user {user_fmt(user)}")
    send_message(bot, message.chat.id, 'role', user=link_to(user), role_name=role_name)


def unrole(bot: telebot.TeleBot, message: telebot.types.Message, username: str, role_name: str) -> None:
    username = username.replace("@", "")
    if not exists(bot, message, username, role_name):
        return
    user = database.get_user(username)
    if not role_name in database.get_user_role_names(user.user_id):
        bot_logger.info(f"User {user_fmt(user)} does not have role {role_name}")
        send_message(bot, message.chat.id, 'user does not have role', user=link_to(user), role_name=role_name)
        return

    database.remove_role(user.user_id, role_name)
    bot_logger.info(f"Removed role {role_name} from user {user_fmt(user)}")
    send_message(bot, message.chat.id, 'unrole', user=link_to(user), role_name=role_name)


def createRoleHandler(message: telebot.types.Message, bot: telebot.TeleBot) -> None:
    role_name = telebot.util.extract_arguments(message.text).strip()
    if exists(bot, message, None, role_name, send_role_message=False):
        send_message(bot, message.chat.id, 'role already exists', role_name=role_name)
        return

    database.create_role(role_name)
    send_message(bot, message.chat.id, 'role created', role_name=role_name)
    bot_logger.info(f"Created role {role_name}")


def deleteRoleHandler(message: telebot.types.Message, bot: telebot.TeleBot) -> None:
    role_name = telebot.util.extract_arguments(message.text).strip()
    if not exists(bot, message, None, role_name):
        return
    database.delete_role(role_name)
    send_message(bot, message.chat.id, 'role deleted', role_name=role_name)
    bot_logger.info(f"Deleted role {role_name}")


def selfRollerHandler(message: telebot.types.Message, bot: telebot.TeleBot) -> None:
    role_name = telebot.util.extract_arguments(message.text).strip()
    role(bot, message, message.from_user.username, role_name)


def selfUnrollerHandler(message: telebot.types.Message, bot: telebot.TeleBot) -> None:
    role_name = telebot.util.extract_arguments(message.text).strip()
    unrole(bot, message, message.from_user.username, role_name)


def userRollerHandler(message: telebot.types.Message, bot: telebot.TeleBot) -> None:
    username, role_name = telebot.util.extract_arguments(message.text).strip().split()
    role(bot, message, username, role_name)


def userUnrollerHandler(message: telebot.types.Message, bot: telebot.TeleBot) -> None:
    username, role_name = telebot.util.extract_arguments(message.text).strip().split()
    unrole(bot, message, username, role_name)


def pingRoleHandler(message: telebot.types.Message, bot: telebot.TeleBot) -> None:
    role_name = telebot.util.extract_arguments(message.text).strip()
    if not exists(bot, message, None, role_name):
        return

    to_ping = database.get_role_users(role_name)
    users = ''
    for user in to_ping:
        users += link_to(user) + ' '

    if users:
        bot_logger.info(f"Ping message for {role_name}: {users}")
        send_message(bot, message.chat.id, 'ping', role_name=role_name, users=users.strip())
    else:
        bot_logger.info(f"Nobody to ping for {role_name}")
        send_message(bot, message.chat.id, 'nobody to ping', role_name=role_name)
