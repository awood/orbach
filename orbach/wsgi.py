from __future__ import print_function, division, absolute_import

import orbach

"""Entry point for Twisted, Gunicorn, etc.  Standalone WSGI containers just want
a pointer to something they can import."""

app = orbach.init_from_file(None)
