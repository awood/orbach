import os

from werkzeug.datastructures import FileStorage

from orbach.util import hash_file, hash_stream

from test.test_orbach import OrbachTest
from orbach.errors import ForbiddenFileExtensionError


# TODO - These tests all run through the REST API before hitting the controller.  Fix that.
class UploadTest(OrbachTest):
    def create_app(self, *args, **kwargs):
        app = super().create_app(*args, **kwargs)
        self.destination = os.path.join(app.config.orbach['application_root'], 'images')
        self.resources = os.path.join(os.path.dirname(__file__), 'resources')
        return app

    def test_simple_upload(self):
        with open(os.path.join(self.resources, 'dog.jpg'), 'rb') as f:
            digest = hash_stream(f)
            triplet = digest[:3]

            f.seek(0)

            storage = FileStorage(f, 'dog.jpg')
            resp = self.client.post(
                path='/api/v1/image_files/',
                data={'file': storage}
            )
            self.assert200(resp)
            self.assertEqual(os.path.join(triplet, 'dog.jpg'), resp.json['image_file'])
            destination_path = os.path.join(self.destination, triplet, 'dog.jpg')
            self.assertTrue(os.path.exists(destination_path))

            with hash_file(destination_path) as result_digest:
                self.assertEquals(digest, result_digest)

    def test_forbidden_extension(self):
        with open(os.path.join(self.resources, 'not_allowed.txt'), 'rb') as f:
            storage = FileStorage(f, 'not_allowed.txt')
            with self.assertRaises(ForbiddenFileExtensionError):
                self.client.post(
                    path='/api/v1/image_files/',
                    data={'file': storage}
                )
