import requests
import json
from utils.db_api.models import faculties_ukr, faculties
from utils.db_api import db_commands
import asyncio
from utils.db_api.database import create_db, drop_connection

res = requests.get('https://schedule.kpi.ua/api/schedule/groups')

py_res = json.loads(res.text)


async def main():
    await create_db()

    for faculty in faculties_ukr:
        groups = []
        for i in py_res['data']:
            if i['faculty'] == faculty:
                print(i['name'])
                groups.append(i['name'])

            if len(groups) > 0:
                faculty_index = faculties_ukr.index(faculty)
                await db_commands.add_groups(faculties[faculty_index], groups)
            groups.clear()

    await drop_connection()


asyncio.get_event_loop().run_until_complete(main())


