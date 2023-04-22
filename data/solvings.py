import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase

class Solvings(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'solvings'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    problem_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("problems.id"))
    student_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    is_solved = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    code = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    solved_tests = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    problem = orm.relationship('Problems')
    student = orm.relationship('User')