#! /usr/bin/env python

from __future__ import print_function, division, absolute_import

from logging import getLogger

from flask.ext.script import Manager, Server, Shell
from flask.ext.assets import ManageAssets


def build_orbach(config=None):
    app = orbach.init_from_file(config)

    loggers = [getLogger('scss'), getLogger('webassets')]
    for l in loggers:
        map(lambda x: l.addHandler(x), app.logger.handlers)

    return app


if __name__ == "__main__":
    import orbach

    manager = Manager(build_orbach, with_default_commands=False)
    manager.add_command("run", Server(port="8081"))
    manager.add_option('-c', '--config', dest='config', required=False, default="test.conf")

    manager.add_command("assets", ManageAssets())
    manager.add_command("shell", Shell())

    manager.run(default_command="run")
