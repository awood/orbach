from __future__ import print_function, division, absolute_import

import abc
import logging
import pprint

from ConfigParser import SafeConfigParser, NoOptionError
from itertools import imap

from orbach.util import unicode_in, unicode_out, to_unicode
from orbach.errors import OrbachError


class MissingSectionError(OrbachError):
    """Raised when no section matches a requested option."""

    def __init__(self, section):
        OrbachError.__init__(self, 'No section: %r' % (section,))
        self.section = section
        self.args = (section, )


class ConfigBase(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def section(self):
        return

    @abc.abstractproperty
    def parser(self):
        return

    def __len__(self):
        return len(self.parser.items(self.section))

    @unicode_out
    def __getitem__(self, key):
        try:
            return self.parser.get(self.section, key)
        except NoOptionError as e:
            logging.exception(e)
            raise KeyError(e)

    @unicode_in
    def __setitem__(self, key, value):
        self.parser.set(self.section, key, value)

    def __delitem__(self, key):
        self.parser.remove_option(self.section, key)

    @unicode_in
    def __contains__(self, item):
        return self.parser.has_option(self.section, item)

    def __iter__(self):
        return imap(
            lambda x: (to_unicode(x[0]), to_unicode(x[1])),
            self.parser.items(self.section))

    def getboolean(self, item):
        return self.parser.getboolean(self.section, item)

    def getint(self, item):
        return self.parser.getint(self.section, item)

    def __repr__(self):
        return pprint.pformat(dict((x for x in self)))

    __str__ = __repr__


class Config(ConfigBase):
    SECTION = "orbach"

    def __init__(self, conf_file):
        super(Config, self).__init__()
        self._parser = SafeConfigParser()

        self.conf_file = conf_file
        self.parser.read(self.conf_file)
        for s in self.other_sections():
            for k, v in self.parser.items(s):
                self.parser.set(s, to_unicode(k), to_unicode(v))
            setattr(self, s, ConfigSection(self, s))

    def __getattr__(self, attr):
        raise MissingSectionError(attr)

    @property
    def section(self):
        return self.SECTION

    def other_sections(self):
        s = self.parser.sections()
        if self.section in s:
            s.remove(self.section)
        return s

    @property
    def parser(self):
        return self._parser

    @parser.setter
    def parser(self, value):
        self._parser = value

    def _persist(self):
        try:
            with open(self.conf_file, 'w') as f:
                self.parser.write(f)
        except Exception:
            logging.exception("Unable to open %s" % self.conf_file)

    def __setitem__(self, key, value):
        super(Config, self).__setitem__(key, value)
        self._persist()

    def __delitem__(self, key):
        super(Config, self).__delitem__(key)
        self._persist()

    def __str__(self):
        dict_repr = super(Config, self).__str__()
        for s in self.other_sections():
            dict_repr += " %s: %s" % (s, str(getattr(self, s)))
        return dict_repr


class ConfigSection(ConfigBase):
    def __init__(self, parent, section):
        super(ConfigSection, self).__init__()
        self._section = section
        self.parent = parent

    @property
    def parser(self):
        return self.parent.parser

    @property
    def section(self):
        return self._section

    def __setitem__(self, key, value):
        super(ConfigSection, self).__setitem__(key, value)
        self.parent._persist()

    def __delitem__(self, key):
        super(ConfigSection, self).__delitem__(key)
        self.parent._persist()
