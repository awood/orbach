from pathlib import Path

from flask import current_app

from orbach.model import Gallery, User, ImageFile

from orbach.util import lowercase_ext, image_dir, resolve_path_conflict, hash_stream
from werkzeug.utils import secure_filename
from orbach.errors import ForbiddenFileExtensionError

ARCHIVES = tuple('gz bz2 zip tar tgz txz 7z'.split())
IMAGES = tuple('jpg jpe jpeg png gif svg bmp'.split())


class ImageFileController(object):
    '''
    Class used to perform all manipulations on Gallery objects
    '''

    def __init__(self, image_id):
        self.image_id = image_id

    @staticmethod
    def create(request):
        f = request.files['file']
        filename = secure_filename(f.filename)
        allowed = f and lowercase_ext(filename) in ARCHIVES + IMAGES
        if not allowed:
            raise ForbiddenFileExtensionError(lowercase_ext(f.filename))

        triplet = hash_stream(f)[:3]

        storage_dir = Path(image_dir()).joinpath(triplet)
        try:
            storage_dir.mkdir()
        except FileExistsError:
            pass

        destination = storage_dir.joinpath(filename)

        if destination.exists():
            destination = resolve_path_conflict(destination)

        f.save(str(destination))

        thumbnail_path = current_app.image_util.create_thumbnail(destination, storage_dir)

        return {
            'image_file': destination.relative_to(image_dir()),
            'thumbnail_file': thumbnail_path.relative_to(image_dir())
        }

    @staticmethod
    def get_all():
        return ImageFile.query.order_by(ImageFile.id).all()

    def get(self):
        pass

    def modify(self):
        pass

    def delete(self):
        pass


class GalleryController(object):
    '''
    Class used to perform all manipulations on Gallery objects
    '''

    def __init__(self, gallery_id):
        self.gallery_id = gallery_id

    @staticmethod
    def create(gallery):
        pass

    @staticmethod
    def get_all():
        return Gallery.query.order_by(Gallery.name).all()

    def get(self):
        pass

    def modify(self):
        pass

    def delete(self):
        pass


class UserController(object):
    '''
    Class used to perform all manipulations on User objects
    '''

    def __init__(self, user):
        self.gallery = user

    @staticmethod
    def create(user):
        pass

    @staticmethod
    def get_all():
        return User.query.order_by(User.username).all()

    def get(self):
        pass

    def modify(self):
        pass

    def delete(self):
        pass
