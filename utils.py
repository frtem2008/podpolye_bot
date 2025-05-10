from aiogram import Bot
from telethon import TelegramClient
from setting import *

async def get_chat_members(chat_id, bot: Bot):
    client = TelegramClient("Имя | Бот", api_id=API_ID, api_hash=API_HASH)
    await client.start(bot_token=BOT_TOKEN)
    chat_members = []

    async for member in client.iter_participants(chat_id):
        user = await bot.get_chat_member(chat_id, member.id)
        user = user.user

        if not user.is_bot:
            chat_members.append(user)

    await client.disconnect()

    return chat_members


def role_in_message(list_role, list_word):
    for role in list_role:
        if role in list_word:
            return role
    return None


async def get_users(chat_id, users_id: list, bot: Bot):
    users = []

    for user_id in users_id:
        data = await bot.get_chat_member(chat_id, user_id)
        users.append(data.user)

    return users