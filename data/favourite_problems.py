import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase

class FavouriteProblems(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'favourite_problems'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    problem_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("problems.id"))
    student_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    problem = orm.relationship('Problems')
    student = orm.relationship('User')