import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase
import datetime

class Problems(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'problems'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    input_description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    output_description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    difficult = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    rating = sqlalchemy.Column(sqlalchemy.Integer, default=100)
    time_needed = sqlalchemy.Column(sqlalchemy.String, default='1 сек')
    memory_needed = sqlalchemy.Column(sqlalchemy.String, default='16 Мб')
    post_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now())
    author = orm.relationship('User')
    students_that_solved = orm.relationship('SolvedProblems', back_populates='problem')
    students_that_liked = orm.relationship('FavouriteProblems', back_populates='problem')
    tests = orm.relationship('Test', back_populates='problem')
    examples = orm.relationship('Example', back_populates='problem')