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
from rest_framework import permissions


class OrbachObjectPermissions(permissions.DjangoObjectPermissions):
    perms_map = {
         'GET': ['%(app_label)s.view_%(model_name)s'],
         'OPTIONS': [],
         'HEAD': [],
         'POST': ['%(app_label)s.add_%(model_name)s'],
         'PUT': ['%(app_label)s.change_%(model_name)s'],
         'PATCH': ['%(app_label)s.change_%(model_name)s'],
         'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }
