from aiogram.filters.command import Command, CommandObject
from aiogram import Router,Bot
from aiogram.types import Message
from aiogram.filters.chat_member_updated import \
    ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER
from aiogram import types
from aiogram.enums import ParseMode

from filters.chat_type import ChatTypeFilter
from database.utils import get_db_connection


roles = Router()


@roles.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER), ChatTypeFilter(chat_type=["group", "supergroup"]))
async def new_group_member(member: types.ChatMemberUpdated):
    await member.answer(f"[Привет, кто бы ты ни был](tg://user?id={member.new_chat_member.user.id})", parse_mode=ParseMode.MARKDOWN_V2)
    new_user = member.new_chat_member.user

    conn, cur = get_db_connection()
    cur.execute("""INSERT INTO "user" (tg_id, username, name, group_id) VALUES (%s, %s, %s, %s)""", (new_user.id, new_user.username, new_user.first_name + " " + new_user.last_name, member.chat.id))
    cur.execute("""SELECT id FROM "role" WHERE group_id=%s and name='all'""", (member.chat.id,))

    cur.execute("""INSERT INTO "user_role" (role_id, user_id, group_id) VALUES (%s, %s, %s)""", (cur.fetchone()[0], new_user.id, member.chat.id))

    conn.commit()
    conn.close()


@roles.chat_member(ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER))
async def delete_group_member(update: types.ChatMemberUpdated):
    conn, cur = get_db_connection()
    # print(update)
    cur.execute("""DELETE FROM "user" WHERE group_id=%s and tg_id=%s""", (update.chat.id, update.new_chat_member.user.id))
    cur.execute("""DELETE FROM "user_role" WHERE user_id=%s and group_id=%s""", (update.new_chat_member.user.id, update.chat.id))

    conn.commit()
    conn.close()


@roles.message(Command("add_role_user", prefix="/!"))
async def role_user_add(message: Message, command: CommandObject):
    args = command.args.split(" ")
    if len(args) < 2:
        await message.reply("не правельный синтаксис")
        return
    role = args[0]
    usernames = args[1:]

    if role == "all":
        await message.answer("Это системная роль")
        return

    conn, cur = get_db_connection()
    cur.execute("""SELECT id FROM "role" WHERE group_id=%s AND name=%s""", (message.chat.id, role))

    role_id = cur.fetchone()
    if role_id is None:
        await message.reply("нет такоой роли")
        return
    # print(role_id)
    for username in usernames:
        if username[0] == "@":
            username = username[1:]

        cur.execute("""SELECT * FROM "user" WHERE group_id=%s AND username=%s""", (message.chat.id, username))
        user_id = cur.fetchone()
        print(message.chat.id, username)
        if user_id is None:
            await message.answer(f"Нет такого пользователя, {username}")
            continue

        cur.execute("""INSERT INTO "user_role" (role_id, user_id, group_id) VALUES (%s, %s, %s)""", (role_id, user_id[1], message.chat.id))
        await message.answer(f"Пользователь {username}, добавлен в роль {role}")

    conn.commit()
    conn.close()


@roles.message(Command("new_role", prefix="/!"))
async def new_role_add(message: Message, command: Command):
    if command.args is None or " " in command.args or "@" in command.args:
        await message.reply("неправильное использование аргументов")
        return

    role_name = command.args
    conn, cur = get_db_connection()
    cur.execute("""SELECT * FROM "role" WHERE group_id=%s and name=%s""", (message.chat.id, role_name))

    if not cur.fetchone() is None:
        await message.reply("Роль с таким именем есть")
        return

    cur.execute("""INSERT INTO "role" (group_id, name) VALUES (%s, %s)""", (message.chat.id, role_name))
    await message.answer(f"роль создана {role_name}")

    conn.commit()
    conn.close()



