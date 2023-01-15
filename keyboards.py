from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from utils.db_api.models import faculties, faculties_ukr

from aiogram import types

# confirmation callback values: -1 for empty, 0 for False, 1 for True
faculty_cd: CallbackData = CallbackData("id", "faculty_index", "group_name", "confirmation_faculty", "confirmation_group",)


async def faculty_markup():
    markup = InlineKeyboardMarkup()
    for i in faculties_ukr:
        markup.row(
            InlineKeyboardButton(text=i, callback_data=faculty_cd.new(faculties_ukr.index(i), '', -1, -1))
        )

    return markup


async def faculty_confirmation_markup(faculty_index):
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(text='Так', callback_data=faculty_cd.new(faculty_index, '', '1', -1))
    )

    markup.row(
        InlineKeyboardButton(text='Ні', callback_data=faculty_cd.new(faculty_index, '', 0, -1))
    )

    return markup


async def group_confirmation_markup(faculty_index, group_name):
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(text='Так', callback_data=faculty_cd.new(faculty_index, '', -1, 1))
    )

    markup.row(
        InlineKeyboardButton(text='Ні', callback_data=faculty_cd.new(faculty_index, '', -1, 0))
    )

    return markup
