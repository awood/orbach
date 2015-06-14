'''
Copyright 2015

This file is part of Orbach.

Orbach is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Orbach is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Orbach.  If not, see <http://www.gnu.org/licenses/>.
'''
from django.db import models
from django.contrib.auth.models import User

from orbach.core.util import image_dir
from orbach.core.storage import HashDistributedStorage


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ImageFile(BaseModel):
    file = models.ImageField(max_length=150, upload_to=image_dir, storage=HashDistributedStorage,
         height_field="height", width_field="width")
    owner = models.ForeignKey(User)

    class Meta:
        db_table = "ob_image_files"


class Gallery(BaseModel):
    name = models.CharField(max_length=175)
    owner = models.ForeignKey(User)
    description = models.TextField(max_length=300)
    parent = models.ForeignKey('self')

    class Meta:
        db_table = "ob_galleries"
        verbose_name_plural = "galleries"


class Picture(BaseModel):
    caption = models.TextField(max_length=250)
    title = models.TextField(max_length=50)
    image = models.ForeignKey(ImageFile)
    gallery = models.ForeignKey(Gallery)

    class Meta:
        db_table = "ob_pictures"
        unique_together = ('id', 'gallery')


class Cover(BaseModel):
    gallery = models.ForeignKey(Gallery)
    picture = models.ForeignKey(Picture)

    class Meta:
        db_table = "ob_covers"
        unique_together = ('gallery', 'picture')
