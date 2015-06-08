from pathlib import Path

from PIL import Image, ExifTags

from flask.ext.babel import _

# The Exif codes dictionary has some keys that appear more than once,
# so we can't just reverse the dictionary
codes, names = zip(*ExifTags.TAGS.items())
REVERSE_TAGS = dict(zip(names, [[] for x in names]))
for c in codes:
    name = ExifTags.TAGS[c]
    REVERSE_TAGS[name].append(c)


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

        img.thumbnail(self.thumbnail_size, Image.ANTIALIAS)
        img = self._orient(img)
        img.save(str(destination_path))
        return destination_path

    def _orient(self, img):
        """Much of this courtesy http://stackoverflow.com/questions/4228530"""
        if 'exif' not in img.info:
            # Not a JPG
            return img

        tags = img._getexif()

        # Orientation should only have one Exif code
        orientation = tags.get(REVERSE_TAGS['Orientation'][0], None)

        transposition = None
        if orientation == 3:
            transposition = Image.ROTATE_180
        elif orientation == 6:
            transposition = Image.ROTATE_270
        elif orientation == 8:
            transposition = Image.ROTATE_90

        if transposition:
            img = img.transpose(transposition)
        return img
