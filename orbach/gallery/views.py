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
from django.shortcuts import render
from django.http import HttpResponseRedirect


from orbach.gallery.forms import LoginForm


def home(request):
    return render(request, "index.html", {})


def text_file(request, filename):
    return render(request, filename, {}, content_type='text/plain')


def lost_username(request):
    # FIXME
    return render(request, "index.html", {})


def lost_password(request):
    # FIXME
    return render(request, "index.html", {})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')
    else:
        return render(request, 'login.html', {'form': LoginForm, 'pf_class': 'login-pf'})
