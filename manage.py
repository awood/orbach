#! /usr/bin/env python

from __future__ import print_function, division, absolute_import

from logging import StreamHandler, Formatter, getLogger
import logging

from flask.ext.script import Manager, Server, Shell
from flask.ext.assets import ManageAssets


def build_orbach(config=None):
    app = orbach.init_from_file(config)
    loggers = [app.logger, getLogger('scss'), getLogger('webassets')]
    for l in loggers:
        l.addHandler(stderr)
    return app


if __name__ == "__main__":
    import orbach


    formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stderr = StreamHandler()
    stderr.setFormatter(formatter)
    stderr.setLevel(logging.DEBUG)

    manager = Manager(build_orbach, with_default_commands=False)
    manager.add_command("run", Server(port="8081"))
    manager.add_option('-c', '--config', dest='config', required=False)

    manager.add_command("assets", ManageAssets())
    manager.add_command("shell", Shell())

    manager.run(default_command="run")
