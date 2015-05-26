from flask.ext.sqlalchemy import Model

from sqlalchemy import Column, Integer, DateTime, Unicode, String, ForeignKey, \
    func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.collections import attribute_mapped_collection

from orbach import DbMeta


class StandardAttributes(object):
    id = Column(Integer, primary_key=True)
    created = Column(DateTime, server_default=func.now())
    modified = Column(DateTime, server_default=func.now(), server_onupdate=func.now())


class User(Model, StandardAttributes, metaclass=DbMeta):
    __tablename__ = "users"

    username = Column(Unicode)
    password = Column(String)
    image_files = relationship("ImageFile", backref="owner", lazy="dynamic")
    galleries = relationship("Gallery", backref="owner", lazy="dynamic")

    def to_json(self):
        return {
            "username": self.username,
        }


class Role(Model, StandardAttributes, metaclass=DbMeta):
    __tablename__ = "roles"


class Gallery(Model, StandardAttributes, metaclass=DbMeta):
    __tablename__ = "galleries"

    # Need this explicitly here since we reference it early on in remote_side
    id = Column(Integer, primary_key=True)

    name = Column(Unicode)
    description = Column(Unicode)
    owner_id = Column(Integer, ForeignKey("users.id"))
    parent_id = Column(Integer, ForeignKey("galleries.id"))

    # See http://docs.sqlalchemy.org/en/latest/orm/self_referential.html#self-referential
    children = relationship("Gallery", backref=backref('parent', remote_side=[id]))
    properties = relationship("GalleryProperty", backref="gallery",
        collection_class=attribute_mapped_collection('property'))
    pictures = relationship("Picture", backref="gallery")

    def to_json(self):
        return {
            "name": self.name,
            "description": self.description,
            "parent_id": self.parent,
            "properties": [x.to_json() for x in self.properties],
        }


class GalleryProperty(Model, StandardAttributes, metaclass=DbMeta):
    __tablename__ = "gallery_properties"

    gallery_id = Column(Integer, ForeignKey('galleries.id'))
    property = Column(Unicode)
    value = Column(Unicode)

    def __init__(self, property_name, value):
        self.property = property_name
        self.value = value

    def to_json(self):
        return {
            "property": self.property,
            "value": self.value,
        }


class ImageFile(Model, StandardAttributes, metaclass=DbMeta):
    __tablename__ = "image_files"

    file = Column(Unicode)
    owner_id = Column(Integer, ForeignKey("users.id"))
    pictures = relationship("Picture", backref="image_file", lazy="dynamic")

    def to_json(self):
        return {
            'file': self.file,
            'owner': self.owner.to_json(),
        }


class Picture(Model, StandardAttributes, metaclass=DbMeta):
    __tablename__ = "pictures"

    title = Column(Unicode)
    caption = Column(Unicode)
    image_file_id = Column(Integer, ForeignKey("image_files.id"))
    gallery_id = Column(Integer, ForeignKey("galleries.id"))

    def to_json(self):
        return {
            "title": self.title,
            "caption": self.caption,
            "image_file": self.image_file.to_json(),
        }


class Cover(Model, StandardAttributes, metaclass=DbMeta):
    __tablename__ = "covers"
