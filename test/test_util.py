import unittest

from pathlib import Path
from unittest.mock import patch

from orbach.util import resolve_path_conflict
from orbach.util import Path as PatchPath


class ConflictResolverTest(unittest.TestCase):
    def test_simple_conflict(self):
        filename = Path("/tmp/hello.jpg")
        result = resolve_path_conflict(filename)
        self.assertEqual(Path("/tmp/hello_01.jpg"), result)

    @patch.object(PatchPath, 'exists')
    def test_double_conflict(self, mock_exists):
        mock_exists.side_effect = [True, False]
        filename = Path("/tmp/hello.jpg")
        result = resolve_path_conflict(filename)
        self.assertEqual(Path("/tmp/hello_02.jpg"), result)

    @patch.object(PatchPath, 'exists')
    def test_complex_conflict(self, mock_exists):
        mock_exists.side_effect = ([True] * 99) + [False]
        filename = Path("/tmp/hello.jpg")
        result = resolve_path_conflict(filename)
        self.assertEqual(Path("/tmp/hello_100.jpg"), result)

    def test_multiple_extensions(self):
        filename = Path("/tmp/hello.tar.gz")
        result = resolve_path_conflict(filename)
        self.assertEqual(Path("/tmp/hello_01.tar.gz"), result)
