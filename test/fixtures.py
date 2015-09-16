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
import factory
from faker import Faker

from orbach.core import models

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User

    first_name = fake.first_name()
    last_name = fake.last_name()
    is_active = True
    username = ".".join([first_name, last_name]).lower()
    password = factory.PostGenerationMethodCall('set_password', 'xanadu')
    email = "%s@%s" % (username, fake.free_email_domain())
