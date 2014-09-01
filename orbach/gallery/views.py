from __future__ import print_function, division, absolute_import
from orbach.gallery import gallery


@gallery.route('/')
def hello():
    return "Hello"
