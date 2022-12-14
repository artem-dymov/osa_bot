import requests
import json
from utils.db_api.models import faculties_ukr, faculties
from utils.db_api import db_commands
import asyncio
from utils.db_api.database import create_db, drop_connection

for faculty in faculties:
    groups_schedule_ids = await db_commands.get_all_groups_schedule_id(faculty)

    for group_schedule_id in groups_schedule_ids:

        res = requests.get(f"https://schedule.kpi.ua/api/schedule/lessons?groupId={group_schedule_id}")

        py_res = json.loads(res.text)

        for day in py_res['data']['scheduleFirstWeek']:
            for teacher in day:
                pass
py_res = json.loads(res.text)