from utils.db_api.models import User, Teacher, Teacher_classes, Vote, Vote_classes, Group, Group_classes

from typing import Union


async def get_user_by_tg_id(tg_id: int) -> User:
    user: User = await User.query.where(User.tg_id == tg_id).gino.first()
    return user


async def get_user(id: int) -> User:
    user: User = await User.get(id)
    return user


async def add_user(tg_id: int, faculty: str, group, username=None) -> User:
    new_user: User = await User(tg_id=tg_id, username=username, faculty=faculty, group=group).create()
    return new_user


async def is_user_in_db(tg_id: int):
    user: User = await get_user_by_tg_id(tg_id)

    if user is not None:
        return True
    else:
        return False


# adds Nones to matrix if it is needed, returning lists without nested lists
async def space_filler_in_matrix(matrix: list[list, list]) -> list[list, list]:
    error_msg: str = "Matrix variable must be a list with 2 nested lists to be filled with None or with 1 nested list" + \
                " to be returned back."

    if len(matrix) == 2:
        if type(matrix[0]) == list and type(matrix[1] == list):
            x: int = len(matrix[0])
            y: int = len(matrix[1])

            if x == y:
                return matrix
            else:
                if x > y:
                    for i in range(x - y):
                        matrix[1].append(None)
                if x < y:
                    for i in range(y - x):
                        matrix[0].append(None)
                return matrix
        else:
            raise TypeError(error_msg)

    elif len(matrix) == 1:
        return matrix

    else:
        raise TypeError(error_msg)


# deleting Nones from list/matrix
async def space_unfiller_in_matrix(matrix: list) -> list:
    new_matrix = []

    for i in matrix:
        if i is not None:
            if type(i) == list:
                new_i = []
                for k in i:
                    if k is not None:
                        new_i.append(k)
                new_matrix.append(new_i)
            else:
                new_matrix.append(i)

    return new_matrix


async def get_teacher(faculty: str, id: int) -> Teacher:
    teacher: Teacher = await Teacher_classes[faculty].get(id)
    if teacher.groups is not None:
        teacher.groups = await space_unfiller_in_matrix(teacher.groups)
    return teacher


async def get_all_teachers(faculty: str) -> Teacher:
    teachers: Teacher = await Teacher_classes[faculty].query.gino.all()
    for teacher in teachers:
        if teacher.groups is not None:
            teacher.groups = await space_unfiller_in_matrix(teacher.groups)
    return teachers


async def add_teacher(faculty: str, full_name: str, type: str,
                      groups: Union[list[str], list[list[str], list[str]]]) -> Teacher:
    groups = await space_filler_in_matrix(groups)
    print(groups)

    for teacher in Teacher_classes:
        print(teacher)
    new_teacher: Teacher = await Teacher_classes[faculty](full_name=full_name, type=type, groups=groups).create()

    return new_teacher


async def get_vote(faculty: str, id: int) -> Vote:
    vote: Vote = await Vote_classes[faculty].get(id)
    vote.marks = await space_unfiller_in_matrix(vote.marks)
    vote.questions_id = await space_unfiller_in_matrix(vote.questions_id)
    return vote


async def get_all_votes(faculty: str) -> list[Vote]:
    votes: list[Vote] = await Vote_classes[faculty].query.gino.all()
    for vote in votes:
        vote.marks = await space_unfiller_in_matrix(vote.marks)
        vote.questions_id = await space_unfiller_in_matrix(vote.questions_id)
    return votes


async def get_votes_by_teacher_id(faculty: str, teacher_id: int) -> list[Vote]:
    votes: list[Vote] = await Vote_classes[faculty].query.where(teacher_id=teacher_id).gino.all()
    for vote in votes:
        vote.marks = await space_unfiller_in_matrix(vote.marks)
        vote.questions_id = await space_unfiller_in_matrix(vote.questions_id)
    return votes


async def add_vote(faculty: str, user_id: int, teacher_id: int,
                   marks: Union[list[int], list[list[int], list[int]]],
                   questions_id: Union[list[int], list[list[int], list[int]]]) -> Vote:
    error_msg = "Variables questions_id and marks must have the same number of elements (in nested lists too)."

    marks_len = len(marks)
    questions_id_len = len(questions_id)
    if marks_len == 2:
        marks = await space_filler_in_matrix(marks)

    if questions_id_len == 2:
        questions_id = await space_filler_in_matrix(questions_id)

    if marks_len != questions_id_len:
        raise TypeError(error_msg)

    if marks_len == 2 and questions_id_len == 2:
        if len(marks[0]) != len(questions_id[0]) or len(marks[1]) != len(questions_id[1]):
            raise TypeError(error_msg)

    vote: Vote = await Vote_classes[faculty](user_id=user_id, teacher_id=teacher_id,
                                             marks=marks, questions_id=questions_id).create()

    return vote


async def get_all_groups_names(faculty: str) -> list[str]:
    groups: list[Group] = await Group_classes[faculty].query.gino.all()

    names = []
    for i in groups:
        names.append(i.name)

    return names


async def is_group_in_db(faculty: str, group: str) -> bool:
    groups = await get_all_groups_names(faculty)
    if group.strip() in groups:
        return True
    else:
        return False


async def add_groups(faculty: str, groups: list[str]) -> None:
    for i in groups:
        group: Group = await Group_classes[faculty](name=i).create()
