from __future__ import print_function, division, absolute_import

import logging

from logging.handlers import RotatingFileHandler


class OrbachLog(object):
    @staticmethod
    def setup(app):
        handler = RotatingFileHandler('orbach.log', maxBytes=10000, backupCount=2)
        if app.debug:
            handler.setLevel(logging.DEBUG)
        else:
            handler.setLevel(logging.INFO)
        app.logger.addHandler(handler)
