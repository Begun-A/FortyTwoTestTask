from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from hello.models import Contact

from apps import initial_data


class ContactView(DetailView):

    template_name = 'contact.html'
    model = Contact
    pk_url_kwarg = initial_data[0]['pk']
    context_object_name = 'contact'

    def get_object(self):
        return get_object_or_404(Contact, pk=self.pk_url_kwarg)
