import json
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.views.generic import UpdateView
from django.core.urlresolvers import reverse_lazy

from hello.mixins import AjaxableResponseMixin, LoginRequiredMixin
from hello.models import Contact
from hello.forms import ContactForm


class EditView(LoginRequiredMixin, AjaxableResponseMixin, UpdateView):

    template_name = 'edit.html'
    model = Contact
    pk_url_kwarg = 1
    context_object_name = 'contact'
    form_class = ContactForm
    success_url = reverse_lazy('edit')

    def get_initial(self):
        return json.loads(
            serializers.serialize(
                'json',
                [self.model.objects.get(pk=self.pk_url_kwarg), ])
        )[0]['fields']

    def get_object(self):
        return get_object_or_404(Contact, pk=self.pk_url_kwarg)

    def form_valid(self, form):
        self.object = form.save()
        self.data = self.get_initial()
        return super(EditView, self).form_valid(form)
