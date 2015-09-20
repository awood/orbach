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
from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from test import fixtures

from orbach.gallery import msg


class LoginTest(TestCase):
    def test_login(self):
        user = fixtures.UserFactory.create()
        client = Client()
        response = client.post(reverse('gallery:login'), {
            'username': user.username,
            'password': 'password',
        }, follow=True)

        self.assertRedirects(response, reverse('gallery:home'))

    def test_inactive_user_login(self):
        user = fixtures.UserFactory.create(is_active=False)
        client = Client()
        response = client.post(reverse('gallery:login'), {
            'username': user.username,
            'password': 'password',
        }, follow=True)

        self.assertTemplateUsed(response, 'login.html')
        self.assertFormError(response, "form", None, msg.INACTIVE_ACCOUNT)

    def test_bad_password_login(self):
        user = fixtures.UserFactory.create()
        client = Client()
        response = client.post(reverse('gallery:login'), {
            'username': user.username,
            'password': 'WRONG',
        }, follow=True)

        self.assertTemplateUsed(response, 'login.html')
        self.assertFormError(response, "form", None, msg.INVALID_LOGIN)
