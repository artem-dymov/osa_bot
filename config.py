import json

faculties = ('fbme', 'ipp', 'fl', 'fel', 'its', 'ipt', 'imi')
faculties_ukr = ('ФБМІ', 'ВПІ', 'ФЛ', 'ФЕЛ', 'ІТС', 'ФТІ', 'ММІ')


with open('settings.json', 'r') as file:
    py_data = json.load(file)
    BOT_TOKEN = py_data['BOT_TOKEN']
    POSTGRESQL_URL = py_data['POSTGRESQL_URL']
    ANTIFLOOD_RATE = py_data['ANTIFLOOD_RATE']

skip_message = 'Щоб пропустити це питання, натисніть /skip'

cancel_vote_msg = 'Щоб відмінити голосування натисніть /cancel'

start_suggestion_msg = 'Натисніть /start щоб почати опитування\n\nНатисніть /list щоб подивитись список викладачів'

teacher_non_type_msg = 'Якщо у вас немає поділення на лекції і практики, обирайте практики.'
