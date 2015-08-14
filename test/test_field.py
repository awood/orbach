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
import os

from pathlib import Path
from tempfile import TemporaryDirectory

from django.core.files.base import ContentFile
from django.test import TestCase

from orbach.test.models import DummyThumbnailModel, DummyThumbnailNoSignalModel


class ThumbnailImageFieldTest(TestCase):
    def setUp(self):
        super().setUp()
        self.resources = os.path.join(os.path.dirname(__file__), 'resources')
        self.img_path = Path(os.path.join(self.resources, "dog.jpg"))
        self.temp_dir = TemporaryDirectory(prefix="orbach_field_test_")

        with open(str(self.img_path), 'rb') as f:
            self.content = f.read()

    @classmethod
    def tearDownClass(cls):
        DummyThumbnailModel.objects.all().delete()
        DummyThumbnailNoSignalModel.objects.all().delete()

    def test_save(self):
        with self.settings(ORBACH_ROOT=self.temp_dir.name):
            content_file = ContentFile(self.content, name="dog.jpg")
            d = DummyThumbnailModel.objects.create(file=content_file)
            d.refresh_from_db(fields=['file'])
            self.assertRegex(d.file.thumb_path, r'dog_.+_tbn.jpg')

    def test_delete_with_signal_configured(self):
        with self.settings(ORBACH_ROOT=self.temp_dir.name):
            content_file = ContentFile(self.content, name="dog.jpg")
            d = DummyThumbnailModel.objects.create(file=content_file)
            d.refresh_from_db(fields=['file'])
            thumb_path = d.file.thumb_path
            self.assertRegex(thumb_path, r'dog_.+_tbn.jpg')
            self.assertTrue(os.path.exists(thumb_path))
            self.assertTrue(os.path.exists(d.file.path))
            DummyThumbnailModel.objects.all().delete()
            self.assertFalse(os.path.exists(d.file.path))
            self.assertFalse(os.path.exists(thumb_path))

    def test_no_delete_without_signal(self):
        with self.settings(ORBACH_ROOT=self.temp_dir.name):
            content_file = ContentFile(self.content, name="dog.jpg")
            d = DummyThumbnailNoSignalModel.objects.create(file=content_file)
            d.refresh_from_db(fields=['file'])
            thumb_path = d.file.thumb_path
            self.assertRegex(thumb_path, r'dog_.+_tbn.jpg')
            self.assertTrue(os.path.exists(thumb_path))
            self.assertTrue(os.path.exists(d.file.path))
            DummyThumbnailNoSignalModel.objects.all().delete()
            self.assertTrue(os.path.exists(d.file.path))
            self.assertTrue(os.path.exists(thumb_path))
