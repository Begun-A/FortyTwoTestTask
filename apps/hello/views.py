from django.views.generic import DetailView, TemplateView
from .models import Contact


class ContactView(DetailView):

    template_name = 'hello/contact.html'
    model = Contact


class LogRequestView(TemplateView):

    template_name = 'hello/requests.html'
