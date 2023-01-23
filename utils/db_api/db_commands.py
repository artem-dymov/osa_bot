from utils.db_api.models import User, Teacher, Teacher_classes, Vote, Vote_classes, Group, Group_classes, Question
from utils.db_api.models import faculties, faculties_ukr
from typing import Union
from sqlalchemy import func


async def get_user_by_tg_id(tg_id: int) -> User:
    user: User = await User.query.where(User.tg_id == tg_id).gino.first()
    return user


async def get_user(id: int) -> User:
    user: User = await User.get(id)
    return user


async def add_user(tg_id: int, faculty_ukr: str, group_id=None, username=None) -> User:
    new_user: User = await User(tg_id=tg_id, username=username, faculty=faculty_ukr, group_id=group_id).create()
    return new_user


async def is_user_in_db(tg_id: int) -> bool:
    user: User = await get_user_by_tg_id(tg_id)

    if user is not None:
        return True
    else:
        return False


async def update_user(tg_id: int, **kwargs) -> None:
    user: User = await get_user_by_tg_id(tg_id)
    await user.update(**kwargs).apply()


async def get_user_faculty_by_tg_id(tg_id) -> str:
    user: User = await get_user_by_tg_id(tg_id)
    if user is not None:
        return user.faculty
    else:
        return None


async def get_teacher(faculty: str, id: int) -> Teacher:
    teacher: Teacher = await Teacher_classes[faculty].get(id)
    return teacher


async def get_teacher_by_schedule_id(faculty: str, schedule_id) -> Teacher:
    teacher: Teacher = await Teacher_classes[faculty].query.where(Teacher_classes[faculty].schedule_id == schedule_id).gino.first()
    return teacher


async def get_all_teachers(faculty: str) -> list[Teacher]:
    teachers: Teacher = await Teacher_classes[faculty].query.gino.all()
    return teachers


async def add_teacher(faculty: str, full_name: str, type: str, schedule_id=None) -> Teacher:
    new_teacher: Teacher = await Teacher_classes[faculty](full_name=full_name, type=type, schedule_id=schedule_id).create()
    return new_teacher


async def get_vote(faculty: str, id: int) -> Vote:
    vote: Vote = await Vote_classes[faculty].get(id)
    return vote


async def get_all_votes(faculty: str) -> list[Vote]:
    votes: list[Vote] = await Vote_classes[faculty].query.gino.all()
    return votes


async def get_votes_by_teacher_id(faculty: str, teacher_id: int) -> list[Vote]:
    votes: list[Vote] = await Vote_classes[faculty].query.where(Vote_classes[faculty].teacher_id == teacher_id).gino.all()
    return votes


# {"lecture": {"questions_ids": [1, 2, 3], "marks": [5, 5, 4]}, "pracrice": {"questions_ids": [4, 5, 3], "marks": [4, 5, 4]}}
# example of variable results
# results = {
#   "lecture": {"questions_ids": [1, 2, 3], "marks": [5, 5, 4]},
#   "pracrice": {"questions_ids": [4, 5, 3], "marks": [4, 5, 4]}
# }
# results must have at least 1 pair, maximum - 2 pairs
async def add_vote(faculty: str, user_id: int, teacher_id: int, results: dict, open_answers: dict) -> Vote:
    vote: Vote = await Vote_classes[faculty](user_id=user_id, teacher_id=teacher_id,
                                             results=results, open_answers=open_answers).create()
    return vote


async def get_all_groups(faculty: str) -> list[Group]:
    groups: list[Group] = await Group_classes[faculty].query.gino.all()
    return groups


async def get_group_by_schedule_id(faculty: str, schedule_id: int) -> Group:
    group: Group = await Group_classes[faculty].query.where(Group_classes[faculty].schedule_id == schedule_id).gino.first()
    return group


# 'faculty' accepts values both in Ukrainian and in English
async def get_all_groups_names(faculty: str) -> list[str]:
    groups: list[Group] = await Group_classes[faculty].query.gino.all()
    names = []
    for i in groups:
        names.append(i.name)
    return names


async def get_all_groups_schedule_id(faculty: str) -> list[str]:
    groups: list[Group] = await Group_classes[faculty].query.gino.all()
    schedule_ids = []
    for i in groups:
        schedule_ids.append(i.schedule_id)

    return schedule_ids


# поиск с учетом регистра
async def is_group_in_db_legacy(faculty: str, group_name: str) -> bool:
    groups = await get_all_groups_names(faculty)
    if group_name in groups:
        return True
    else:
        return False


async def get_group_id_by_name(faculty: str, group_name: str) -> Group:
    print(faculty, group_name)
    groups = await get_all_groups_names(faculty)
    group_name = group_name.lower().strip()
    group_index = None
    for i in groups:
        j = i.lower().strip()
        if group_name in j:
            print(f" X - {group_name} = {j}")
            group = await Group_classes[faculty].query.where(Group_classes[faculty].name == i).gino.first()
            print(group_name, group)
            return group.id


async def is_group_in_db(faculty: str, group_name: str) -> bool:

    if (faculty not in faculties) and (faculty in faculties_ukr):
        print("if")
        faculty = faculties[faculties_ukr.index(faculty)]

    print(f"KEy {faculty}")
    groups = await get_all_groups_names(faculty)
    group_name = group_name.lower()
    for i in groups:
        j = i.lower()
        if group_name == j:
            return True

    return False


async def get_group_by_name(faculty: str, group_name: str) -> Group:
    group = await Group_classes[faculty].query.where(Group_classes[faculty].name == group_name).gino.first()
    return group


async def is_teacher_in_db_schedule(faculty: str, schedule_id: str) -> bool:
    teacher = await Teacher_classes[faculty].query.where(schedule_id == schedule_id).gino.first()
    if teacher is None:
        return True
    else:
        return False


async def is_teacher_in_db(faculty: str, full_name: str) -> bool:
    teachers = await get_all_teachers(faculty)
    for teacher in teachers:
        if full_name.lower().strip() == teacher.full_name.lower().strip():
            return True

    return False


async def get_teacher_by_name(faculty: str, full_name: str):
    teachers = await get_all_teachers(faculty)
    for teacher in teachers:
        if full_name.lower().strip() == teacher.full_name.lower().strip():
            return teacher


async def add_group(faculty: str, name: str, schedule_id: str, teachers: list[dict]) -> None:
    await Group_classes[faculty](schedule_id=schedule_id, name=name, teachers=teachers).create()


async def update_group(faculty, schedule_id, **kwargs):
    group: Group = get_group_by_schedule_id(faculty, schedule_id)
    await group.update(**kwargs).apply()


async def update_teacher(faculty, schedule_id, full_name, type):
    teacher: Teacher = await get_teacher_by_schedule_id(faculty, schedule_id)
    await teacher.update(full_name=full_name, schedule_id=schedule_id, type=type).apply()
    return teacher


async def search_teachers_by_name(faculty: str, full_name: str) -> list[str]:
    result = []
    for i in await get_all_teachers(faculty):
        if full_name.lower() in i.full_name.lower() and i.full_name not in result:
            result.append(i.full_name)

    print(result)
    # if result is empty
    if not result:
        return None
    else:
        return result


async def get_all_questions() -> list[Question]:
    questions: Question = await Question.query.gino.all()
    return questions


async def get_question(id):
    question: Question = await Question.get(id)
    return question


async def is_teacher_voted(user_id: int, teacher_id: int, faculty: str) -> bool:
    votes = await get_all_votes(faculty)

    for vote in votes:
        if teacher_id == vote.teacher_id:
            return True

    return False