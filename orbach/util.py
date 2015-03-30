from flask import g, request, current_app

ORBACH_LANGS = ['en', 'fr']


def get_locale():
    # if a user is logged in, use the locale from the user settings
    user = getattr(g, 'user', None)
    if user is not None:
        return user.locale
    # otherwise try to guess the language from the user accept
    # header the browser transmits.
    current_app.logger.debug("Returning %s" % request.accept_languages.best_match(ORBACH_LANGS))
    return request.accept_languages.best_match(ORBACH_LANGS)


def get_timezone():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone
