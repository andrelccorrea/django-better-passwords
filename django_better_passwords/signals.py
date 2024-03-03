from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_password_record(sender, instance, **kwargs):
    try:
        latest_record = instance.password_records.latest()

        if latest_record.password == instance.password:
            return

    except ObjectDoesNotExist:
        pass

    instance.password_records.create(password=instance.password)
