import asyncio
import logging
import sys
import config

from src.handlers.admin import admin
from src.handlers.users import users

from aiogram import Bot, Dispatcher


async def main() -> None:
    bot = Bot(config.TOKEN)
    disp = Dispatcher()

    disp.include_router(users)
    disp.include_router(admin)

    await disp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
