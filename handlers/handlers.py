import asyncio

from aiogram import types
import keyboards
from utils.db_api import db_commands
from utils.db_api.models import Teacher

from loader import dp, bot

from keyboards import faculty_cd, faculty_markup, faculty_confirmation_markup, teacher_cd, questions_cd, \
    open_q_confrimation_cd

from utils.db_api.models import faculties, faculties_ukr

from states import PollStates
from aiogram.dispatcher import FSMContext

from utils.db_api.models import User

import hashlib
from aiogram.types import InlineQuery, \
    InputTextMessageContent, InlineQueryResultArticle

import config


@dp.inline_handler()
async def inline_echo(inline_query: InlineQuery):
    text = inline_query.query or 'echo'

    faculty_ukr = await db_commands.get_user_faculty_by_tg_id(inline_query.from_user.id)
    faculty = faculties[faculties_ukr.index(faculty_ukr)]

    # if user in db, then faculty will be not None
    if faculty is not None:
        teachers_names: list[Teacher] = await db_commands.search_teachers_by_name(faculty, text)

        if teachers_names is not None:
            items = []
            for teacher_name in teachers_names:
                input_content = InputTextMessageContent(f"/start_poll {teacher_name}")
                result_id: str = hashlib.md5(teacher_name.encode()).hexdigest()
                item = InlineQueryResultArticle(
                    id=result_id,
                    title=teacher_name,
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


@dp.message_handler(state=PollStates.open_micro_question)
async def open_micro_handler(message: types.Message, state: FSMContext):
    state_data = await state.get_data()

    if None in state_data.values():
        await message.answer('Дайте відповідь на всі питання позаду')
    elif message.text == '/skip':
        await state.update_data({13: ' '})
        await message.answer('Ви певні, що хочете пропустити питання?',
                             reply_markup=await keyboards.open_q_confirmation_markup(13, False))
    else:
        await state.update_data({13: message.text})
        await message.answer(f'Ви певні, що хочете зберегти цю відповідь?\n\n{message.text}',
                             reply_markup=await keyboards.open_q_confirmation_markup(13, False))


@dp.message_handler(state=PollStates.anonymous_question)
async def anonymous_question_handler(message: types.Message, state: FSMContext):
    if message.text == '/skip':
        await state.update_data({14: ' '})
        await message.answer('Ви певні, що хочете пропустити питання?',
                             reply_markup=await keyboards.open_q_confirmation_markup(14, True))
    else:
        await state.update_data({14: message.text})
        await message.answer(f'Ви певні, що хочете зберегти цю відповідь?\n\n{message.text}',
                         reply_markup=await keyboards.open_q_confirmation_markup(14, True))


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

            faculty = faculties[faculties_ukr.index(user.faculty)]
            is_teacher_voted = await db_commands.is_teacher_voted(user.id, teacher.id, faculty)
            if teacher is not None and is_teacher_voted is False:
                await state.set_state(PollStates.minor_state)
                await state.update_data(teacher_id=teacher.id)
                print('Teacher in db')
                await message.answer(f"Ви обрали викладача: {full_name}.\n\nЩо викладав у вас даний викладач?",
                                     reply_markup=await keyboards.teacher_type_markup(faculty, teacher.id))
            elif teacher is not None:
                await message.answer('Ви вже заповнювали цього викладача.')
            else:
                print('Teacher not in db')
                await message.answer('Викладача з таким ПІБ не знайдено.')


        else:
            await message.answer('Неправильний формат!')
    else:
        await message.answer('Ви не зареєстровані.')


@dp.message_handler(commands=['test'])
async def test_handler(message: types.Message, state: FSMContext):
    await message.answer(message.from_user.id)
    await message.answer(message.chat.id)


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


@dp.callback_query_handler(faculty_cd.filter())
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


async def send_poll_questions(teacher_type: str, message: types.Message, user_tg_id: str, state: FSMContext):
    await state.set_state(PollStates.open_micro_question)

    # data structure in state storage:
    # keys are user_tg_id, teacher_type, teacher_id and questions_ids
    # keys: user_tg_id, teacher_type, teacher_id, 1, 2, 3, 4, 5...
    # values:
    # user_id - message.from_user.id
    # teacher_type - practice/lecture/lecture+practice
    # teacher_id - int
    # question_id (1-9) - 1-5
    # question_id (10-12) - Так/Ні -> 1/0
    # question_id (13-14) - free strings
    await state.update_data(user_tg_id=user_tg_id, teacher_type=teacher_type)
    print(message.from_user.id)
    print(await state.get_data('user_tg_id'))
    print(await state.get_data())
    questions = await db_commands.get_all_questions()

    for question in questions:
        print(question.id)
        # check teacher_type
        if question.type == 'both' or teacher_type == "lecture+practice" or question.type == teacher_type:
            # questions with answers 1-5
            if question.id in range(1, 10):
                await state.update_data({question.id: None})
                await message.answer(question.question_text, reply_markup=await keyboards.poll_1_5_markup(question.id))
            # questions with answers Yes/No
            elif question.id in range(10, 13):
                await state.update_data({question.id: None})
                await message.answer(question.question_text, reply_markup=await keyboards.poll_yes_no_markup(question.id))

    # first open question - open microphone question
    question_open_micro = await db_commands.get_question(13)
    await message.answer(question_open_micro.question_text + f'\n\n{config.skip_message}')


@dp.callback_query_handler(teacher_cd.filter(), state=PollStates.minor_state)
async def send_questions_cb(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.edit_reply_markup(None)

    teacher_type_cb = callback_data.get('teacher_type')

    # lecture type
    if teacher_type_cb == '0':
        await call.message.answer('Ви заповнюєте викладача як лектора')
        await send_poll_questions('lecture', call.message, call.from_user.id, state)
    # practice type
    elif teacher_type_cb == '1':
        await call.message.answer('Ви заповнюєте викладача як практика')
        await send_poll_questions('practice', call.message, call.from_user.id, state)
    # lecture+practice type
    elif teacher_type_cb == '2':
        await call.message.answer('Ви заповнюєте викладача як лектора і практика')
        await send_poll_questions('lecture+practice', call.message, call.from_user.id, state)


# questions with keyboards
@dp.callback_query_handler(questions_cd.filter(), state=PollStates.open_micro_question)
async def questions_btns_handler(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    print(callback_data)
    question_id = int(callback_data.get('question_id'))
    question_answer = int(callback_data.get('answer'))
    markup_type: str = callback_data.get('markup_type')

    await state.update_data({question_id: question_answer})

    if markup_type == '1_5':
        await call.message.edit_reply_markup(reply_markup=await keyboards.poll_1_5_markup(question_id, question_answer))
    elif markup_type == 'yes/no':
        await call.message.edit_reply_markup(reply_markup= await keyboards.poll_yes_no_markup(question_id, question_answer))
    await call.answer()


@dp.callback_query_handler(open_q_confrimation_cd.filter(),
                           state=[PollStates.open_micro_question, PollStates.anonymous_question])
async def open_q_conf_btns_handler(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    question_id: str = callback_data.get('question_id')
    question_confirmation = int(callback_data.get('confirmation'))
    is_last_question = int(callback_data.get('is_final_q'))

    await call.message.edit_reply_markup(None)

    if question_confirmation == 1:
        anonymous_question = await db_commands.get_question(14)
        await call.message.edit_text('Відповідь прийнято.')

        if is_last_question != 1:
            await state.set_state(PollStates.anonymous_question)
            await call.message.answer(anonymous_question.question_text + f'\n\n{config.skip_message}')
    else:
        await call.message.edit_text('Введіть нову відповідь.')

    if is_last_question == 1 and question_confirmation != 0:
        state_data = await state.get_data()
        print(state_data)
        user_tg_id = state_data['user_tg_id']
        teacher_id: int = state_data['teacher_id']
        teacher_type: str = state_data['teacher_type']
        user: User = await db_commands.get_user_by_tg_id(user_tg_id)
        faculty = faculties[faculties_ukr.index(user.faculty)]

        results_cb: dict = state_data

        open_answers = dict()
        open_answers[13] = results_cb[13]
        open_answers[14] = results_cb[14]

        del results_cb['user_tg_id'], results_cb['teacher_id'], results_cb['teacher_type'], results_cb[13], results_cb[14]

        results = {
            'lecture': {
                'questions_ids' : [],
                'marks': []
            },
            'practice': {
                'questions_ids': [],
                'marks': []
            }
        }

        questions = await db_commands.get_all_questions()
        for question in questions:
            if question.id in results_cb.keys():
                if question.type == 'lecture':
                    results['lecture']['questions_ids'].append(question.id)
                    results['lecture']['marks'].append(results_cb[question.id])
                elif question.type == 'practice':
                    results['practice']['questions_ids'].append(question.id)
                    results['practice']['marks'].append(results_cb[question.id])
                elif question.type == 'both':
                    results['lecture']['questions_ids'].append(question.id)
                    results['lecture']['marks'].append(results_cb[question.id])

                    results['practice']['questions_ids'].append(question.id)
                    results['practice']['marks'].append(results_cb[question.id])

        await db_commands.add_vote(faculty, user.id, teacher_id, results, open_answers)
        await call.message.answer('Опитування закінчено, дані збережені.\nДякуємо за участь!')
        await state.finish()
        await call.answer()
