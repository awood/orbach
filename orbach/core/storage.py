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
import hashlib
import logging

from pathlib import Path

from django.conf import settings
from django.core.files.storage import FileSystemStorage

ARCHIVES = tuple(['.%s' % x for x in 'gz bz2 zip tar tgz txz 7z'.split()])
IMAGES = tuple(['.%s' % x for x in 'jpg jpe jpeg png gif svg bmp'.split()])

log = logging.getLogger(__name__)


class HashDistributedStorage(FileSystemStorage):
    def _validate(self, name):
        allowed = name.suffix.lower() in ARCHIVES + IMAGES

        if not allowed:
            raise IOError("Files with extension %s are not allowed" % name.suffix)

    def _save(self, name, content):
        name = Path(name)
        self._validate(name)
        name = name.with_suffix(name.suffix.lower())
        hashed_dir = Path(self._hash_dir(content))
        dest_name = hashed_dir.joinpath(name)
        return super()._save(str(dest_name), content)

    def _hash_dir(self, content):
        hasher = hashlib.sha256()

        for chunk in content.chunks():
            hasher.update(chunk)

        return hasher.hexdigest()[:3]

    def delete(self, name):
        path = Path(name).resolve()
        super().delete(name)
        parent = path.parent
        is_empty = parent.is_dir() and len(list(parent.iterdir())) == 0
        ok_to_delete = is_empty and Path(settings.ORBACH_ROOT) in list(parent.parents)

        if ok_to_delete:
            parent.rmdir()
