import asyncio
from utils.db_api.database import create_db, drop_connection
from utils.db_api import db_commands

from aiogram.types import BotCommand
from loader import bot

from utils.db_api.database import create_db
import traceback


async def on_startup(dp):
    print("Bot is running...")
    await create_db()


async def on_shutdown(dp):
    await drop_connection()


if __name__ == '__main__':
    from aiogram import executor
    from handlers.handlers import dp

    try:
        executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
    except Exception as e:
        var = traceback.format_exc()
        print(var)
