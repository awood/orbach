from flask.ext.babel import _


# General exception classes
class OrbachError(Exception):
    """Base class for exceptions."""

    def __init__(self, msg=''):
        self.message = msg
        Exception.__init__(self, msg)

    def __repr__(self):
        return self.message

    __str__ = __repr__


class ForbiddenFileExtensionError(OrbachError):
    def __init__(self, filename):
        msg = _("%s is not an allowed file extension.")
        super().__init__(msg)
