from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from utils.db_api.models import faculties, faculties_ukr

from aiogram import types

# confirmation callback values: -1 for empty, 0 for False, 1 for True
faculty_cd: CallbackData = CallbackData("id", "faculty_index", "confirmation_faculty",)


async def faculty_markup():
    markup = InlineKeyboardMarkup()
    for i in faculties_ukr:
        markup.row(
            InlineKeyboardButton(text=i, callback_data=faculty_cd.new(faculties_ukr.index(i), -1))
        )

    return markup


async def faculty_confirmation_markup(faculty_index):
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(text='Так', callback_data=faculty_cd.new(faculty_index, 1))
    )

    markup.row(
        InlineKeyboardButton(text='Ні', callback_data=faculty_cd.new(faculty_index, 0))
    )

    return markup


# teacher_type: 0 - for lecture, 1 - for practice (labs/''), 2 - for lecture+practice
teacher_cd: CallbackData = CallbackData('id', 'faculty_index', 'teacher_type', 'teacher_id')


async def teacher_type_markup(faculty_index: str, teacher_id):
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(text='Лекції', callback_data=teacher_cd.new(faculty_index, 0, teacher_id))
    )

    markup.row(
        InlineKeyboardButton(text='Практики', callback_data=teacher_cd.new(faculty_index, 1, teacher_id,))
    )

    markup.row(
        InlineKeyboardButton(text='Лек+Прак', callback_data=teacher_cd.new(faculty_index, 2, teacher_id))
    )
    return markup


async def start_inline_search_markup():
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(text='Обрати викладача', switch_inline_query_current_chat='')
    )
    return markup


questions_cd: CallbackData = CallbackData('id', 'question_id', 'answer')

async def poll_1_5_markup(question_id):
    markup = InlineKeyboardMarkup(row_width=5)
    for i in range(1, 6):
        markup.insert(InlineKeyboardButton(text=f"{i}", callback_data=questions_cd.new(question_id, i)))


    return markup


async def poll_yes_no_markup(question_id):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(text='Так', callback_data=questions_cd.new(question_id, 1)),
        InlineKeyboardButton(text='Ні', callback_data=questions_cd.new(question_id, 0))
    )

    return markup

# confirmation: 1 - True (Yes), 0 - False (No)
# is_final_q: 1 - True, 0 - False
open_q_confrimation_cd: CallbackData = CallbackData('id', 'question_id', 'confirmation', 'is_final_q')


async def open_q_confirmation_markup(question_id: int, is_final_q: bool):

    if is_final_q is True:
        is_final_q = 1
    else:
        is_final_q = 0

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(text='Так', callback_data=open_q_confrimation_cd.new(question_id, 1, is_final_q)),
        InlineKeyboardButton(text='Ні', callback_data=open_q_confrimation_cd.new(question_id, 0, is_final_q))
    )

    return markup
