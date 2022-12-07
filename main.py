import asyncio
from database import create_db, drop_connection
from models import User, Teacher, Teacher_classes, Vote, Vote_classes
import db_commands

async def main():
    await create_db()

    # your code here
    # <example 1
    # user: User = await db_commands.get_user(4)
    # print(user.faculty)
    # example>

    # Пример записи голоса из бота в базу
    # questions_id = [1, 2, 3]
    # marks = [4, 5, 4]
    # await db_commands.add_vote('FBME', 5, 2, marks, questions_id)

    # Пример получения всех голосов с опроса по факультету и вывод оценок
    votes = await db_commands.get_all_votes('FBME')
    for vote in votes:
        print(vote.marks)

    # добавление препода
    # await db_commands.add_teacher('FBME', 'Bakun V B', 'practice', [['bs-11', 'bs-12', 'bs-13'], ['bs-11']])

    # получение препода по айдишнику с бд
    # teacher = await db_commands.get_teacher('FBME', 5)
    # print(teacher.groups)



    await drop_connection()

asyncio.get_event_loop().run_until_complete(main())
