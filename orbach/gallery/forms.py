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

from django import forms
from django.forms import widgets

from django.utils.translation import ugettext as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML, Submit


class LoginForm(forms.Form):
    username = forms.CharField(
        label=_("Username"),
        max_length=80,
        required=True,
    )

    password = forms.CharField(
        label=_("Password"),
        max_length=80,
        required=True,
        widget=widgets.PasswordInput
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'login_form'
        self.helper.form_method = 'post'
        self.helper.form_action = 'login.html'

        self.helper.form_class = 'form-horizontal'
        self.helper.field_class = 'col-sm-10 col-md-10'
        self.helper.label_class = 'col-sm-2 col-md-2'

        self.helper.layout = Layout(
            "username",
            "password",
            Div(
                Div(
                      #{% blocktrans with l_username_anchor=%s(name_link) l_password_anchor=%s(pw_link) %s(end_anchor) %}
                    HTML('''{% load i18n %}
                    {% url 'gallery:lost_username' as username_url %}
                    {% url 'gallery:lost_password' as password_url %}
                    <span class="help-block">
                      {% blocktrans %}
                      Forgot <a href="{{ username_url }}">username</a> or <a href="{{ password_url }}">password</a>?
                      {% endblocktrans %}
                    </span>'''),
                    css_class="col-xs-8 col-sm-offset-2 col-sm-6 col-md-offset-2 col-md-6"
                ),
                Div(
                    Submit('sign_in', _('Sign in'), css_class='btn btn-primary btn-lg'),
                    css_class="col-xs-4 col-sm-4 col-md-4 submit"
                ),
                css_class="form-group",
            )
        )


class AddPhotosForm(forms.Form):
    file = forms.FileField(
        label=_('File'),
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
