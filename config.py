import json
import os

faculties = ('fbme', 'ipp', 'fl', 'fel', 'its', 'ipt', 'imi')
faculties_ukr = ('ФБМІ', 'ВПІ', 'ФЛ', 'ФЕЛ', 'ІТС', 'ФТІ', 'ММІ')


with open('settings.json', 'r') as file:
    py_data = json.load(file)
    BOT_TOKEN = py_data['BOT_TOKEN']
    POSTGRESQL_URL = py_data['POSTGRESQL_URL']

skip_message = 'Щоб пропустити це питання, натисніть /skip'

cancel_vote_msg = 'Щоб відмінити голосування натисніть /cancel'

start_suggestion_msg = 'Натисніть /start щоб почати опитування\n\nНатисніть /list щоб подивитись список викладачів'