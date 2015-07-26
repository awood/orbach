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
from django.contrib.auth.models import User, Group
from orbach.core.models import ImageFile, Picture, Cover, Gallery

from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        lookup_field = 'username'
        fields = ('username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('name')


class ImageFileSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = ImageFile
        fields = ('id', 'owner', 'file', 'created', 'modified', 'height', 'width')
        read_only_fields = ('id', 'owner', 'height', 'width', 'created', 'modified')


class PictureSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Picture


class CoverSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cover


class GallerySerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Gallery
