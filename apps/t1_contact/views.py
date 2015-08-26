import json
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.views.generic import UpdateView
from .models import Contact
from .forms import ContactForm

from apps import initial_data


class ContactView(UpdateView):

    template_name = 't1_contact/contact.html'
    model = Contact
    pk_url_kwarg = initial_data[0]['pk']
    context_object_name = 'contact'
    form_class = ContactForm

    def get_initial(self):
        data = json.loads(
            serializers.serialize(
                'json',
                [self.model.objects.get(pk=self.pk_url_kwarg), ])
        )[0]['fields']
        return dict(**data)

    def get_object(self):
        return get_object_or_404(Contact, pk=self.pk_url_kwarg)
