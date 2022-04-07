import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class Posts(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'posts'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    creator = sqlalchemy.Column(
        sqlalchemy.String, sqlalchemy.ForeignKey("users.username"))
    title = sqlalchemy.Column(sqlalchemy.String(100),
                              nullable=True, unique=True)
    intro = sqlalchemy.Column(sqlalchemy.String(140), nullable=True)
    text = sqlalchemy.Column(sqlalchemy.Text(800), nullable=True)
    start_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                   default=datetime.datetime.now)
    user = orm.relation('User')
