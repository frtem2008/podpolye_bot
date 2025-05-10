from aiogram.filters.command import Command
from aiogram.filters import StateFilter, BaseFilter
from aiogram import Router, F, Bot
from aiogram.types import Message, ChatMemberUpdated, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters.chat_member_updated import \
    ChatMemberUpdatedFilter, IS_NOT_MEMBER, ADMINISTRATOR, IS_MEMBER
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