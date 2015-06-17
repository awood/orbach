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
import os

from django.core.files.storage import FileSystemStorage
from django.utils._os import safe_join

ARCHIVES = tuple(['.%s' % x for x in 'gz bz2 zip tar tgz txz 7z'.split()])
IMAGES = tuple(['.%s' % x for x in 'jpg jpe jpeg png gif svg bmp'.split()])


class HashDistributedStorage(FileSystemStorage):
    def _lower_ext(self, name):
        basename, ext = os.path.splitext(name)
        return "".join([basename, ext.lower()])

    def _save(self, name, content):
        _basename, ext = os.path.splitext(name)
        allowed = ext.lower() in ARCHIVES + IMAGES

        if not allowed:
            raise IOError("Files with extension %s are not allowed" % ext)

        name = self._lower_ext(name)
        return super()._save(name, content)

    def path(self, name):
        name = self._lower_ext(name)
        hasher = hashlib.sha256(name.encode('utf-8'))
        hash_dir = hasher.hexdigest()[:3]
        return safe_join(self.location, hash_dir, name)
