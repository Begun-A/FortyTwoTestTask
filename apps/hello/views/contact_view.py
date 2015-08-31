from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from hello.models import Contact
from hello.fixtures import settings as init_settings


class ContactView(DetailView):

    template_name = 'contact.html'
    model = Contact
    context_object_name = 'contact'
    pk_url_kwarg = init_settings[0]['pk']

    def get_object(self):
        return get_object_or_404(Contact, pk=self.pk_url_kwarg)
