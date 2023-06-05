import asyncio

from ..osa_utils.db_api.database import create_db, drop_connection

from loader import bot

import traceback
import sys


async def on_startup(dp):
    print("Bot is running...")
    await create_db()


async def on_shutdown(dp):
    await drop_connection()


if __name__ == '__main__':
    if sys.argv:
        print("if")
    else:
        print('else')
    from aiogram import executor
    from handlers.handlers import dp

    try:
        executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
    except Exception as e:
        var = traceback.format_exc()
        print(var)
