from flask.ext.sqlalchemy import Model

from sqlalchemy import Column, Integer, DateTime, Unicode, String
from sqlalchemy import func

from orbach import DbMeta


class StandardAttributes():
    id = Column(Integer, primary_key=True)
    created = Column(DateTime, server_default=func.now())
    modified = Column(DateTime, server_default=func.now(), server_onupdate=func.now())


class User(Model, StandardAttributes, metaclass=DbMeta):
    __tablename__ = "users"

    username = Column(Unicode)
    password = Column(String)


class Role(Model, StandardAttributes, metaclass=DbMeta):
    __tablename__ = "roles"


class Gallery(Model, StandardAttributes, metaclass=DbMeta):
    __tablename__ = "galleries"


class ImageFile(Model, StandardAttributes, metaclass=DbMeta):
    __tablename__ = "image_files"


class Picture(Model, StandardAttributes, metaclass=DbMeta):
    __tablename__ = "pictures"


class Cover(Model, StandardAttributes, metaclass=DbMeta):
    __tablename__ = "covers"
