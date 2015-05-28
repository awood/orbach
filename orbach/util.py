import hashlib
import os

from contextlib import contextmanager
from pathlib import Path

from flask import g, request, current_app


def hash_stream(fh):
    h = hashlib.sha256()
    h.update(fh.read())
    # Return to the beginning so the stream can be used again
    fh.seek(0)
    return h.hexdigest()


@contextmanager
def hash_file(filename):
    try:
        fh = open(filename, 'rb')
        yield hash_stream(fh)
    finally:
        fh.close()


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
    return ext.lower().lstrip('.')


def resolve_path_conflict(filename):
    """Expects a pathlib.Path object."""
    count = 0
    while True:
        count = count + 1
        name, unused1, unused2 = filename.stem.partition('.')
        newname = '{}_{:02d}{}'.format(name, count, ''.join(filename.suffixes))
        if not filename.with_name(newname).exists():
            return filename.with_name(newname)
