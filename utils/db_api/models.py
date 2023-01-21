from utils.db_api.database import db
from sqlalchemy import sql, Column, Sequence, INTEGER, TEXT, ARRAY, BIGINT, JSON


faculties = ('fbme', 'ipp', 'fl', 'fel', 'its', 'ipt', 'imi')
faculties_ukr = ('ФБМІ', 'ВПІ', 'ФЛ', 'ФЕЛ', 'ІТС', 'ФТІ', 'ММІ')


class User(db.Model):
    __table_args__ = dict(schema='public')
    __tablename__ = 'users'
    query: sql.Select

    id = Column(INTEGER, Sequence("users_id_seq"), primary_key=True)
    tg_id = Column(BIGINT)
    username = Column(TEXT)
    faculty = Column(TEXT)
    group_id = Column(INTEGER)


class Teacher(db.Model):
    __tablename__ = 'teachers'
    query: sql.Select

    id = Column(INTEGER, Sequence("teachers_id_seq"), primary_key=True)
    full_name = Column(TEXT)
    type = Column(TEXT)
    schedule_id = Column(TEXT)


Teacher_classes: Teacher = {}  # : dict[str, Teacher]
for i in faculties:
    Teacher_classes[f"{i}"] = (type(f"Teacher_{i}", (db.Model,), {"__table_args__" : {"schema" : f"{i}"} , "__tablename__": "teachers",
                                "id": Column(INTEGER, Sequence("teachers_id_seq", schema=i), primary_key=True),
                                "full_name": Column(TEXT),
                                "type": Column(TEXT),
                                "schedule_id": Column(TEXT)}))


class Vote(db.Model):
    __tablename__ = 'votes'
    query: sql.Select

    id = Column(INTEGER, Sequence("votes_id_seq"), primary_key=True)
    user_id = Column(INTEGER)
    teacher_id = Column(INTEGER)
    results = Column(JSON)

    # {question_id(int) : answer(str), question_id: answer}
    # must be 2 pairs
    # example
    # {13: 'Hello', 14: 'world'}
    open_answers = Column(JSON)


Vote_classes: Vote = {}  # : dict[str, Vote]
for i in faculties:
    Vote_classes[f"{i}"] = (type(f"Vote_{i}", (db.Model,), {"__table_args__": {"schema": f"{i}"} , "__tablename__": "votes",
                                "id": Column(INTEGER, Sequence("votes_id_seq", schema=i), primary_key=True),
                                "user_id": Column(INTEGER),
                                "teacher_id": Column(INTEGER),
                                "results": Column(JSON),
                                "open_answers": Column(JSON)}))


class Group(db.Model):
    __tablename__ = 'groups'
    query: sql.select

    id = Column(INTEGER, Sequence("groups_id_seq"), primary_key=True)
    name = Column(TEXT)
    schedule_id = Column(INTEGER)
    teachers = Column(JSON)


Group_classes = {}  # : dict[str, Group]
for i in faculties:
    Group_classes[f"{i}"] = (type(f"Group_{i}", (db.Model,), {"__table_args__": {"schema": f"{i}"} , "__tablename__": "groups",
                                "id": Column(INTEGER, Sequence("votes_id_seq", schema=i), primary_key=True),
                                "name": Column(TEXT),
                                "schedule_id": Column(TEXT),
                                "teachers": Column(JSON)}))


class Question(db.Model):
    __table_args__ = dict(schema='public')
    __tablename__ = 'questions'
    query: sql.select

    id = Column(INTEGER, Sequence("questions_id_seq"), primary_key=True)
    question_text = Column(TEXT)
    type = Column(TEXT)

