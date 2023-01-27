from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from config import faculties, faculties_ukr

from aiogram import types

# confirmation callback values: -1 for empty, 0 for False, 1 for True
faculty_cd: CallbackData = CallbackData("id_faculty", "faculty_index", "confirmation_faculty",)


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

# confirmation_group - '0' for False, '1' for True
group_cd: CallbackData = CallbackData("id_group", "confirmation_group",)


async def group_confirmation_markup():
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(text='Так', callback_data=group_cd.new('1'))
    )

    markup.row(
        InlineKeyboardButton(text='Ні', callback_data=group_cd.new('0'))
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

# markup_type - possible values: '1_5' or 'yes/no'
questions_cd: CallbackData = CallbackData('id', 'question_id', 'answer', 'markup_type')


# selected option - number from 1 to 5, describes near what number will be checkmark
async def poll_1_5_markup(question_id, selected_option=None):
    markup = InlineKeyboardMarkup(row_width=5)
    for i in range(1, 6):
        if selected_option == i:
            markup.insert(InlineKeyboardButton(text=f"{i}✅", callback_data=questions_cd.new(question_id, i, '1_5')))
        else:
            markup.insert(InlineKeyboardButton(text=f"{i}", callback_data=questions_cd.new(question_id, i, '1_5')))

    return markup


async def poll_yes_no_markup(question_id, selected_option=None):
    markup = InlineKeyboardMarkup()
    for i in range(0, 2).__reversed__():
        text = ''
        if i == 1:
            text = 'Так'
        elif i == 0:
            text = 'Ні'

        if i == selected_option:
            markup.add(
                InlineKeyboardButton(text=text+'✅', callback_data=questions_cd.new(question_id, i, 'yes/no'))
            )
        else:
            markup.add(
                InlineKeyboardButton(text=text, callback_data=questions_cd.new(question_id, i, 'yes/no'))
            )
    return markup

# confirmation: 1 - True (Yes), 0 - False (No)
# is_final_q: 1 - True, 0 - False
open_q_confrimation_cd: CallbackData = CallbackData('ikd', 'question_id', 'confirmation', 'is_final_q')


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
