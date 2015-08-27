from django import forms
from .models import Contact
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext as _


bs3_input_class = "form-control"


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


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = [
            'first_name',
            'last_name',
            'birth_date',
            'bio',
            'email',
            'jabber',
            'skype',
            'other',
            'photo'
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": bs3_input_class}),
            "last_name": forms.TextInput(attrs={"class": bs3_input_class}),
            "birth_date": forms.DateInput(attrs={
                "class": bs3_input_class + " datepicker",
            }),
            "bio": forms.Textarea(attrs={
                "class": bs3_input_class,
                "style": "width: 242px; height: 112px;"
            }),
            "email": forms.EmailInput(attrs={"class": bs3_input_class}),
            "jabber": forms.EmailInput(attrs={"class": bs3_input_class}),
            "skype": forms.TextInput(attrs={"class": bs3_input_class}),
            "other": forms.Textarea(attrs={
                "class": bs3_input_class,
                "style": "width: 242px; height: 112px;"
            }),
        }
        labels = {
            'first_name': 'Name: ',
            'last_name': 'Last name: ',
            'birth_date': 'Date of birth: ',
            'bio': 'Bio: ',
            'email': 'Email: ',
            'jabber': 'Jabber: ',
            'skype': 'Skype: ',
            'other': 'Other contacts: ',
            'photo': 'Photo: '
        }
        error_messages = {
            'first_name': {'required': 'First name is required.'},
            'last_name': {'required': 'Surname is required.'},
            'birth_date': {
                'required': 'Birthday date is required.',
                'invalid': 'Set up a valid date (format: yyyy-mm-dd)'
            },
            'email': {'required': 'Email is required.'},
            'jabber': {'required': 'Jabber is required.'},
            'skype': {'required': 'Skype is required.'},
        }
