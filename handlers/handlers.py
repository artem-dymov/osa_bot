from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from utils.db_api import db_commands

from loader import dp, bot
from data import config

from keyboards import faculty_cd, faculty_markup

from utils.db_api.models import faculties, faculties_ukr

async def save_faculty(faculty_index):
    print("User chosed faculty: " + f"{faculties[int(faculty_index)]}")


@dp.message_handler(commands=['start'])
async def bot_start(message: types.Message):
    if await db_commands.is_user_in_db(message.from_user.id) is True:
        print("In db")
    else:
        print("Not in db")
        await message.answer("Виберіть ваш факультет.", reply_markup=await faculty_markup())



@dp.callback_query_handler(faculty_cd.filter())
async def choosing_faculty(call: types.CallbackQuery, callback_data: dict):
    faculty_index = callback_data.get('faculty_index')

    await save_faculty(faculty_index)

    await call.answer()
