from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from hello.models import SignalLog


MODELS_IGNORE = (
    'LogEntry',
    'SignalLog',
)


@receiver(post_save, dispatch_uid=settings.SECRET_KEY)
def post_and_put_signal_log(sender, created, **kwargs):
    if created and sender.__name__ not in MODELS_IGNORE:
        SignalLog.objects.create(
            model=sender.__name__,
            action='added'
        )

    if not created and sender.__name__ not in MODELS_IGNORE:
        SignalLog.objects.create(
            model=sender.__name__,
            action='updated'
        )

    return


@receiver(post_delete, dispatch_uid=settings.SECRET_KEY)
def delete_signal_log(sender, **kwargs):
    if sender.__name__ not in MODELS_IGNORE:
        SignalLog.objects.create(
            model=sender.__name__,
            action='removed'
        )

    return
