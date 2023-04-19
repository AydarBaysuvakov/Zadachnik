import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase

class Example(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'examples'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    problem_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("problems.id"))
    input = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    output = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    problem = orm.relationship('Problems')