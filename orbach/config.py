from io import StringIO
from configparser import ConfigParser, NoOptionError, NoSectionError


class Config(dict):
    SECTION = "orbach"
    RESERVED_SECTION = "flask"

    def __init__(self, conf):
        """If the conf object sent in has a readline method the configuration will
        be pulled from it as a stream.  If the object is a string, the string will be
        treated as a file to open and read from."""
        self._parser = ConfigParser()

        # Remove ambiguous values
        states = dict(self._parser.BOOLEAN_STATES)
        del states['1']
        del states['0']
        self._parser.BOOLEAN_STATES = states

        self._conf = conf

        if self._is_stream():
            self._parser.read_file(conf)
        else:
            self._parser.read(conf)

        self._section = Config.SECTION

        self._child_sections = {}
        for s in self.other_sections():
            self._child_sections[s] = ConfigSection(self, s)

    def flask_config(self):
        objectified_config = {}
        for k, _ in self._parser.items(self.RESERVED_SECTION):
            objectified_config[k.upper()] = self.objectify_flask_option(k)
        return objectified_config

    def _is_stream(self):
        return hasattr(self._conf, 'readline')

    def __getitem__(self, key):
        if key.upper() != key:
            return self._parser.get(self._section, key)
        else:
            raise NoOptionError("Upper case options can only be retrieved via flask_config()", self._section)

    def __setitem__(self, key, value):
        persist = not key in self
        if key.upper() != key:
            self._parser.set(self._section, key, str(value))
        else:
            raise NoOptionError("Upper case options are immutable", self._section)

        if persist:
            self._persist()

    def __delitem__(self, key):
        if key.upper() != key:
            self._parser.remove_option(self._section, key)
        else:
            raise NoOptionError("Upper case options are immutable", self._section)
        self._persist()

    def __contains__(self, key):
        if key.upper() != key:
            return self._parser.has_option(self._section, key)
        else:
            return False

    def has_section(self, name):
        return name in self._child_sections

    def get_section(self, name):
        try:
            return self._child_sections[name]
        except KeyError:
            raise NoSectionError("No section '%s'" % name)

    def set_section(self, key, value):
        persist = not key in self._child_sections
        self._child_sections[key] = value
        if persist:
            self._persist()

    def delete_section(self, key):
        del self._child_sections[key]
        self._parser.remove_section(key)
        self._persist()

    def other_sections(self):
        s = self._parser.sections()
        if self._section in s:
            s.remove(self._section)
            if self.has_section(self.RESERVED_SECTION):
                s.remove(self.RESERVED_SECTION)
        return s

    def __iter__(self):
        items = self._parser.items(self._section)
        if self.has_section(self.RESERVED_SECTION):
            items += self._parser.items(self.RESERVED_SECTION)
        return iter(items)

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

    def objectify_flask_option(self, key):
        v = self._parser.get(self.RESERVED_SECTION, key)
        try:
            v = self._parser.getboolean(self.RESERVED_SECTION, key)
        except ValueError:
            pass

        try:
            v = self._parser.getint(self.RESERVED_SECTION, key)
        except ValueError:
            pass

        return v

    def __str__(self):
        out = StringIO()
        self._parser.write(out)
        return out.getvalue()


class ConfigSection(Config):
    def __init__(self, parent, section):
        self._section = section
        self._parent = parent
        self._parser = self._parent._parser
        self._conf = self._parent._conf

    def __iter__(self):
        return self._parser.items(self._section)

    def __getitem__(self, key):
        return self._parser.get(self._section, key)

    def __setitem__(self, key, value):
        persist = not key in self
        self._parser.set(self._section, key, value)
        if persist:
            self._persist()

    def __delitem__(self, key):
        self._parser.remove_option(self._section, key)
        self._persist()

    def __contains__(self, key):
        return self._parser.has_option(self._section, key)
