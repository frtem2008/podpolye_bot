from aiogram import Router, F, Bot
from aiogram.types import Message

from utils import role_in_message, get_users
from filters.chat_type import ChatTypeFilter
from database.utils import get_db_connection

ping = Router()


@ping.message(F.text, ChatTypeFilter(chat_type=["group", "supergroup"]))
async def test(message: Message, bot: Bot):
    conn, cur = get_db_connection()

    cur.execute("""SELECT name, id FROM role WHERE group_id=%s""", (message.chat.id,))

    # print(cur.fetchall())
    data = cur.fetchall()
    roles = [i[0] for i in data]
    id_roles = [i[1] for i in data]
    role_list = [f"@{role}" for role in roles]
    list_of_words = [word for word in message.text.split(" ") if "@" in word]

    main_role = role_in_message(role_list, list_of_words)
    if main_role:
        cur.execute("""SELECT user_id FROM user_role WHERE role_id=%s""", (id_roles[role_list.index(main_role)],))
        users_id = [id[0] for id in cur.fetchall()]

        users = await get_users(message.chat.id, users_id, bot)
        users_usernames = [user.username for user in users]
        answer = " @".join(users_usernames)

        await message.answer("@"+answer)

    conn.close()
