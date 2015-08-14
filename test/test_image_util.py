import os
import unittest

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from PIL import Image

from orbach.core.image_util import ImageUtil


class ImageUtilTest(unittest.TestCase):
    def setUp(self):
        self.resources = os.path.join(os.path.dirname(__file__), 'resources')

    def test_thumbnail_jpg(self):
        img_path = Path(os.path.join(self.resources, "dog.jpg"))
        with TemporaryDirectory(prefix=self._testMethodName) as d:
            test_path = Path(d).joinpath("dog_tbn.jpg")
            thumbnail = ImageUtil.create_thumbnail(img_path, test_path)
            img = Image.open(str(thumbnail))
            self.assertEqual((140, 250), img.size)

    def test_thumbnail_png(self):
        img_path = Path(os.path.join(self.resources, "cat.png"))
        with TemporaryDirectory(prefix=self._testMethodName) as d:
            test_path = Path(d).joinpath("cat_tbn.png")
            thumbnail = ImageUtil.create_thumbnail(img_path, test_path)
            img = Image.open(str(thumbnail))
            self.assertEqual((140, 250), img.size)

    def test_orientation_jpg(self):
        img = Image.open(os.path.join(self.resources, "dog.jpg"))
        original_size = list(img.size)
        reoriented = ImageUtil._orient(img)
        self.assertEqual(tuple(reversed(original_size)), reoriented.size)

    def test_orientation_png(self):
        img = Image.open(os.path.join(self.resources, "cat.png"))
        with patch.object(img, 'info') as mock_info:
            mock_info.__contains__.return_value = False
            ImageUtil._orient(img)
            mock_info.__contains__.assert_called_once_with('exif')
