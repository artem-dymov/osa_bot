import json
from utils.db_api.models import faculties_ukr, faculties, Teacher, Group, Group_classes, Teacher_classes
from utils.db_api import db_commands
import asyncio
from utils.db_api.database import create_db, drop_connection

required_id: int = 2382


async def main():
    await create_db()

    groups = await db_commands.get_all_groups("ipt")
    for group in groups:
        for teacher in group.teachers:
            if teacher['id'] == required_id:
                t = await db_commands.get_teacher('ipt', teacher['id'])
                print(f"{required_id}, {t.full_name} --- {group.name}")

    await drop_connection()


async def test():
    await create_db()

    group = await db_commands.get_group_by_name('fbme', 'бс-11')
    print(group.name)
    print(group.teachers)
    await drop_connection()

# asyncio.get_event_loop().run_until_complete(main())
asyncio.get_event_loop().run_until_complete(test())