import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase

class SolvedProblems(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'solved_problems'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    problem_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("problems.id"))
    student_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("students.id"))
    is_solved = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    problem = orm.relationship('Problems')
    student = orm.relationship('Students')