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
import mimetypes
import zipfile

from django.shortcuts import render
from django.http import HttpResponseBadRequest
from django.http.response import JsonResponse
from django.utils.translation import ugettext as _

from orbach.gallery.forms import ImageFileForm, ArchiveFileForm
from orbach.core import models

import logging
from django.core.files.uploadedfile import SimpleUploadedFile
log = logging.getLogger(__name__)


def upload_photos(request):
    nav = {
        'active': 'upload_photos',
        'section': 'photos',
    }
    # TODO This is ugly
    if request.method == 'POST':
        images = []
        names = []

        # TODO This is a mess since the blueimp file upload will not display more
        # files than there are divs to hold them.  Since the zip file only creates
        # one div, either we have to pack all the return information into that one
        # div or else figure out enough Javascript to create divs for each file item
        # to display in.  Right now we are going with the former.
        if ('file' in request.FILES and request.FILES['file'].content_type == 'application/zip'):
            form = ArchiveFileForm(request.user, request.POST, request.FILES)
            if form.is_valid():
                with zipfile.ZipFile(request.FILES['file']) as z:
                    for filename in z.namelist():
                        data = z.read(filename)
                        file = SimpleUploadedFile(filename, data, mimetypes.guess_type(filename)[0])
                        image = models.ImageFile.create(file=file, owner=request.user)
                        image.save()
                        images.append(image)
                        names.append(filename)
            else:
                return HttpResponseBadRequest(_('Must have files attached!'))
        else:
            form = ImageFileForm(request.user, request.POST, request.FILES)
            if form.is_valid():
                image = form.save()
                images.append(image)
                names.append(image.file.name)
            else:
                return HttpResponseBadRequest(_('Must have files attached!'))

        result = []
        for image in images:
            file = image.file
            result.append({
                "name": names,
                "size": file.size,
                "url": file.url,
                "thumbnail_url": file.thumb_url,
                "type": mimetypes.guess_type(file.name)[0]
            })
        return JsonResponse({"files": result})
    return render(request, 'actions/upload_photos.html', {'nav': nav})


def modify_photos(request):
    nav = {
        'active': 'modify_photos',
        'section': 'photos',
    }
    return render(request, 'actions/modify_photos.html', {'nav': nav})


def delete_photos(request):
    nav = {
        'active': 'delete_photos',
        'section': 'photos',
    }
    return render(request, 'actions/delete_photos.html', {'nav': nav})


def create_galleries(request):
    nav = {
        'active': 'create_galleries',
        'section': 'galleries',
    }
    return render(request, 'actions/create_galleries.html', {'nav': nav})


def modify_galleries(request):
    nav = {
        'active': 'modify_galleries',
        'section': 'galleries',
    }
    return render(request, 'actions/modify_galleries.html', {'nav': nav})


def delete_galleries(request):
    nav = {
        'active': 'delete_galleries',
        'section': 'galleries',
    }
    return render(request, 'actions/delete_galleries.html', {'nav': nav})
