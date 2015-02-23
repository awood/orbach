from __future__ import print_function, division, absolute_import

import pprint

from ConfigParser import SafeConfigParser
from flask import Flask

from orbach.errors import OrbachError
from orbach.util import unicode_in, unicode_out

FLASK_RESERVED = Flask.default_config.keys() + [
        'SQLALCHEMY_DATABASE_URI',
        'SQLALCHEMY_BINDS',
        'SQLALCHEMY_NATIVE_UNICODE',
        'SQLALCHEMY_ECHO',
        'SQLALCHEMY_RECORD_QUERIES',
        'SQLALCHEMY_POOL_SIZE',
        'SQLALCHEMY_POOL_TIMEOUT',
        'SQLALCHEMY_POOL_RECYCLE',
        'SQLALCHEMY_MAX_OVERFLOW',
        'SQLALCHEMY_COMMIT_ON_TEARDOWN',
]


class MissingSectionError(OrbachError):
    """Raised when no _section matches a requested option."""

    def __init__(self, section):
        OrbachError.__init__(self, 'No section: %r' % (section,))
        self._section = section
        self.args = (section, )


class MissingOptionError(OrbachError):
    """Raised when no _section matches a requested option."""

    def __init__(self, option):
        OrbachError.__init__(self, 'No option: %r' % (option,))
        self._section = option
        self.args = (option, )


class Config(object):
    SECTION = u"orbach"

    def __init__(self, conf):
        """If the conf object send in has a readline method the configuration will
        be pull from it as a stream.  If the object is a string, the string will be
        treated as a file to open and read from."""
        self._parser = SafeConfigParser()

        self._conf = conf

        if self._is_stream():
            self._parser.readfp(conf)
        else:
            self._parser.read(conf)

        self._section = Config.SECTION
        self._child_sections = {}
        for s in self.other_sections():
            self[s] = ConfigSection(self, s)

        self.__setattrs()

    def _is_stream(self):
        return hasattr(self._conf, 'readline')

    @unicode_in
    def __setattr__(self, name, value):
        # If they are setting the attribute in lowercase.
        # E.g. self.debug will throw an error but self.DEBUG will not
        if name.upper() in FLASK_RESERVED and name not in FLASK_RESERVED:
            raise AttributeError("Cannot set %s.  Maybe you meant %s?" % (name, name.upper()))
        if not name.startswith("_"):
            self._parser.set(self._section, name, str(value))
            self._persist()
        super(Config, self).__setattr__(name, value)

    def __setattrs(self):
        # TODO need to validate keys are valid python identifiers.  E.g. nothing
        # staring with a number or symbol.
        for k in self._parser.options(self._section):
            if k.upper() in FLASK_RESERVED:
                k = k.upper()
            setattr(self, k, self._parser.get(self._section, k))

    @unicode_out
    def __getattr__(self, name):
        """Called when accessing nonexistent attributes"""
        # By default, ConfigParser is agnostic about case, but we want to be picky when
        # dealing with Flask reserved configuration options.
        if name.startswith("_"):
            raise AttributeError("Missing attribute %s" % name)
        if self._parser.has_option(self._section, name) and name.upper() not in FLASK_RESERVED:
            return self._parser.get(self._section, name)
        else:
            raise MissingOptionError(name)

    def __delattr__(self, name):
        if self._parser.has_option(self._section, name):
            self._parser.remove_option(self._section, name)
            self._persist()
        super(Config, self).__delattr__(name)

    def __len__(self):
        return len(self._child_sections)

    def __getitem__(self, key):
        try:
            return self._child_sections[key]
        except KeyError:
            raise MissingSectionError(key)

    @unicode_in
    def __setitem__(self, key, value):
        self._child_sections[key] = value

    def __delitem__(self, key):
        del self._child_sections[key]
        self._parser.remove_section(key)
        self._persist()

    @unicode_in
    def __contains__(self, item):
        return item in self._child_sections.keys()

    def other_sections(self):
        s = self._parser.sections()
        if self._section in s:
            s.remove(self._section)
        return s

    def __iter__(self):
        return self._child_sections.iteritems()

    def _persist(self):
        if not self._is_stream():
            try:
                with open(self._conf, 'w') as f:
                    self._parser.write(f)
            except:
                raise IOError("Unable to open %s" % self._conf)

    def get_boolean(self, item):
        return self._parser.getboolean(self._section, item)

    def get_int(self, item):
        return self._parser.getint(self._section, item)

    def to_boolean(self, *args):
        for option in args:
            setattr(self, option, self.get_boolean(option))

    def to_int(self, *args):
        for option in args:
            setattr(self, option, self.get_int(option))

    def __repr__(self):
        return pprint.pformat(self.__dict__)

    def __str__(self):
        settings = filter(lambda t: not t[0].startswith('_'), self.__dict__.iteritems())
        return pprint.pformat(dict(settings))


class ConfigSection(Config):
    def __init__(self, parent, section):
        self._section = section
        self._parent = parent
        self._parser = self._parent._parser
        self._conf = self._parent._conf
        self.__setattrs()

    def __setattrs(self):
        for k in self._parser.options(self._section):
            setattr(self, k, self._parser.get(self._section, k))
