'''
Copyright 2015

This file is part of Orbach.

Orbach is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Orbach is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Orbach.  If not, see <http://www.gnu.org/licenses/>.
'''
import unittest
import hashlib
import os

from tempfile import TemporaryDirectory
from orbach.core.storage import HashDistributedStorage
from django.core.files.base import ContentFile


class StorageTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = TemporaryDirectory(prefix="orbach_storage_test_")
        self.storage = HashDistributedStorage(location=self.temp_dir.name, base_url='/test_storage/')

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_creates_path_based_on_hash(self):
        file_name = 'foobar.gif'
        content = file_name.encode('utf-8')
        expected_prefix = hashlib.sha256(content).hexdigest()[:3]
        expected_path = os.path.join(self.temp_dir.name, expected_prefix, file_name)

        self.storage.save(file_name, ContentFile('Hello World'))

        self.assertEqual(expected_path, self.storage.path(file_name))
        self.assertTrue(os.path.exists(expected_path))
        with self.storage.open(expected_path) as f:
            self.assertEqual(f.read(), b'Hello World')
        self.storage.delete(expected_path)

    def test_forbids_unknown_extensions(self):
        file_name = 'foobar.txt'
        with self.assertRaises(IOError):
            self.storage.save(file_name, ContentFile('Hello World'))

    def test_allows_uppercase_extensions(self):
        file_name = 'foobar.JPG'
        content = 'foobar.jpg'.encode('utf-8')
        expected_prefix = hashlib.sha256(content).hexdigest()[:3]
        expected_path = os.path.join(self.temp_dir.name, expected_prefix, 'foobar.jpg')

        self.storage.save(file_name, ContentFile('Hello World'))

        self.assertEqual(expected_path, self.storage.path(file_name))
        self.assertTrue(os.path.exists(expected_path))
        with self.storage.open(expected_path) as f:
            self.assertEqual(f.read(), b'Hello World')
        self.storage.delete(expected_path)
