from aiogram import types
from utils.db_api import db_commands

from loader import dp, bot, storage
from data import config

from keyboards import faculty_cd, faculty_markup

from utils.db_api.models import faculties, faculties_ukr

from states import Registering
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

@dp.message_handler(commands=['test'])
async def test_handler(message: types.Message, state: FSMContext):
    votes = await db_commands.get_all_votes('fbme')
    for vote in votes:
        print(vote.results)


@dp.message_handler(commands=['start'])
async def bot_start(message: types.Message, state: FSMContext):
    if await db_commands.is_user_in_db(message.from_user.id) is True:
        print("In db")
    else:
        print("Not in db")
        await message.answer("Оберіть ваш факультет.", reply_markup=await faculty_markup())


async def save_faculty(faculty_index):
    print("User chosed faculty: " + f"{faculties[int(faculty_index)]}")
    faculty_ukr = faculties_ukr[int(faculty_index)]
    await db_commands.add_user()



@dp.callback_query_handler(faculty_cd.filter())
async def choosing_faculty(call: types.CallbackQuery, callback_data: dict):
    faculty_index = callback_data.get('faculty_index')

    await save_faculty(faculty_index)

    await call.answer()
