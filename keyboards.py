from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from utils.db_api.models import faculties, faculties_ukr

from aiogram import types

faculty_cd: CallbackData = CallbackData("id", "faculty_index")



async def faculty_markup():
    markup = InlineKeyboardMarkup()
    for i in faculties_ukr:
        markup.row(
            InlineKeyboardButton(text=i, callback_data=faculty_cd.new(faculties_ukr.index(i)))
        )

    return markup

