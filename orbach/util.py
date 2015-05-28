import os

from pathlib import Path

from flask import g, request, current_app

ORBACH_LANGS = ['en', 'fr']


def get_locale():
    # if a user is logged in, use the locale from the user settings
    user = getattr(g, 'user', None)
    if user is not None:
        return user.locale
    # otherwise try to guess the language from the user accept
    # header the browser transmits.
    return request.accept_languages.best_match(current_app.translations)


def get_timezone():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone


def image_dir(config=None):
    if not config:
        config = current_app.config

    root = Path(config.orbach["application_root"])
    return root.joinpath(config.orbach['image_directory'])


def gallery_dir(config=None):
    if not config:
        config = current_app.config

    root = Path(config.orbach["application_root"])
    return root.joinpath(config.orbach['gallery_directory'])


def lowercase_ext(filename):
    unused, ext = os.path.splitext(os.path.basename(filename))
    return ext.lower()
