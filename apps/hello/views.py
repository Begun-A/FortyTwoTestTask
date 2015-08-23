from django.views.generic import DetailView, ListView
from .models import Contact, LogWebRequest


class ContactView(DetailView):

    template_name = 'hello/contact.html'
    model = Contact


class LogRequestView(ListView):

    template_name = 'hello/requests.html'
    queryset = LogWebRequest.objects.order_by('-id')[:10]
    context_object_name = 'log_requests'
