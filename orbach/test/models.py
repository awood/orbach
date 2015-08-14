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

from orbach.core.fields import ThumbnailImageField
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


class DummyThumbnailModel(models.Model):
    file = ThumbnailImageField(max_length=150)


@receiver(pre_delete, sender=DummyThumbnailModel)
def imagefile_delete(sender, instance, **kwargs):
    # Set save to False to instance doesn't try to save the object
    instance.file.delete(save=False)


class DummyThumbnailNoSignalModel(models.Model):
    file = ThumbnailImageField(max_length=150)
