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
import logging

from pathlib import Path
from urlpath import URL

from django.db.models.fields.files import ImageField, ImageFieldFile

from orbach.core.image_util import ImageUtil

log = logging.getLogger(__name__)


class ThumbnailImageFieldFile(ImageFieldFile):
    def _add_thumb(self, path_item):
        destination_file = "{}_tbn{}".format(path_item.stem, "".join(path_item.suffixes))
        return str(path_item.with_name(destination_file))

    def _get_thumb_path(self):
        return self._add_thumb(Path(self.path))

    thumb_path = property(_get_thumb_path)

    def _get_thumb_url(self):
        return self._add_thumb(URL(self.url))

    thumb_url = property(_get_thumb_url)

    def save(self, name, content, save=True):
        log.info("Saving {}".format(name))
        super().save(name, content, save)
        ImageUtil.create_thumbnail(self.path, self.thumb_path, self.field.thumb_width, self.field.thumb_height)

    def delete(self, save=True):
        log.info("Deleting thumbnail {}".format(self.thumb_path))
        f = Path(self.thumb_path)
        if f.exists():
            f.unlink()
        super().delete(save)


class ThumbnailImageField(ImageField):
    attr_class = ThumbnailImageFieldFile

    def __init__(self, thumb_width=250, thumb_height=250, *args, **kwargs):
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height
        log.debug("Thumb dimensions {} and {}".format(thumb_height, thumb_width))
        super().__init__(*args, **kwargs)
