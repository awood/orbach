from flask.ext.babel import _
from werkzeug.exceptions import BadRequest
from werkzeug.http import HTTP_STATUS_CODES


class OrbachError(Exception):
    """Base class for exceptions."""
    @property
    def data(self):
        """Flask-RESTful looks for a dictionary named 'data' on the exception object"""
        return {
            'message': "%s - %s" % (HTTP_STATUS_CODES[self.code], self.description),
        }

    def __repr__(self):
        return self.description

    __str__ = __repr__


class ForbiddenFileExtensionError(OrbachError, BadRequest):
    description = _("{} is not an accepted file extension.")

    def __init__(self, ext):
        super().__init__(self.description.format(ext))
