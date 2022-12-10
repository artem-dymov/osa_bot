from gino import Gino
from database import db
from sqlalchemy import sql, Column, Sequence, INTEGER, TEXT, ARRAY, BIGINT


faculties = ('FBME', 'IPT')
faculties_ukr = ('ФБМІ', 'ФТІ')





class User(db.Model):
    __table_args__ = dict(schema='public')
    __tablename__ = 'users'
    query: sql.Select

    id = Column(INTEGER, Sequence("users_id_seq"), primary_key=True)
    tg_id = Column(BIGINT)
    username = Column(TEXT)
    faculty = Column(TEXT)
    group = Column(TEXT)


class Teacher(db.Model):
    __tablename__ = 'teachers'
    query: sql.Select

    id = Column(INTEGER, Sequence("teachers_id_seq"), primary_key=True)
    full_name = Column(TEXT)
    type = Column(TEXT)
    groups = Column(ARRAY(TEXT))



Teacher_classes: Teacher = {}  # : dict[str, Teacher]
for i in faculties:
    Teacher_classes[f"{i}"] = (type(f"Teacher_{i}", (db.Model,), {"__table_args__" : {"schema" : f"{i}"} , "__tablename__": "teachers",
                                "id": Column(INTEGER, Sequence("teachers_id_seq", schema=i), primary_key=True),
                                "full_name": Column(TEXT),
                                "type": Column(TEXT),
                                "groups": Column(ARRAY(TEXT))}))


class Vote(db.Model):
    __tablename__ = 'votes'
    query: sql.Select

    id = Column(INTEGER, Sequence("votes_id_seq"), primary_key=True)
    user_id = Column(INTEGER)
    teacher_id = Column(INTEGER)
    marks = Column(ARRAY(INTEGER))
    questions_id = Column(ARRAY(INTEGER))


Vote_classes: Vote = {}  # : dict[str, Vote]
for i in faculties:
    Vote_classes[f"{i}"] = (type(f"Vote_{i}", (db.Model,), {"__table_args__": {"schema": f"{i}"} , "__tablename__": "votes",
                                "id": Column(INTEGER, Sequence("votes_id_seq", schema=i), primary_key=True),
                                "user_id": Column(INTEGER),
                                "teacher_id": Column(INTEGER),
                                "marks": Column(ARRAY(INTEGER)),
                                "questions_id": Column(ARRAY(INTEGER))}))

