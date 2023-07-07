import asyncio

from osa_utils.db_api.database import create_db, drop_connection

from loader import bot

import traceback
import sys

import logging
logging.basicConfig(level=logging.INFO, filename='bot_log.log', filemode='w')


async def on_startup(dp):
    print("Bot is running...")
    logging.info('Bot is running...')

    logging.info('Connecting to db...')
    await create_db()
    logging.getLogger('gino.engine._SAEngine').setLevel(logging.WARNING)
    logging.info('Success! Connected to db.')


async def on_shutdown(dp):
    await drop_connection()


if __name__ == '__main__':
    from aiogram import executor
    from handlers.handlers import dp

    try:
        executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
    except Exception as e:
        var = traceback.format_exc()
        logging.exception(var)
