from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import (
    resolve,
    reverse,
)
from django.utils import timezone
from django.utils.translation import gettext as _


class PasswordExpirationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.expiration_days = timezone.timedelta(
            days=getattr(settings, "DBP_PASSWORD_EXPIRATION_DAYS", 60)
        )

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        resolver_match = resolve(request.path)
        user = request.user

        if user.is_authenticated:
            latest_record = user.password_records.latest()
            records_count = user.password_records.count()

            if ((timezone.now() - latest_record.date) >= self.expiration_days) or (
                records_count <= 1
            ):
                if (
                    resolver_match.app_name == "admin"
                    and resolver_match.url_name
                    not in (
                        "password_change",
                        "logout",
                    )
                    or not resolver_match.app_name
                    and resolver_match.url_name in ("pages-root", "pages-details-by-slug")
                ):
                    return redirect(
                        reverse(
                            "admin:password_change",
                            current_app=resolver_match.namespace,
                        )
                    )
                elif (
                    hasattr(settings, "DBP_PASSWORD_CHANGE_REDIRECT_URL")
                    and bool(settings.DBP_PASSWORD_CHANGE_REDIRECT_URL)
                    and resolver_match.url_name
                    not in (
                        settings.DBP_PASSWORD_CHANGE_REDIRECT_URL,
                        settings.DBP_LOGOUT_URL,
                    )
                ):
                    return redirect(
                        reverse(
                            settings.DBP_PASSWORD_CHANGE_REDIRECT_URL,
                            current_app=resolver_match.namespace,
                        )
                    )

                if request.method == "GET":
                    message = (
                        "Update your password to get started."
                        if records_count <= 1
                        else f"Your password is at least {self.expiration_days.days} days old and needs to be updated."
                    )

                    messages.add_message(
                        request,
                        messages.WARNING,
                        _(message),
                        fail_silently=True,
                    )

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
