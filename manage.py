#! /usr/bin/env python

from __future__ import print_function, division, absolute_import

from logging import StreamHandler, Formatter, getLogger
import logging

from flask.ext.script import Manager, Server, Shell
from flask.ext.assets import ManageAssets


if __name__ == "__main__":
    # Do development app configuration here
    from orbach import app

    formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stderr = StreamHandler()
    stderr.setFormatter(formatter)
    stderr.setLevel(logging.DEBUG)

    loggers = [app.logger, getLogger('scss'), getLogger('webassets')]
    for l in loggers:
        l.addHandler(stderr)

    manager = Manager(app, with_default_commands=False)
    manager.add_command("run", Server(port="8081"))
    manager.add_command("assets", ManageAssets())
    manager.add_command("shell", Shell())
    manager.run(default_command="run")
