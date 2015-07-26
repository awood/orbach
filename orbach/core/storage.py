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
import os

from django.core.files.storage import FileSystemStorage

ARCHIVES = tuple(['.%s' % x for x in 'gz bz2 zip tar tgz txz 7z'.split()])
IMAGES = tuple(['.%s' % x for x in 'jpg jpe jpeg png gif svg bmp'.split()])

log = logging.getLogger(__name__)


class HashDistributedStorage(FileSystemStorage):
    def _lower_ext(self, name):
        basename, ext = os.path.splitext(name)
        return "".join([basename, ext.lower()])

    def _validate(self, name):
        _basename, ext = os.path.splitext(name)
        allowed = ext.lower() in ARCHIVES + IMAGES

        if not allowed:
            raise IOError("Files with extension %s are not allowed" % ext)

    def _save(self, name, content):
        self._validate(name)
        name = self._lower_ext(name)
        name = os.path.normpath(os.path.join(self._hash_dir(content), name))
        return super()._save(name, content)

    def _hash_dir(self, content):
        hasher = hashlib.sha256()

        for chunk in content.chunks():
            hasher.update(chunk)

        return hasher.hexdigest()[:3]
