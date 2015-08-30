from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from hello.models import Contact


class ContactView(DetailView):

    template_name = 'contact.html'
    model = Contact
    email = "dev1dor@ukr.net"
    pk_url_kwarg = model.objects.get(email=email).pk
    context_object_name = 'contact'

    def get_object(self):
        return get_object_or_404(Contact, pk=self.pk_url_kwarg)
