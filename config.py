import json

faculties =     ('fbme', 'ipp', 'fel', 'its', 'ipt', 'fbt', 'fsl', 'tef', 'imz')
faculties_ukr = ('ФБМІ', 'ВПІ', 'ФЕЛ', 'ІТС', 'ФТІ', 'ФБТ', 'ФСП', 'ІАТЕ', 'ІМЗ')

global BOT_TOKEN
global DATABASE_URL
global ANTIFLOOD_RATE

def _get_data():
    with open('settings.json', 'r') as file:
        global BOT_TOKEN
        global DATABASE_URL
        global ANTIFLOOD_RATE

        py_data = json.load(file)

        BOT_TOKEN = py_data['BOT_TOKEN']
        DATABASE_URL = py_data['DATABASE_URL']
        ANTIFLOOD_RATE = py_data['ANTIFLOOD_RATE']

        print(DATABASE_URL)


try:
    _get_data()
except FileNotFoundError:
    import os
    os.chdir('../..')
    _get_data()
except Exception as e:
    print(e)


skip_message = 'Щоб пропустити це питання, натисніть /skip'

cancel_vote_msg = 'Щоб відмінити голосування натисніть /cancel'

start_suggestion_msg = 'Натисніть /start щоб почати опитування\n\nНатисніть /list щоб подивитись список викладачів'

teacher_non_type_msg = 'Якщо у вас немає поділення на лекції і практики, обирайте практики.'
