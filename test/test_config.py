from __future__ import print_function, division, absolute_import

import unittest

from test import temp_file, open_mock
from textwrap import dedent

from ConfigParser import SafeConfigParser

from orbach.config import Config, ConfigSection, MissingSectionError, MissingOptionError


class ConfigTest(unittest.TestCase):
    def setUp(self):
        self.content = dedent("""
            [orbach]
            hello = world
            goodbye = world
        """)

    def test_get_attribute(self):
        with temp_file(self.content) as t:
            conf = Config(t)
            self.assertEquals(conf.hello, 'world')

    def test_get_attribute_unicode(self):
        with temp_file(self.content) as t:
            conf = Config(t)
            self.assertIsInstance(conf.hello, unicode)

    def test_bad_get(self):
        with temp_file(self.content) as t:
            conf = Config(t)
            with self.assertRaises(MissingOptionError):
                conf.does_not_exist

    def test_set(self):
        with temp_file(self.content) as t:
            conf = Config(t)
            conf.foo = 'bar'
            parser = SafeConfigParser()
            parser.read(t)
            self.assertTrue(parser.has_option(Config.SECTION, 'foo'))
            self.assertEquals('bar', conf.foo)

    def test_set_unicode(self):
        with temp_file(self.content) as t:
            conf = Config(t)
            conf.foo = 'bar'
            self.assertIsInstance(conf.foo, unicode)

    def test_getboolean(self):
        boolean_conf = dedent("""
            [orbach]
            x = True
            y = False
            a = on
            b = off
        """)
        with temp_file(boolean_conf) as t:
            conf = Config(t)
            self.assertTrue(conf.getboolean('x'))
            self.assertTrue(conf.getboolean('a'))
            self.assertFalse(conf.getboolean('y'))
            self.assertFalse(conf.getboolean('b'))

    def test_getint(self):
        boolean_conf = dedent("""
            [orbach]
            x = 123
        """)
        with temp_file(boolean_conf) as t:
            conf = Config(t)
            self.assertEquals(123, conf.getint('x'))

    def test_reserved_options(self):
        reserved = dedent("""
            [orbach]
            DEBUG = True
            USE_X_SENDFILE = True
        """)
        with temp_file(reserved) as t:
            conf = Config(t)
            self.assertEquals("True", conf.DEBUG)
            with self.assertRaises(MissingOptionError):
                conf.debug

            self.assertEquals("True", conf.USE_X_SENDFILE)
            with self.assertRaises(AttributeError):
                conf.use_x_sendfile = "False"

    def test_read_stream(self):
        stream = dedent(u"""
            [orbach]
            foo = baz
        """)
        with open_mock(stream) as m:
            conf = Config(m)
            self.assertEquals("baz", conf.foo)


class ConfigWithSectionsTest(unittest.TestCase):
    def setUp(self):
        self.content = dedent("""
            [orbach]
            hello = world
            goodbye = world

            [other]
            foo = bar
            baz = qux
        """)

    def test_del(self):
        with temp_file(self.content) as t:
            conf = Config(t)
            del(conf['other'])
            parser = SafeConfigParser()
            parser.read(t)
            self.assertFalse(parser.has_section('other'))
            with self.assertRaises(MissingSectionError):
                conf['other']

    def test_contains(self):
        with temp_file(self.content) as t:
            conf = Config(t)
            self.assertTrue('other' in conf)
            self.assertFalse('xyz' in conf)

    def test_len(self):
        with temp_file(self.content) as t:
            conf = Config(t)
            self.assertEquals(1, len(conf))

    def test_section_access(self):
        with temp_file(self.content) as t:
            conf = Config(t)
            self.assertEquals('bar', conf['other'].foo)
            self.assertEquals('qux', conf['other'].baz)

    def test_iter(self):
        with temp_file(self.content) as t:
            conf = Config(t)
            for k, v in conf:
                self.assertTrue(isinstance(k, unicode))
                self.assertTrue(isinstance(v, ConfigSection))

    def test_del_from_section(self):
        with temp_file(self.content) as t:
            conf = Config(t)
            del(conf['other'].foo)
            parser = SafeConfigParser()
            parser.read(t)
            self.assertFalse(parser.has_option('other', 'foo'))
            with self.assertRaises(MissingOptionError):
                conf['other'].foo

    def test_set_to_section(self):
        with temp_file(self.content) as t:
            conf = Config(t)
            conf['other'].abc = 'xyz'
            parser = SafeConfigParser()
            parser.read(t)
            self.assertTrue(parser.has_option('other', 'abc'))
            self.assertEquals('xyz', conf['other'].abc)

    def test_other_sections(self):
        with temp_file(self.content) as t:
            conf = Config(t)
            self.assertFalse(Config.SECTION in conf.other_sections())
            self.assertEquals(['other'], conf.other_sections())

    def test_missing_section(self):
        with temp_file(self.content) as t:
            conf = Config(t)
            with self.assertRaises(MissingSectionError):
                conf['missing']
