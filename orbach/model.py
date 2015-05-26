from flask.ext.sqlalchemy import Model

from sqlalchemy import Column, Integer, DateTime, Unicode, String, ForeignKey, \
    func
from sqlalchemy.orm import relationship

from orbach import DbMeta


class StandardAttributes(object):
    id = Column(Integer, primary_key=True)
    created = Column(DateTime, server_default=func.now())
    modified = Column(DateTime, server_default=func.now(), server_onupdate=func.now())


class User(Model, StandardAttributes, metaclass=DbMeta):
    __tablename__ = "users"

    username = Column(Unicode)
    password = Column(String)

    def to_json(self):
        return {
            "username": self.username,
        }


class Role(Model, StandardAttributes, metaclass=DbMeta):
    __tablename__ = "roles"


class Gallery(Model, StandardAttributes, metaclass=DbMeta):
    __tablename__ = "galleries"

    name = Column(Unicode)
    description = Column(Unicode)
    parent = Column(Integer)
    properties = relationship("GalleryProperty", backref="gallery")

    def to_json(self):
        return {
            "name": self.name,
            "description": self.description,
            "parent": self.parent,
            "properties": [x.to_json() for x in self.properties],
        }


class GalleryProperty(Model, StandardAttributes, metaclass=DbMeta):
    __tablename__ = "gallery_properties"

    gallery_id = Column(Integer, ForeignKey('galleries.id'))
    property = Column(Unicode)
    value = Column(Unicode)

    def to_json(self):
        return {
            "property": self.property,
            "value": self.value,
        }


class ImageFile(Model, StandardAttributes, metaclass=DbMeta):
    __tablename__ = "image_files"


class Picture(Model, StandardAttributes, metaclass=DbMeta):
    __tablename__ = "pictures"


class Cover(Model, StandardAttributes, metaclass=DbMeta):
    __tablename__ = "covers"
