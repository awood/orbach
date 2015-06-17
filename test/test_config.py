import unittest

from test import temp_file, open_mock
from textwrap import dedent

from configparser import ConfigParser, NoOptionError, NoSectionError

from orbach.config import Config


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
            self.assertEqual(conf['hello'], 'world')

    def test_bad_get(self):
        with temp_file(self.content) as t:
            conf = Config(t)
            with self.assertRaises(NoOptionError):
                conf['blah']

    def test_set(self):
        with temp_file(self.content) as t:
            conf = Config(t)
            conf['foo'] = 'bar'
            parser = ConfigParser()
            parser.read(t)
            self.assertTrue(parser.has_option(Config.SECTION, 'foo'))
            self.assertEqual('bar', conf['foo'])

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
            self.assertTrue(conf.get_boolean('x'))
            self.assertTrue(conf.get_boolean('a'))
            self.assertFalse(conf.get_boolean('y'))
            self.assertFalse(conf.get_boolean('b'))

    def test_getint(self):
        boolean_conf = dedent("""
            [orbach]
            x = 123
            y = 01
        """)
        with temp_file(boolean_conf) as t:
            conf = Config(t)
            self.assertEqual(123, conf.get_int('x'))
            self.assertEqual(1, conf.get_int('y'))

    def test_objectify_options(self):
        conf = dedent("""
            [orbach]
            x = y

            [django]
            DEBUG = True
            SIZE = 3
            NAME = hi
        """)
        with temp_file(conf) as t:
            conf = Config(t).reserved_config()
            self.assertEqual(True, conf['DEBUG'])
            self.assertEqual(3, conf['SIZE'])
            self.assertEqual('hi', conf['NAME'])

    def test_objectify_does_not_cast_integers_to_bools(self):
        conf = dedent("""
            [orbach]
            x = y

            [django]
            DEBUG = 0
            SIZE = 1
        """)
        with temp_file(conf) as t:
            conf = Config(t).reserved_config()
            self.assertEqual(0, conf['DEBUG'])
            self.assertEqual(1, conf['SIZE'])

    def test_reserved_options(self):
        reserved = dedent("""
            [orbach]
            WRONG = this

            [django]
            DEBUG = True
            USE_X_SENDFILE = True
        """)
        with temp_file(reserved) as t:
            conf = Config(t)
            with self.assertRaises(NoOptionError):
                conf['WRONG']

    def test_read_stream(self):
        stream = dedent("""
            [orbach]
            foo = baz
        """)
        with open_mock(stream) as m:
            conf = Config(m)
            self.assertEqual("baz", conf['foo'])

    def test_contains(self):
        with temp_file(self.content) as t:
            conf = Config(t)
            self.assertTrue("hello" in conf)
            self.assertFalse("blah" in conf)

    def test_iter(self):
        with temp_file(self.content) as t:
            conf = Config(t)
            for k, v in conf:
                self.assertTrue(k in ["hello", "goodbye"])
                self.assertEqual("world", v)


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
            conf.delete_section('other')
            parser = ConfigParser()
            parser.read(t)
            self.assertFalse(parser.has_section('other'))
            with self.assertRaises(NoSectionError):
                conf.get_section('other')

    def test_section_access(self):
        with temp_file(self.content) as t:
            conf = Config(t)
            self.assertEqual('bar', conf.get_section('other')['foo'])

    def test_del_from_section(self):
        with temp_file(self.content) as t:
            conf = Config(t)
            del(conf.get_section('other')['foo'])
            parser = ConfigParser()
            parser.read(t)
            self.assertFalse(parser.has_option('other', 'foo'))
            with self.assertRaises(NoOptionError):
                conf.get_section('other')['foo']

    def test_set_to_section(self):
        with temp_file(self.content) as t:
            conf = Config(t)
            conf.get_section('other')['abc'] = 'xyz'
            parser = ConfigParser()
            parser.read(t)
            self.assertTrue(parser.has_option('other', 'abc'))
            self.assertEqual('xyz', conf.get_section('other')['abc'])

    def test_other_sections(self):
        with temp_file(self.content) as t:
            conf = Config(t)
            self.assertFalse(Config.SECTION in conf.other_sections())
            self.assertEqual(['other'], conf.other_sections())

    def test_missing_section(self):
        with temp_file(self.content) as t:
            conf = Config(t)
            with self.assertRaises(NoSectionError):
                conf.get_section('missing')
