from aiogram import types
from memory_profiler import memory_usage
import keyboards
from utils.db_api import db_commands
from utils.db_api.models import Teacher

from loader import dp, bot

from keyboards import faculty_cd, faculty_markup, faculty_confirmation_markup

from utils.db_api.models import faculties, faculties_ukr

from states import Registering
from aiogram.dispatcher import FSMContext

from utils.db_api.models import User

import hashlib
from aiogram.types import InlineQuery, \
    InputTextMessageContent, InlineQueryResultArticle


@dp.inline_handler()
async def inline_echo(inline_query: InlineQuery):
    text = inline_query.query or 'echo'

    faculty_ukr = await db_commands.get_user_faculty_by_tg_id(inline_query.from_user.id)
    faculty = faculties[faculties_ukr.index(faculty_ukr)]

    # if user in db, then faculty will be not None
    if faculty is not None:
        teachers: list[Teacher] = await db_commands.search_teachers_by_name(faculty, text)

        if teachers is not None:
            items = []
            for teacher in teachers:
                input_content = InputTextMessageContent(f"/start_poll {teacher.full_name}")
                result_id: str = hashlib.md5(teacher.full_name.encode()).hexdigest()
                item = InlineQueryResultArticle(
                    id=result_id,
                    title=teacher.full_name,
                    input_message_content=input_content,
                )
                items.append(item)

            # Now this if is not using.
            if not items:
                input_content = InputTextMessageContent("Порожньо")
                result_id: str = hashlib.md5(text.encode()).hexdigest()
                item = InlineQueryResultArticle(
                    id=result_id,
                    title='Немає результатів',
                    input_message_content=input_content,
                )
                items.append(item)
            # don't forget to set cache_time=1 for testing (default is 300s or 5m)
            await bot.answer_inline_query(inline_query.id, results=items[:10], cache_time=1)


# @dp.message_handler(state=Registering.group)
# async def group_enter(message: types.Message, state: FSMContext):
#     group_name = message.text
#
#     faculty_ukr = await db_commands.get_user_faculty_by_tg_id(message.from_user.id)
#
#     is_group_in_db = await db_commands.is_group_in_db(faculty_ukr, group_name)
#
#     user: User = await db_commands.get_user_by_tg_id(message.from_user.id)
#
#     if is_group_in_db is True:
#         await message.answer(f"confirm group {message.text}", reply_markup=await keyboards.group_confirmation_markup(
#             faculties_ukr.index(faculty_ukr), group_name
#         ))
#         # await message.edit_reply_markup(None)
#         group_id = await db_commands.get_group_id_by_name(faculties[faculties_ukr.index(faculty_ukr)], group_name.lower())
#         await db_commands.update_user(message.from_user.id, group_id=group_id)
#         await state.finish()
#     else:
#         await message.answer("No such group on this faculty. Try again.")


@dp.message_handler(commands=['start_poll'])
async def start_poll(message: types.Message, state: FSMContext):
    user = await db_commands.get_user_by_tg_id(message.from_user.id)
    if user is not None:
        if len(message.text.split(' ')) > 1:
            faculty = faculties[faculties_ukr.index(user.faculty)]

            full_name = ''
            for i in message.text.split(' '):
                if '/' not in i:
                    full_name = full_name + ' ' + i

            teacher = await db_commands.get_teacher_by_name(faculty, full_name)
            if teacher is not None:
                print('Teacher in db')
                await message.answer(f"Ви обрали викладача: {full_name}.\n\nЩо викладав у вас даний викладач?",
                                     reply_markup=await keyboards.teacher_type_markup(faculty, teacher.id))


            else:
                print('Teacher not in db')
                await message.answer('Викладача з таким ПІБ не знайдено.')

            print(full_name)

        else:
            await message.answer('Неправильний формат!')
    else:
        await message.answer('Ви не зареєстровані.')


@dp.message_handler(commands=['test'])
async def test_handler(message: types.Message, state: FSMContext):
    # txt = message.text.split(' ')
    # txt = txt[1]
    #
    # print(await db_commands.is_group_in_db('fbme', txt))
    #
    # print(txt)

    # await message.answer(memory_usage())
    await message.answer("Hello world")


@dp.message_handler(commands=['start'])
async def bot_start(message: types.Message, state: FSMContext):
    if await db_commands.is_user_in_db(message.from_user.id) is True:
        print("In db")
        await message.answer('Нажміть на кнопку нижче, а потім почніть вводити ПІБ викладача і виберіть потрібного з ' +
                             'наданого списку',
                             reply_markup=await keyboards.start_inline_search_markup())
    else:
        print("Not in db")
        await message.answer("Оберіть ваш факультет.", reply_markup=await faculty_markup())


async def save_faculty(faculty_index, tg_id, username):
    print("User chosed faculty: " + f"{faculties[faculty_index]}")
    faculty_ukr = faculties_ukr[faculty_index]
    await db_commands.add_user(faculty_ukr=faculty_ukr, tg_id=tg_id, username=username)


async def save_group(faculty_index, tg_id, group_name):
    await db_commands.update_user(tg_id, group_name=group_name)


@dp.callback_query_handler(faculty_cd.filter(), state='*')
async def choosing_faculty(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    faculty_index = int(callback_data.get('faculty_index'))

    confirmation_faculty = callback_data.get('confirmation_faculty')
    bool_confirmation_faculty = None
    if confirmation_faculty == '-1':
        pass
    elif confirmation_faculty == '0':
        bool_confirmation_faculty = False
    elif confirmation_faculty == '1':
        bool_confirmation_faculty = True


    if bool_confirmation_faculty is None:
        if await db_commands.is_user_in_db(call.from_user.id) is True:
            print("User in db.")
            try:
                await call.message.edit_reply_markup(None)
            except Exception as e:
                await call.message.answer('Помилка! Почніть з команди /start\nConfirimation None.')
                print(e)
            await call.message.answer('Ви вже обрали факультет')
        else:
            try:
                await call.message.edit_text(f"Ви певні, що хочете обрати факультет {faculties_ukr[faculty_index]}?")
                await call.message.edit_reply_markup(await faculty_confirmation_markup(faculty_index))
            except Exception as e:
                await call.message.answer('Помилка! Почніть з команди /start\nConfirimation None.')
                print(e)

    elif bool_confirmation_faculty is True:
        try:
            if not (await db_commands.is_user_in_db(call.from_user.id) is True):
                await save_faculty(faculty_index, call.from_user.id, call.from_user.username)
                await call.message.edit_reply_markup(None)
                await call.message.answer('Ваш факультет збережено!\n\nНатисніть /start, щоб почати опитування.')


            else:
                await call.message.edit_reply_markup(None)
                await call.message.answer('Ви вже обрали факультет')
        except Exception as e:
            print(e)

    elif bool_confirmation_faculty is False:
        try:
            await call.message.edit_text("Оберіть ваш факультет.")
            await call.message.edit_reply_markup(await faculty_markup())
        except Exception as e:
            print(e)

    await call.answer()
