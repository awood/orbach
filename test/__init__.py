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
import os
import sys
import tempfile

from io import StringIO
from contextlib import contextmanager
from unittest.mock import mock_open, patch


@contextmanager
def temp_file(content, *args, **kwargs):
    try:
        kwargs['delete'] = False
        kwargs.setdefault('prefix', 'orbach')
        fn = tempfile.NamedTemporaryFile(*args, **kwargs)
        fn.write(bytes(content, "utf-8"))
        fn.close()
        yield fn.name
    finally:
        os.unlink(fn.name)


@contextmanager
def open_mock(content, **kwargs):
    content_out = StringIO()
    m = mock_open(read_data=content)
    with patch('__main__.open', m, create=True, **kwargs) as mo:
        stream = StringIO(content)
        rv = mo.return_value
        rv.write = lambda x: content_out.write(bytes(x, "utf-8"))
        rv.content_out = lambda: content_out.getvalue()
        rv.__iter__ = lambda x: iter(stream.readlines())
        yield rv


def assert_items_equals(self, a, b):
    """Assert that two lists contain the same items regardless of order."""
    if sorted(a) != sorted(b):
        self.fail("%s != %s" % (a, b))
    return True


# Use as a context manager to intercept stdout and stderr and examine them
class Capture(object):
    class Tee(object):
        def __init__(self, stream, silent):
            self.buf = StringIO()
            self.stream = stream
            self.silent = silent

        def write(self, data):
            self.buf.write(data)
            if not self.silent:
                self.stream.write(bytes(data, "utf-8"))

        def getvalue(self):
            return self.buf.getvalue()

    def __init__(self, silent=False):
        self.silent = silent

    def __enter__(self):
        self.buffs = (self.Tee(sys.stdout, self.silent), self.Tee(sys.stderr, self.silent))
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        sys.stdout, sys.stderr = self.buffs
        return self

    @property
    def out(self):
        return self.buffs[0].getvalue()

    @property
    def err(self):
        return self.buffs[1].getvalue()

    def __exit__(self, exc_type, exc_value, traceback):
        sys.stdout = self.stdout
        sys.stderr = self.stderr
