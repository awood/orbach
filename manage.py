#! /usr/bin/env python

from __future__ import print_function, division, absolute_import

from flask import Config
from flask.ext.script import Manager, Server, Shell
from flask.ext.assets import ManageAssets


class DevelopmentConfig(Config):
    DEBUG = True

    def __init__(self):
        pass


if __name__ == "__main__":
    # Do development app configuration here
    from orbach import app
    app.config.from_object(DevelopmentConfig())
    manager = Manager(app, with_default_commands=False)
    manager.add_command("run", Server(port="8081"))
    manager.add_command("assets", ManageAssets())
    manager.add_command("shell", Shell())
    manager.run(default_command="run")
