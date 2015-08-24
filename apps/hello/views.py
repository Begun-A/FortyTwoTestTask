from django.views.generic import ListView
from django.views.generic.edit import FormView
from .models import Contact, LogWebRequest
from .forms import LoginForm

from apps import initial_data


class ContactView(ListView):

    template_name = 'hello/contact.html'
    queryset = Contact.objects.get(pk=initial_data[0]['pk'])
    context_object_name = 'contact'


class LogRequestView(ListView):

    template_name = 'hello/requests.html'
    queryset = LogWebRequest.objects.order_by('-id')[:10]
    context_object_name = 'log_requests'


class LoginView(FormView):

    template_name = 'hello/login.html'
    form_class = LoginForm
