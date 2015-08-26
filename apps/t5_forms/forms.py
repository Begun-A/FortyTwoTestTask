from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext as _


class LoginForm(AuthenticationForm):

    username = forms.CharField(
        label=_("Username"),
        error_messages={
            "required": _("Username is required.")
        },
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'username'
        }),
    )
    password = forms.CharField(
        label=_("Password"),
        error_messages={
            "required": _("Password is required.")
        },
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'password'
        }),
    )
