from __future__ import print_function, division, absolute_import

import logging

from ConfigParser import SafeConfigParser, NoOptionError
from itertools import imap

from orbach.util import unicode_in, unicode_out, to_unicode


class Config(object):
    SECTION = "orbach"

    def __init__(self, conf_file):
        self.conf_file = conf_file
        self.parser = SafeConfigParser()
        self.parser.read(self.conf_file)
        for s in self.parser.sections():
            for k, v in self.parser.items(s):
                self.parser.set(s, to_unicode(k), to_unicode(v))

    def __persist(self):
        try:
            with open(self.conf_file, 'w') as f:
                self.parser.write(f)
        except Exception:
            logging.exception("Unable to open %s" % self.conf_file)

    def __len__(self):
        return len(self.parser.items(self.SECTION))

    @unicode_out
    def __getitem__(self, key):
        try:
            return self.parser.get(self.SECTION, key)
        except NoOptionError as e:
            logging.exception(e)
            raise KeyError(e)

    @unicode_in
    def __setitem__(self, key, value):
        self.parser.set(self.SECTION, key, value)
        self.__persist()

    def __delitem__(self, key):
        self.parser.remove_option(self.SECTION, key)
        self.__persist()

    @unicode_in
    def __contains__(self, item):
        return self.parser.has_option(self.SECTION, item)

    def __iter__(self):
        return imap(
            lambda x: (to_unicode(x[0]), to_unicode(x[1])),
            self.parser.items(self.SECTION))
