from __future__ import print_function, division, absolute_import

import unittest

from test import temp_file
from textwrap import dedent

from ConfigParser import SafeConfigParser

from orbach.config import Config


class ConfigTest(unittest.TestCase):
    def setUp(self):
        self.content = dedent("""
            [orbach]
            hello = world
            goodbye = world
        """)

    def test_len(self):
        with temp_file(self.content) as t:
            conf = Config(t)
            self.assertEquals(2, len(conf))

    def test_contains(self):
        with temp_file(self.content) as t:
            conf = Config(t)
            self.assertTrue('hello' in conf)
            self.assertFalse('xyz' in conf)

    def test_get(self):
        with temp_file(self.content) as t:
            conf = Config(t)
            self.assertEquals(conf['hello'], 'world')

    def test_get_unicode(self):
        with temp_file(self.content) as t:
            conf = Config(t)
            self.assertIsInstance(conf['hello'], unicode)

    def test_bad_get(self):
        with temp_file(self.content) as t:
            conf = Config(t)
            with self.assertRaises(KeyError):
                conf['does_not_exist']

    def test_set(self):
        with temp_file(self.content) as t:
            conf = Config(t)
            conf['foo'] = 'bar'
            parser = SafeConfigParser()
            parser.read(t)
            self.assertTrue(parser.has_option(conf.SECTION, 'foo'))
            self.assertEquals('bar', conf['foo'])

    def test_set_unicode(self):
        with temp_file(self.content) as t:
            conf = Config(t)
            conf['foo'] = 'bar'
            self.assertIsInstance(conf['foo'], unicode)

    def test_del(self):
        with temp_file(self.content) as t:
            conf = Config(t)
            del(conf['hello'])
            parser = SafeConfigParser()
            parser.read(t)
            self.assertFalse(parser.has_option(conf.SECTION, 'hello'))
            with self.assertRaises(KeyError):
                conf['hello']

    def test_iter(self):
        with temp_file(self.content) as t:
            conf = Config(t)
            for k, v in conf:
                self.assertTrue(isinstance(k, unicode))
                self.assertTrue(isinstance(v, unicode))