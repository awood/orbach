from flask import Blueprint
from flask.ext.restful import Api

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint, prefix="/api/v1", catch_all_404s=True)

# Flask requires that all view functions be imported in the __init__.py but
# this unfortunately causes Flake8 to complain about unused imports so we tag
# this line NOQA
from orbach.api import v1  # NOQA
