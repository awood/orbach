from __future__ import print_function, division, absolute_import

import os
import sys
import tempfile

from io import StringIO
from contextlib import contextmanager
from mock import mock_open, patch
from orbach.util import unicode_in, unicode_out


@contextmanager
@unicode_in
def temp_file(content, *args, **kwargs):
    try:
        kwargs['delete'] = False
        kwargs.setdefault('prefix', 'orbach')
        fn = tempfile.NamedTemporaryFile(*args, **kwargs)
        fn.write(content)
        fn.close()
        yield fn.name
    finally:
        os.unlink(fn.name)


@contextmanager
@unicode_in
def open_mock(content, **kwargs):
    m = mock_open(read_data=content)
    with patch('__builtin__.open', m, create=True, **kwargs) as m:
        yield m


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

        @unicode_in
        def write(self, data):
            self.buf.write(data)
            if not self.silent:
                self.stream.write(data)

        @unicode_out
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
