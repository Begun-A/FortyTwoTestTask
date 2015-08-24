from django.views.generic import ListView
from .models import Contact, LogWebRequest

from apps import initial_data


class ContactView(ListView):

    template_name = 'hello/contact.html'
    queryset = Contact.objects.get(pk=initial_data[0]['pk'])
    context_object_name = 'contact'


class LogRequestView(ListView):

    template_name = 'hello/requests.html'
    queryset = LogWebRequest.objects.order_by('-id')[:10]
    context_object_name = 'log_requests'
