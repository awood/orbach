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
from django.contrib import auth, messages
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _

from orbach.gallery.forms import UploadPhotosForm


def upload_photos(request):
    nav = {
        'active': 'upload_photos',
        'section': 'photos',
    }
    if request.method == 'POST':
        form = UploadPhotosForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = UploadPhotosForm
    return render(request, 'actions/upload_photos.html', {'nav': nav, 'form': form})


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
