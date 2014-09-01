#! /usr/bin/env python

from __future__ import print_function, division, absolute_import


def main(app):
    app.run(port=8080)

if __name__ == "__main__":
    # Do development app configuration here

    from orbach import app
    main(app)
