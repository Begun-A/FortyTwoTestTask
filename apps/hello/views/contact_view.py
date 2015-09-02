from django.views.generic import DetailView

from hello.models import Contact


class ContactView(DetailView):

    template_name = 'contact.html'
    model = Contact
    context_object_name = 'contact'

    def get_object(self):
        return self.model.objects.first()
