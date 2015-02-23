from __future__ import print_function, division, absolute_import

from flask.ext.sqlalchemy import Model

from sqlalchemy import Column, Integer, DateTime, Unicode, String
from sqlalchemy import func

from orbach import DbMeta


class StandardAttributes():
    id = Column(Integer, primary_key=True)
    created = Column(DateTime, server_default=func.now())
    modified = Column(DateTime, server_default=func.now(), server_onupdate=func.now())


class User(Model, StandardAttributes):
    __metaclass__ = DbMeta
    __tablename__ = "users"

    username = Column(Unicode)
    password = Column(String)
