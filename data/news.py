import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class News(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'news'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    creator = sqlalchemy.Column(
        sqlalchemy.String, sqlalchemy.ForeignKey("users.username"))
    title = sqlalchemy.Column(sqlalchemy.String(30),
                              nullable=True, unique=True)
    intro = sqlalchemy.Column(sqlalchemy.String(50), nullable=False)
    text = sqlalchemy.Column(sqlalchemy.Text(800), nullable=False)
    create_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                   default=datetime.datetime.now)
    image = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    user = orm.relation('User')
