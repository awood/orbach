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
import logging

from django.contrib import auth
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http.response import HttpResponseForbidden
from django.utils.translation import ugettext as _

from orbach.gallery.forms import LoginForm
from orbach.core.util import HttpResponseUnauthorized

log = logging.getLogger(__name__)


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
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    log.info("Logging in {}".format(username))
                    auth.login(request, user)
                    return HttpResponseRedirect('/gallery/index.html')
                else:
                    form.add_error(None, _("Your account is inactive."))
            else:
                form.add_error(None, _("Invalid login details."))
    else:
        form = LoginForm
    return render(request, 'login.html', {'form': form, 'pf_class': 'login-pf'})
