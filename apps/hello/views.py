from django.views.generic import ListView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import login
from .models import Contact, LogWebRequest
from .forms import LoginForm
from .mixins import AjaxableResponseMixin

from apps import initial_data


class ContactView(ListView):

    template_name = 'hello/contact.html'
    queryset = Contact.objects.get(pk=initial_data[0]['pk'])
    context_object_name = 'contact'


class LogRequestView(ListView):

    template_name = 'hello/requests.html'
    queryset = LogWebRequest.objects.order_by('-id')[:10]
    context_object_name = 'log_requests'


class LoginView(AjaxableResponseMixin, FormView):

    template_name = 'hello/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('contact')

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)
