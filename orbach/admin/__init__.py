from __future__ import print_function, division, absolute_import

from flask import Blueprint

admin = Blueprint('admin', __name__, template_folder="templates")

# Flask requires that all view functions be imported in the __init__.py but
# this unfortunately causes Flake8 to complain about unused imports so we tag
# this line NOQA
from orbach.admin import views  # NOQA
