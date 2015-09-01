from django.views.generic import UpdateView
from django.core.urlresolvers import reverse_lazy

from hello.mixins import AjaxableResponseMixin, LoginRequiredMixin
from hello.models import Contact
from hello.forms import ContactForm


class EditView(LoginRequiredMixin, AjaxableResponseMixin, UpdateView):

    template_name = 'edit.html'
    model = Contact
    context_object_name = 'contact'
    form_class = ContactForm

    def get_success_url(self):
        if 'pk' in self.kwargs:
            pk = self.kwargs['pk']
            return reverse_lazy('edit', kwargs={"pk": pk})
        super(EditView, self).get_success_url()

    def get_initial(self):
        return self.model.objects.filter(pk=self.kwargs['pk']).values()[0]

    def form_valid(self, form):
        self.object = form.save()
        self.data = self.get_initial()
        return super(EditView, self).form_valid(form)
