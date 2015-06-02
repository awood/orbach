from pathlib import Path

from PIL import Image


class ImageUtil(object):
    def __init__(self, thumbnail_size=None):
        if thumbnail_size is None:
            thumbnail_size = (250, 250)
        self.thumbnail_size = thumbnail_size

    def create_thumbnail(self, image_path, destination_directory):
        destination_file = Path("{}_tbn{}".format(image_path.stem, "".join(image_path.suffixes)))
        destination_path = destination_directory.joinpath(destination_file)

        if destination_path == image_path:
            raise IOError(_("Destination and source are the same: {}").format(image_path))

        img = Image.open(str(image_path))

        # TODO need to fix orientation on thumbnail

        img.thumbnail(self.thumbnail_size)
        img.save(str(destination_path))
        return destination_path
