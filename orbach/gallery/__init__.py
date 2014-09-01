from __future__ import print_function, division, absolute_import

from flask import Blueprint

gallery = Blueprint('gallery', __name__, template_folder="templates")

from orbach.gallery import views
