from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_better_passwords.models import PasswordRecord


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_password_record(sender, instance, **kwargs):

    if hasattr(instance, "password_records"):
        record = instance.password_records

        if record.password != instance.password:
            record.password = instance.password
            record.first_login = False
            record.save()
        return

    password = PasswordRecord(user=instance, password=instance.password)
    password.save()
