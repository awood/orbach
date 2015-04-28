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
