from django.apps import AppConfig


class BetterPasswordsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_better_passwords"

    def ready(self):
        # Implicitly connect signal handlers decorated with @receiver.
        import django_better_passwords.signals  # noqa
