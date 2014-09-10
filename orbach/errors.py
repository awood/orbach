from __future__ import print_function, division, absolute_import


# General exception classes
class OrbachError(Exception):
    """Base class for exceptions."""

    def __init__(self, msg=''):
        self.message = msg
        Exception.__init__(self, msg)

    def __repr__(self):
        return self.message

    __str__ = __repr__
