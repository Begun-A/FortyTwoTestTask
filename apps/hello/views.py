from django.views.generic import DetailView
from .models import Contact


class ContactView(DetailView):

    template_name = 'hello/contact.html'
    model = Contact
