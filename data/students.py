import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase

class Students(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'students'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User')
    solved_problems = orm.relationship('SolvedProblems', back_populates='student')
    favourite_problems = orm.relationship('FavouriteProblems', back_populates='student')
    favourite_authors = orm.relationship('FavouriteAuthors', back_populates='student')