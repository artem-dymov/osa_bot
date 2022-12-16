
from utils.db_api.models import User, Teacher, Teacher_classes, Vote, Vote_classes, Group, Group_classes
from typing import Union


async def get_user_by_tg_id(tg_id: int) -> User:
    user: User = await User.query.where(User.tg_id == tg_id).gino.first()
    return user


async def get_user(id: int) -> User:
    user: User = await User.get(id)
    return user


async def add_user(tg_id: int, faculty: str, group_id=None, username=None) -> User:
    new_user: User = await User(tg_id=tg_id, username=username, faculty=faculty, group_id=group_id).create()
    return new_user


async def is_user_in_db(tg_id: int):
    user: User = await get_user_by_tg_id(tg_id)

    if user is not None:
        return True
    else:
        return False


async def update_user(tg_id: int, **kwargs):
    user: User = get_user_by_tg_id(tg_id)
    await user.update(**kwargs).apply()


async def get_teacher(faculty: str, id: int) -> Teacher:
    teacher: Teacher = await Teacher_classes[faculty].get(id)
    return teacher


async def get_teacher_by_schedule_id(faculty: str, schedule_id) -> Teacher:
    teacher: Teacher = await Teacher_classes[faculty].query.where(Teacher_classes[faculty].schedule_id == schedule_id).gino.first()
    return teacher


async def get_all_teachers(faculty: str) -> Teacher:
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
    votes: list[Vote] = await Vote_classes[faculty].query.where(teacher_id=teacher_id).gino.all()
    return votes


# example of variable results
# results = {
#   "lecture": {"questions_ids": [1, 2, 3], "marks": [5, 5, 4]},
#   "pracrice": {"questions_ids": [4, 5, 3], "marks": [4, 5, 4]}
# }
# results must have at least 1 pair, maximum - 2 pairs
async def add_vote(faculty: str, user_id: int, teacher_id: int, results: dict) -> Vote:
    vote: Vote = await Vote_classes[faculty](user_id=user_id, teacher_id=teacher_id,
                                             results=results).create()
    return vote


async def get_all_groups(faculty: str) -> list[Group]:
    groups: list[Group] = await Group_classes[faculty].query.gino.all()
    return groups


async def get_group_by_schedule_id(faculty: str, schedule_id: int) -> Group:
    group: Group = await Group_classes[faculty].query.where(schedule_id=schedule_id).gino.first()
    return group


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


async def is_group_in_db(faculty: str, group_name: str) -> bool:
    groups = await get_all_groups_names(faculty)
    if group_name in groups:
        return True
    else:
        return False


async def get_group_by_name(faculty: str, group_name: str) -> Group:
    group = await Group_classes[faculty].query.where(name=group_name).gino.first()
    return group


async def is_teacher_in_db(faculty: str, schedule_id: str) -> bool:
    teacher = await Teacher_classes[faculty].query.where(schedule_id == schedule_id).gino.first()
    if teacher is None:
        return True
    else:
        return False



async def add_group(faculty: str, name: str, schedule_id: str, teachers: list[dict]) -> None:
    await Group_classes[faculty](schedule_id=schedule_id, name=name, teachers=teachers).create()


async def update_group(faculty, schedule_id, **kwargs):
    group: Group = get_group_by_schedule_id(faculty, schedule_id)
    await group.update(**kwargs).apply()

async def update_teacher(faculty, schedule_id, full_name, type):
    teacher: Teacher = await get_teacher_by_schedule_id(faculty, schedule_id)
    await teacher.update(full_name=full_name, schedule_id=schedule_id, type=type).apply()
    return teacher
