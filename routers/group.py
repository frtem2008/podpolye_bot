from aiogram.filters import StateFilter, BaseFilter
from aiogram import Router, F, Bot
from aiogram.types import Message, ChatMemberUpdated, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters.chat_member_updated import \
    ChatMemberUpdatedFilter, IS_NOT_MEMBER, ADMINISTRATOR, IS_MEMBER
from aiogram import types
from aiogram.enums import ParseMode

from utils import *
from filters.chat_type import ChatTypeFilter
from database.utils import get_db_connection, add_members

group = Router()


@group.my_chat_member(ChatTypeFilter(chat_type=["group", "supergroup"]), ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def new_group(update: types.ChatMemberUpdated, bot: Bot):
    await update.answer("Я в группе")
    conn, cur = get_db_connection()
    cur.execute("""INSERT INTO "group" (tg_id, name) VALUES (%s, %s)""", (update.chat.id, update.chat.title))

    cur.execute("""INSERT INTO "role" (group_id, name) VALUES (%s, %s) RETURNING id""", (update.chat.id, "all"))
    all_role_id = cur.fetchone()[0]

    users = await get_chat_members(update.chat.id, bot)
    add_members(update.chat.id, users, conn, cur)

    for user in users:
        cur.execute("""INSERT INTO "user_role" (role_id, user_id, group_id) VALUES (%s, %s, %s)""", (all_role_id, user.id, update.chat.id))

    conn.commit()
    conn.close()


@group.my_chat_member(ChatTypeFilter(chat_type=["supergroup", "group"]), ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER))
async def delete_group(update: types.ChatMemberUpdated, bot: Bot):
    conn, cur = get_db_connection()

    cur.execute("""DELETE FROM "user_role" where group_id=%s""", (update.chat.id,))

    cur.execute("""DELETE FROM "role" WHERE group_id=%s""", (update.chat.id,))
    cur.execute("""DELETE FROM "user" WHERE group_id=%s""", (update.chat.id,))
    cur.execute("""DELETE FROM "group" WHERE tg_id=%s""", (update.chat.id,))

    await bot.send_message(update.from_user.id, "за что?")

    conn.commit()
    conn.close()
