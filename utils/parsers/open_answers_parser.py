import asyncio
import os
from config import faculties, faculties_ukr
from utils.db_api.database import create_db, drop_connection
from utils.db_api import db_commands


async def main():
    await create_db()

    for faculty in faculties:
        faculty_ukr = faculties_ukr[faculties.index(faculty)]
        teachers = await db_commands.get_all_teachers(faculty)
        votes = await db_commands.get_all_votes(faculty)

        try:
            open_micro_file = open(f'open_answers_results/{faculty_ukr}/відкритий_мікрофон.txt', 'w')
            anon_file = open(f'open_answers_results/{faculty_ukr}/анонімні_відповіді.txt', 'w')
        except FileNotFoundError:
            os.mkdir(f'open_answers_results/{faculty_ukr}')

            open_micro_file = open(f'open_answers_results/{faculty_ukr}/відкритий_мікрофон.txt', 'w')
            anon_file = open(f'open_answers_results/{faculty_ukr}/анонімні_відповіді.txt', 'w')

        open_micro_results = ''
        anon_results = ''

        for teacher in teachers:

            for vote in votes:
                if vote.teacher_id == teacher.id:
                    first_open = list(vote.open_answers.values())[0]
                    if first_open.strip() != '':
                        open_micro_results += f'Викладач: {teacher.full_name}\nВідповідь: {first_open}\n\n'

                    second_open = list(vote.open_answers.values())[1]
                    if second_open.strip() != '':
                        anon_results += f'Викладач: {teacher.full_name}\nВідповідь: {second_open}\n\n'

        open_micro_file.write(open_micro_results)
        anon_file.write(anon_results)

        open_micro_file.close()
        anon_file.close()

    await drop_connection()


asyncio.get_event_loop().run_until_complete(main())
