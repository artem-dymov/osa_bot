import asyncio

from aiogram import types
import keyboards
from osa_utils.db_api import db_commands
from osa_utils.db_api.models import Teacher

from loader import dp, bot

from keyboards import faculty_cd, faculty_markup, faculty_confirmation_markup, teacher_cd, questions_cd, \
    open_q_confirmation_cd, group_cd

from config import faculties, faculties_ukr

from states import PollStates, Registering
from aiogram.dispatcher import FSMContext

from osa_utils.db_api.models import User

import hashlib
from aiogram.types import InlineQuery, \
    InputTextMessageContent, InlineQueryResultArticle

import config

from typing import Union

from osa_utils.photo_api import photo_getter

from aiogram.utils.exceptions import Throttled
from main import logging


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
                teacher_name = teacher.full_name
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


async def is_throttled(message: types.Message):
    try:
        await dp.throttle('key', rate=config.ANTIFLOOD_RATE)
    except Throttled:
        # If request is throttled, the `Throttled` exception will be raised
        await message.reply('Занадто багато запитів!')
        logging.warning(f'Bot throttled. User <{message.chat.id}>')
        return True
    else:
        return False


@dp.message_handler(commands=['cancel'], state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    if await is_throttled(message) is True:
        return -1

    if await state.get_state() is None:
        await message.answer('Немає що відміняти. Ви не проходите опитування')
    else:
        await state.finish()
        await message.answer('Дію відмінено')


@dp.message_handler(commands=['start'])
async def bot_start(message: types.Message, state: FSMContext):
    if await is_throttled(message) is True:
        return -1

    if await db_commands.is_user_in_db(message.from_user.id) is True:
        await message.answer('Натисніть на кнопку нижче, а потім почніть вводити ПІБ викладача і оберіть потрібного з ' +
                             'наданого списку',
                             reply_markup=await keyboards.start_inline_search_markup())
    else:
        await message.answer("Оберіть ваш факультет.", reply_markup=await faculty_markup())


async def save_user(faculty_index, tg_id, username, group_id):
    faculty_ukr = faculties_ukr[faculty_index]

    await db_commands.add_user(faculty_ukr=faculty_ukr, tg_id=tg_id, username=username, group_id=group_id)


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
                await state.update_data({
                    'faculty_index': faculty_index,
                    'user_tg_id': call.from_user.id,
                    'username': call.from_user.username
                })

                await state.set_state(Registering.group)

                await call.message.edit_reply_markup(None)
                await call.message.answer('Ваш факультет збережено!\n\nТепер напишіть мені назву своєї групи.\n'
                                          'Назва повинна бути написана українською, приклади:\n'
                                          'бс-11, бс-12мп, бр-03')


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


@dp.message_handler(state=Registering.group)
async def group_reg_handler(message: types.Message, state: FSMContext):
    state_data: dict = await state.get_data()
    faculty_index: int = state_data['faculty_index']
    user_tg_id: int = state_data['user_tg_id']
    username: Union[None, str] = state_data['username']

    groups = await db_commands.get_all_groups(faculties[faculty_index])

    is_group_in_db = False
    for group in groups:
        if group.name.lower().strip() == message.text.lower().strip():
            await state.update_data({'group_id': group.id})
            await state.set_state(Registering.confirm_group)

            markup = await keyboards.group_confirmation_markup()
            is_group_in_db = True
            await message.answer(f'Зберегти групу {group.name}?', reply_markup=markup)

    if is_group_in_db is False:
        await message.answer('Не знайдено групи з такою назвою, спробуйте ще раз!')


@dp.callback_query_handler(group_cd.filter(), state=Registering.confirm_group)
async def cofirm_group_handler(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    confirm_group: Union[0, 1] = int(callback_data.get('confirmation_group'))
    state_data: dict = await state.get_data()
    faculty_index: int = state_data['faculty_index']
    user_tg_id: int = state_data['user_tg_id']
    username: Union[None, str] = state_data['username']
    group_id = state_data['group_id']

    if confirm_group == 1:
        faculty_ukr = faculties_ukr[faculty_index]
        user = await db_commands.add_user(faculty_ukr=faculty_ukr, tg_id=user_tg_id,
                                          username=username, group_id=group_id)

        await state.finish()
        await call.message.answer('Дані збережені!\n\nНатисніть /start щоб обрати викладача, '
                                  'або натисніть /list щоб переглянути список викладачів, які можуть бути '
                                  'Вам цікаві')
    else:
        await state.set_state(Registering.group)
        await call.message.answer('Відправте мені назву своєї групи')

    await call.message.edit_reply_markup(None)


@dp.message_handler(commands=['start_poll'])
async def start_poll(message: types.Message, state: FSMContext):
    if await is_throttled(message) is True:
        return -1

    user = await db_commands.get_user_by_tg_id(message.from_user.id)
    if user is not None:
        if len(message.text.split(' ')) > 1:
            faculty = faculties[faculties_ukr.index(user.faculty)]

            full_name = ''
            for i in message.text.split(' '):
                if '/' not in i:
                    full_name = full_name + ' ' + i

            teacher = await db_commands.get_teacher_by_name(faculty, full_name)

            is_teacher_voted = await db_commands.is_teacher_voted(user.id, teacher.id, faculty)
            if teacher is not None and is_teacher_voted is False:

                # student can vote for certain teacher only if he has it in his group
                user_group = await db_commands.get_group(user.group_id, faculty)
                is_teacher_in_group = False
                if len(user_group.teachers) > 0:
                    for group_teacher in user_group.teachers:
                        if teacher.id == group_teacher['id']:
                            is_teacher_in_group = True

                if is_teacher_in_group:

                    await state.set_state(PollStates.minor_state)
                    await state.update_data(teacher_id=teacher.id)

                    # contains object opened with open()
                    file = await photo_getter.get_teacher_photo(user.faculty, teacher.id)

                    await message.answer_photo(file)
                    file.close()

                    await message.answer(f"Ви обрали викладача: {full_name}.\n\nЩо викладав у Вас даний викладач?\n\n"
                                         f"{config.teacher_non_type_msg}\n\n"
                                         f"{config.cancel_vote_msg}",
                                         reply_markup=await keyboards.teacher_type_markup(faculty, teacher))
                else:
                    await message.answer('Вибачте, цього викладача немає у списку викладачів за Вашою групою.\n\n'
                                         'Натисніть /list щоб побачити список Ваших викладачів.')
            elif teacher is not None:
                await message.answer('Ви вже заповнювали цього викладача.')
            else:
                await message.answer('Викладача з таким ПІБ не знайдено.')

        else:
            await message.answer('Неправильний формат!')
    else:
        await message.answer('Ви не зареєстровані. Натисніть /start')


async def send_poll_questions(teacher_type: str, message: types.Message, user_tg_id: str, state: FSMContext):
    await state.set_state(PollStates.open_micro_question)

    # data structure in state storage:
    # keys are user_tg_id, teacher_type, teacher_id and questions_ids
    # keys: user_tg_id, teacher_type, teacher_id, 1, 2, 3, 4, 5...
    # values:
    # user_id - message.from_user.id
    # teacher_type - practice/lecture/both
    # teacher_id - int
    # question_id - int

    await state.update_data(user_tg_id=user_tg_id, teacher_type=teacher_type)

    questions = await db_commands.get_all_questions()

    for question in questions:
        # check teacher_type
        # both in question type means that this question must be used with lecture, practice and both teachers
        # (for all teachers as open questions)

        # both teacher means that these teachers teach lectures and practices
        if question.type == 'both' or teacher_type == 'both' or question.type == teacher_type:
            # questions with answers 1-5
            if question.answer_format == '1_5':
                await state.update_data({question.id: None})
                await message.answer(question.question_text, reply_markup=await keyboards.poll_1_5_markup(question.id))
            # questions with answers Yes/No
            elif question.answer_format == 'yes/no':
                await state.update_data({question.id: None})
                await message.answer(question.question_text, reply_markup=await keyboards.poll_yes_no_markup(question.id))

            await asyncio.sleep(1)
    # first open question - open microphone question
    question_open_micro = await db_commands.get_first_open_q()
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
        await send_poll_questions('both', call.message, call.from_user.id, state)


# questions with keyboards
@dp.callback_query_handler(questions_cd.filter(), state=PollStates.open_micro_question)
async def questions_btns_handler(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    question_id = int(callback_data.get('question_id'))
    question_answer = int(callback_data.get('answer'))
    markup_type: str = callback_data.get('markup_type')

    await state.update_data({question_id: question_answer})

    if markup_type == '1_5':
        await call.message.edit_reply_markup(reply_markup=await keyboards.poll_1_5_markup(question_id, question_answer))
    elif markup_type == 'yes/no':
        await call.message.edit_reply_markup(reply_markup=await keyboards.poll_yes_no_markup(question_id, question_answer))
    await call.answer()


@dp.message_handler(state=PollStates.open_micro_question)
async def open_micro_handler(message: types.Message, state: FSMContext):
    state_data = await state.get_data()

    if None in state_data.values():
        await message.answer('Дайте відповідь на усі попередні запитання')
    elif message.text == '/skip':
        microphone = await db_commands.get_first_open_q()
        await state.update_data({microphone.id: ''})
        await message.answer('Ви певні, що хочете пропустити питання?',
                             reply_markup=await keyboards.open_q_confirmation_markup(13, True))
    else:
        microphone = await db_commands.get_first_open_q()
        await state.update_data({microphone.id: message.text})
        await message.answer(f'Ви певні, що хочете зберегти цю відповідь?\n\n{message.text}',
                             reply_markup=await keyboards.open_q_confirmation_markup(13, True))


@dp.callback_query_handler(open_q_confirmation_cd.filter(),
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
            await state.set_state(PollStates.open_micro_question)
            await call.message.answer(anonymous_question.question_text + f'\n\n{config.skip_message}')
    else:
        await call.message.edit_text('Введіть нову відповідь.')

    if is_last_question == 1 and question_confirmation != 0:
        state_data = await state.get_data()
        user_tg_id = state_data['user_tg_id']
        teacher_id: int = state_data['teacher_id']
        teacher_type: str = state_data['teacher_type']
        user: User = await db_commands.get_user_by_tg_id(user_tg_id)
        faculty = faculties[faculties_ukr.index(user.faculty)]

        results_cb: dict = state_data

        del results_cb['user_tg_id'], results_cb['teacher_id'], results_cb['teacher_type']

        results = {
            'lecture': {},
            'practice': {}
        }

        open_answers = dict()
        questions = await db_commands.get_all_questions()
        for question in questions:
            if question.id in results_cb.keys():
                if question.type == 'lecture':
                    results['lecture'].update({f'{question.id}': results_cb[question.id]})

                elif question.type == 'practice':
                    results['practice'].update({f'{question.id}': results_cb[question.id]})
                elif question.type == 'both':
                    results['lecture'].update({f'{question.id}': results_cb[question.id]})

                    results['practice'].update({f'{question.id}': results_cb[question.id]})
                elif question.type == 'open':
                    open_answers.update({f'{question.id}': results_cb[question.id]})


        if teacher_type == 'lecture':
            del results['practice']
        elif teacher_type == 'practice':
            del results['lecture']

        logging.info(f'User <{user_tg_id}> voted for teacher <{teacher_id}>. Saving results...')
        try:
            await db_commands.add_vote(faculty, user.id, teacher_id, results, open_answers)
            await call.message.answer('Опитування закінчено, дані збережені.\nДякуємо за участь!\n\nНатисніть /start'
                                  ' щоб почати нове опитування')
        except Exception as e:
            await call.message.answer('Помилка! Результати опитування не збережені!')
            logging.critical(f'User <{user_tg_id}> - teacher <{teacher_id}> -- Saving error - {e}')

        await state.finish()
        await call.answer()


@dp.message_handler(commands=['list', 'ls'])
async def list_cmd_handler(message: types.Message):
    user = await db_commands.get_user_by_tg_id(message.from_user.id)

    if user is not None:
        group_teachers = []
        ls = ''
        groups = await db_commands.get_all_groups(faculties[faculties_ukr.index(user.faculty)])
        for group in groups:
            if group.id == user.group_id:
                try:
                    for teacher in group.teachers:
                        if teacher['full_name'] not in group_teachers:
                            if teacher['full_name'] not in group_teachers:
                                group_teachers.append(teacher['full_name'])

                    for i in group_teachers:
                        ls = ls + '\n' + i
                    if ls.strip() != '':
                        await message.answer(f'Викладачі, які можуть бути вам цікаві:\n\n{ls}')
                    else:
                        raise Exception

                except Exception as e:
                    logging.warning(f'No teachers in group <{group.id}>. Chat with user <{user.id}>')
                    await message.answer('На жаль, за Вашою групою не знайдено жодного викладача.\n'
                                   'Якщо Ви вважаєте, що сталась помилка, то зверніться до студради Вашого факультету.')
    else:
        await message.answer('Ви не зареєстровані!')


@dp.message_handler(content_types=['text'])
async def other_msg_handler(message: types.Message):
    if await is_throttled(message) is True:
        return -1

    await message.answer(config.start_suggestion_msg)



