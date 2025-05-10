import asyncio
from aiogram import Dispatcher, Bot
from setting import *
from routers.ping import ping
from routers.group import group
from routers.roles import roles


async def main():
    # Объект бота
    bot = Bot(token=BOT_TOKEN)
    # Диспетчер
    dp = Dispatcher()
    dp.include_routers(ping)
    dp.include_routers(group)
    dp.include_routers(roles)
    await dp.start_polling(bot, imge={})

if __name__ == "__main__":
    print("START")
    asyncio.run(main())