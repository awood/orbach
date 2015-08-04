from PIL import Image, ExifTags

from django.utils.translation import ugettext as _

# The Exif codes dictionary has some keys that appear more than once,
# so we can't just reverse the dictionary
codes, names = zip(*ExifTags.TAGS.items())
REVERSE_TAGS = dict(zip(names, [[] for x in names]))
for c in codes:
    name = ExifTags.TAGS[c]
    REVERSE_TAGS[name].append(c)


class ImageUtil(object):
    @staticmethod
    def create_thumbnail(image_path, destination_path, thumb_width=250, thumb_height=250):
        """Create a thumbnail of image_path and save to destination_path using thumb_width
        and thumb_height as the dimensions.  Both image_path and destination_path may be Path
        objects."""
        thumbnail_size = (thumb_width, thumb_height)

        if destination_path == image_path:
            raise IOError(_("Destination and source are the same: {}").format(image_path))

        img = Image.open(str(image_path))

        img.thumbnail(thumbnail_size, Image.ANTIALIAS)
        img = ImageUtil._orient(img)
        img.save(str(destination_path))
        return destination_path

    @staticmethod
    def _orient(img):
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
