from django.views.generic import ListView
from .models import Contact

from apps import initial_data


class ContactView(ListView):

    template_name = 't1_contact/contact.html'
    queryset = Contact.objects.get(pk=initial_data[0]['pk'])
    context_object_name = 'contact'
