from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Display all models in db and objects count of each model.'

    def handle(self, *args, **options):
        for ct in ContentType.objects.all():
            m = ct.model_class()
            msg = "Model: %(module)s.%(model)s, count: %(count)s" % dict(
                module=m.__module__,
                model=m.__name__,
                count=m.objects.count()
            )
            self.stdout.write(msg)
            self.stderr.write("error: " + msg)
