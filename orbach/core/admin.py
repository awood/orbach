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
from django.contrib import admin

from orbach.core.models import ImageFile, Gallery, Cover, Picture
from guardian.admin import GuardedModelAdmin


class ImageFileAdmin(GuardedModelAdmin):
    pass


class GalleryAdmin(GuardedModelAdmin):
    pass


class PictureAdmin(GuardedModelAdmin):
    pass


admin.site.register(ImageFile, ImageFileAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Picture, PictureAdmin)
admin.site.register(Cover)
