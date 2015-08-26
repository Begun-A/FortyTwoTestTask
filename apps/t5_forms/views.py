from django.views.generic import RedirectView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import login, logout
from .forms import LoginForm
from .mixins import AjaxableResponseMixin


class LoginView(AjaxableResponseMixin, FormView):

    template_name = 't5_forms/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('contact')

    def form_valid(self, form):
        login(self.request, form.get_user())
        self.data = dict(url=self.get_success_url())
        return super(LoginView, self).form_valid(form)


class LogoutView(RedirectView):

    url = reverse_lazy('contact')

    def post(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).post(request, *args, **kwargs)
