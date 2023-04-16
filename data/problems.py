import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase

class Problems(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'problems'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("authors.id"))
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    input_description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    output_description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    dificult = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    rating = sqlalchemy.Column(sqlalchemy.Integer, default=100)
    author = orm.relationship('Author')
    students_that_solved = orm.relationship('SolvedProblems', back_populates='problem')
    students_that_liked = orm.relationship('FavouriteProblems', back_populates='problem')
    tests = orm.relationship('Tests', back_populates='problem')
    examples = orm.relationship('Examples', back_populates='problem')