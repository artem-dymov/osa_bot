import requests
import json
from utils.db_api.models import Teacher, Group, Group_classes, Teacher_classes
from config import faculties, faculties_ukr
from utils.db_api import db_commands
import asyncio
from utils.db_api.database import create_db, drop_connection

res_groups = requests.get('https://schedule.kpi.ua/api/schedule/groups')
py_res_groups = json.loads(res_groups.text)


async def determine_teacher_type(type_text: str):
    if ("Прак" in type_text) or ("Лаб" in type_text):
        return "practice"
    elif "Лек" in type_text:
        return "lecture"
    elif type_text.strip() == "" or type_text is None:
        return ""
    else:
        return None


async def main():
    await create_db()

    for faculty in faculties:
        faculty_index = faculties.index(faculty)
        faculty_ukr: str = faculties_ukr[faculty_index]

        for group in py_res_groups['data']:
            print(group)

            if group['faculty'] == faculty_ukr:
                new_group = {
                    'name': group['name'],
                    'schedule_id': group['id'],
                    'teachers': []
                }

                res_teachers = requests.get(f"https://schedule.kpi.ua/api/schedule/lessons?groupId={group['id']}")
                py_res_teachers = json.loads(res_teachers.text)

                for day in py_res_teachers['data']['scheduleFirstWeek']:
                    for pair in day['pairs']:
                        teacher_type = await determine_teacher_type(pair['type'])
                        lecturer_id = pair['lecturerId']

                        if (teacher_type is not None) and (lecturer_id != ''):
                            new_teacher = await db_commands.get_teacher_by_schedule_id(faculty, lecturer_id)

                            if new_teacher is not None:
                                print('1')
                                if new_teacher.type == teacher_type:
                                    pass
                                if new_teacher.type != teacher_type:
                                    if new_teacher.type.strip() == '':
                                        if teacher_type == 'lecture':
                                            await db_commands.update_teacher(faculty, lecturer_id, new_teacher.full_name,
                                                                             'both')
                                        elif teacher_type == 'practice':
                                            await db_commands.update_teacher(faculty, lecturer_id, new_teacher.full_name,
                                                                             'practice')
                                    else:
                                        await db_commands.update_teacher(faculty, lecturer_id, new_teacher.full_name,
                                                                         'both')
                            elif new_teacher is None:
                                print('2')
                                await db_commands.add_teacher(faculty, pair['teacherName'], teacher_type, lecturer_id)


                            new_teacher = await db_commands.get_teacher_by_schedule_id(faculty, lecturer_id)

                            print(f"{new_teacher} + {pair['teacherName']} + {lecturer_id}, {teacher_type}")
                            print(f"itering {new_teacher.full_name}")

                            repeat = False
                            for i in new_group['teachers']:
                                print(f"{new_teacher.full_name} = {i['full_name']} --- {new_teacher.id} = {i['id']}")
                                if i['id'] == new_teacher.id and teacher_type == i['type']:
                                    repeat = True

                            if repeat is False:
                                new_group['teachers'].append({
                                    'id': new_teacher.id,
                                    'full_name': new_teacher.full_name,
                                    'type': teacher_type
                                })

                for day in py_res_teachers['data']['scheduleSecondWeek']:
                    for pair in day['pairs']:
                        teacher_type = await determine_teacher_type(pair['type'])
                        lecturer_id = pair['lecturerId']

                        if (teacher_type is not None) and (lecturer_id != ''):
                            new_teacher = await db_commands.get_teacher_by_schedule_id(faculty, lecturer_id)

                            if new_teacher is not None:
                                if new_teacher.type == teacher_type:
                                    pass
                                if new_teacher.type != teacher_type:
                                    if new_teacher.type.strip() == '':
                                        if teacher_type == 'lecture':
                                            await db_commands.update_teacher(faculty, lecturer_id, new_teacher.full_name,
                                                                             'both')
                                        elif teacher_type == 'practice':
                                            await db_commands.update_teacher(faculty, lecturer_id, new_teacher.full_name,
                                                                             'practice')
                                    else:
                                        await db_commands.update_teacher(faculty, lecturer_id, new_teacher.full_name,
                                                                         'both')
                            elif new_teacher is None:
                                await db_commands.add_teacher(faculty, pair['teacherName'], teacher_type, lecturer_id)

                            new_teacher = await db_commands.get_teacher_by_schedule_id(faculty, lecturer_id)

                            print(f"{new_teacher} + {pair['teacherName']}")
                            print(f"itering {new_teacher.full_name}")

                            repeat = False
                            for i in new_group['teachers']:
                                print(f"{new_teacher.full_name} = {i['full_name']} --- {new_teacher.id} = {i['id']}")
                                if i['id'] == new_teacher.id and teacher_type == i['type']:
                                    repeat = True

                            if repeat is False:
                                new_group['teachers'].append({
                                    'id': new_teacher.id,
                                    'full_name': new_teacher.full_name,
                                    'type': teacher_type
                                })

                is_group_in_db = await db_commands.is_group_in_db_legacy(faculty, new_group['schedule_id'])

                if is_group_in_db is False:
                    await db_commands.add_group(faculty, **new_group)
                elif is_group_in_db is True:
                    current_group = await db_commands.get_group_by_name(new_group['name'])
                    current_group.teachers.append()
                    await db_commands.update_group(current_group.id, **new_group)

    await drop_connection()

asyncio.get_event_loop().run_until_complete(main())


