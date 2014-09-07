# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

import unittest

from orbach.util import unicode_in, unicode_out, to_unicode


class ConfigTest(unittest.TestCase):
    def test_to_unicode(self):
        for x in ['hello', 'Motörhead', u'Motörhead']:
            self.assertIsInstance(to_unicode(x), unicode)

    def test_unicode_in_with_str(self):
        self._in()

    def test_unicode_out_with_str(self):
        self._out()

    def test_unicode_in_with_utf8(self):
        self._in('Motörhead', 'Blue Öyster Cult')
        self._in(u'Motörhead', u'Blue Öyster Cult')

    def test_unicode_out_with_utf8(self):
        self._out('Motörhead', 'Blue Öyster Cult')
        self._out(u'Motörhead', u'Blue Öyster Cult')

    def _in(self, test_key='hello', test_value='world'):
        def x(cls, s):
            self.assertIsInstance(s, cls)

        wrapped_x = unicode_in(x)
        wrapped_x(unicode, test_key)

        def y(cls, s=None):
            self.assertIsInstance(s, cls)

        wrapped_y = unicode_in(y)
        wrapped_y(unicode, s=test_key)

        def z(cls, s):
            for i in s:
                if isinstance(i, tuple):
                    self.assertIsInstance(i[0], cls)
                    self.assertIsInstance(i[1], cls)
                else:
                    self.assertIsInstance(i, cls)

        tests = [[test_key, test_value], {test_key: test_value}]
        for test in tests:
            wrapped_z = unicode_in(z)
            wrapped_z(unicode, test)

    def _out(self, test_key='hello', test_value='world'):
        @unicode_out
        def x(s):
            return s

        h = test_key
        self.assertIsInstance(x(h), unicode)

        h = [test_key, test_value]
        map(lambda x: self.assertIsInstance(x, unicode), x(h))

        h = {test_key: test_value}
        for k, v in x(h).items():
            self.assertIsInstance(k, unicode)
            self.assertIsInstance(v, unicode)

    def test_complex_out(self):
        @unicode_out
        def x(s):
            return s

        h = ['hello',
            ['1', '2'],
            {'x': 'y'},
            8]
        out = x(h)
        self.assertIsInstance(out[0], unicode)
        for i in out[1]:
            self.assertIsInstance(i, unicode)
        for k, v in out[2].items():
            self.assertIsInstance(k, unicode)
            self.assertIsInstance(v, unicode)
        self.assertEquals(8, out[3])
