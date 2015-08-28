from django.core import urlresolvers
from django.contrib.contenttypes.models import ContentType

from django import template
register = template.Library()


@register.simple_tag
def edit_link(instance):
    try:
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return urlresolvers.reverse_lazy(
            "admin:%s_%s_change" % (
                content_type.app_label, content_type.model
            ),
            args=(instance.id, )
        )
    except:
        return ""
