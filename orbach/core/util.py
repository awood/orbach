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

from contextlib import contextmanager

from django.conf import settings
from django.http import HttpResponse


def hash_stream(fh):
    h = hashlib.sha256()
    h.update(fh.read())
    # Return to the beginning so the stream can be used again
    fh.seek(0)
    return h.hexdigest()


@contextmanager
def hash_file(filename):
    try:
        fh = open(filename, 'rb')
        yield hash_stream(fh)
    finally:
        fh.close()


def image_dir(instance, filename):
    return os.path.join(
        settings.ORBACH_ROOT,
        settings.ORBACH['image_directory'],
    )


def gallery_dir():
    return os.path.join(
        settings.ORBACH_ROOT,
        settings.ORBACH['gallery_directory'],
    )


class HttpResponseUnauthorized(HttpResponse):
    status_code = 401
