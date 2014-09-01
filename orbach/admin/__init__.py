from __future__ import print_function, division, absolute_import

from flask import Blueprint

admin = Blueprint('admin', __name__)

from orbach.admin import views
