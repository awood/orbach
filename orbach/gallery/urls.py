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
from django.conf.urls import url, include

from orbach.gallery import views as v
from orbach.gallery import action_views as action


action_patterns = [
    url(r'^upload_photos.html$', action.upload_photos, name="upload_photos"),
    url(r'^modify_photos.html$', action.modify_photos, name="modify_photos"),
    url(r'^delete_photos.html$', action.delete_photos, name="delete_photos"),
    url(r'^create_galleries.html$', action.create_galleries, name="create_galleries"),
    url(r'^modify_galleries.html$', action.modify_galleries, name="modify_galleries"),
    url(r'^delete_galleries.html$', action.delete_galleries, name="delete_galleries"),
]

urlpatterns = [
    url(r'^$', v.home),
    url(r'^index.html$', v.home, name='home'),
    url(r'^login.html$', v.login, name='login'),
    url(r'^logout.html$', v.logout, name='logout'),
    url(r'^(?P<filename>(robots.txt))$', v.text_file, name='text_file'),
    url(r'^lost_username.html$', v.lost_username, name='lost_username'),
    url(r'^lost_password.html$', v.lost_password, name='lost_password'),
    url(r'^actions/', include(action_patterns)),
]
