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
from django.contrib.auth.models import User

from rest_framework import authentication, permissions, viewsets, mixins

from orbach.core.serializers import ImageFileSerializer, UserSerializer,\
    GallerySerializer
from orbach.core.models import ImageFile, Gallery
from orbach.core.permissions import OrbachObjectPermissions


class WriteOnceViewSet(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        mixins.DestroyModelMixin,
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet):
    """A viewset for objects that cannot be updated"""
    pass


class ImageFileViewSet(WriteOnceViewSet):
    queryset = ImageFile.objects.all()
    serializer_class = ImageFileSerializer

    authentication_classes = (authentication.BasicAuthentication,)
    permission_classes = (OrbachObjectPermissions, permissions.IsAdminUser)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class GalleryViewSet(viewsets.ModelViewSet):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer

    authentication_classes = (authentication.BasicAuthentication,)
    permission_classes = (OrbachObjectPermissions, permissions.IsAdminUser)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    authentication_classes = (authentication.BasicAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
