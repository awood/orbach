from __future__ import print_function, division, absolute_import

from flask import Blueprint

admin = Blueprint('admin', __name__, template_folder="templates")

from orbach.admin import views
