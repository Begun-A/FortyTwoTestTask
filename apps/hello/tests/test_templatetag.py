from django.test import TestCase
from django.core.urlresolvers import reverse, reverse_lazy
from django.template import Context, Template

from hello.models import Contact


class TemplateTagUnitTest(TestCase):
    """Test tempalte tag if present on the page with correct url.
    """
    fixtures = ['initial_data.json']

    def setUp(self):
        self.fake_path = reverse('contact')
        self.model = Contact
        self.model_name = self.model._meta.model_name
        self.app_name = 'hello'
        self.tag_name = 'edit_link'

    def test_get_template_tag_on_page(self):
        """Check if template tag present on the page.
        """
        load_tag = "{%% load %s %%}" % self.tag_name
        edit_tag = "{%% %s %s %%}" % (
            self.tag_name,
            self.model_name
        )
        template = Template(load_tag + edit_tag)
        queryset = self.model.objects.last()
        context = Context({"contact": queryset})
        needed_path = reverse_lazy(
            "admin:%s_%s_change" % (self.app_name, self.model_name),
            args=(queryset.id,)
        )
        self.assertEqual(needed_path, template.render(context))
