from __future__ import print_function, division, absolute_import
from orbach.admin import admin


@admin.route('/')
def hello():
    return "Hello"
