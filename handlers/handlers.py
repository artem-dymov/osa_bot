from aiogram import types
from utils.db_api import db_commands

from loader import dp, bot, storage
from data import config

from keyboards import faculty_cd, faculty_markup, faculty_confirmation_markup

from utils.db_api.models import faculties, faculties_ukr

from states import Registering
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext


@dp.message_handler(state=Registering.group)
async def group_enter(message: types.Message, state: FSMContext):
    group_name = message.text

    faculty_ukr = await db_commands.get_user_faculty_by_tg_id(message.from_user.id)
    is_group_in_db = await db_commands.is_group_in_db(faculty_ukr, group_name)

    if is_group_in_db is True:
        await message.answer("Group saved")
        await state.finish()
    else:
        await message.answer("No such group on this faculty. Try again.")


@dp.message_handler(commands=['test'])
async def test_handler(message: types.Message, state: FSMContext):
    txt = message.text.split(' ')
    txt = txt[1]

    print(await db_commands.is_group_in_db('fbme', txt))

    print(txt)


@dp.message_handler(commands=['start'])
async def bot_start(message: types.Message, state: FSMContext):
    if await db_commands.is_user_in_db(message.from_user.id) is True:
        print("In db")
    else:
        print("Not in db")
        await message.answer("Оберіть ваш факультет.", reply_markup=await faculty_markup())


async def save_faculty(faculty_index, tg_id, username):
    print("User chosed faculty: " + f"{faculties[faculty_index]}")
    faculty_ukr = faculties_ukr[faculty_index]
    await db_commands.add_user(faculty_ukr=faculty_ukr, tg_id=tg_id, username=username)


@dp.callback_query_handler(faculty_cd.filter(), state='*')
async def choosing_faculty(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    faculty_index = int(callback_data.get('faculty_index'))
    confirmation = callback_data.get('confirmation')
    bool_confirmation = None
    if confirmation == '-1':
        pass
    elif confirmation == '0':
        bool_confirmation = False
    elif confirmation == '1':
        bool_confirmation = True

    if bool_confirmation is None:
        try:
            if await db_commands.is_user_in_db(call.from_user.id) is True:
                print("User in db.")
                await call.message.edit_reply_markup(None)
                await call.message.answer('Ви вже обрали факультет')
            else:
                # await save_faculty(faculty_index, call.from_user.id, call.from_user.username)
                await call.message.edit_text(f"Ви певні, що хочете обрати факультет {faculties_ukr[faculty_index]}?")
                await call.message.edit_reply_markup(await faculty_confirmation_markup(faculty_index))

        except Exception as e:
            await call.message.answer('Помилка! Почніть з команди /start\nConfirimation None.')
            print(e)

    elif bool_confirmation is True:
        try:
            if not (await db_commands.is_user_in_db(call.from_user.id) is True):
                await save_faculty(faculty_index, call.from_user.id, call.from_user.username)
                await call.message.edit_reply_markup(None)
                await call.message.answer('Введіть назву групи')
                await state.set_state(Registering.group)
            else:
                await call.message.edit_reply_markup(None)
                await call.message.answer('Ви вже обрали факультет')
        except Exception as e:
            print(e)

    elif bool_confirmation is False:
        try:
            await call.message.edit_text("Оберіть ваш факультет.")
            await call.message.edit_reply_markup(await faculty_markup())
        except Exception as e:
            print(e)

    await call.answer()
