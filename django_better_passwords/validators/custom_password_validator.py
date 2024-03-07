from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _


class CustomPasswordValidator:
    """
    - Validates password maximum and minimum length;
    - Ensures that it contains required characters, at least one digit, one
    upper case and one lower case letters;
    - Ensures that it not contains forbidden characters;

    Args:
        - min_length (Optional[int]): minimum length, defaults to 6
        - max_length (Optional[int]): maximum length, defaults to 30
        - required_characters (Optional[str]): characters that must be present,
        defaults to ''
        - required_characters_count (Optional[int]): number of required characters
        that must be present, defaults to 1
        - forbidden_characters (Optional[str]): characters that cannot be present,
        defaults to ''
    """

    def __init__(
        self,
        min_length: int = 6,
        max_length: int = 30,
        required_characters: str = "",
        required_characters_count: int = 1,
        forbidden_characters: str = "",
    ):
        self.min_length = min_length
        self.max_length = max_length
        self.required_characters = required_characters
        self.required_characters_count = required_characters_count
        self.forbidden_characters = forbidden_characters

    def validate(self, password, user=None):
        self._validate_min_length(password=password)
        self._validate_max_length(password=password)
        self._validate_required_characters(password=password)
        self._validate_forbidden_characters(password=password)
        self._validate_digits(password=password)
        self._validate_upper_case_letter(password=password)
        self._validate_lower_case_letter(password=password)

    def _validate_min_length(self, password: str):
        if len(password) < self.min_length:
            raise ValidationError(
                _(f"Password must contain at least {self.min_length} characters.")
            )

    def _validate_max_length(self, password: str):
        if len(password) > self.max_length:
            raise ValidationError(
                _(f"Password cannot be longer than {self.max_length} characters.")
            )

    def _validate_required_characters(self, password: str):

        if self.required_characters and self.required_characters_count > 0:
            count = sum(1 for char in password if char in self.required_characters)

            if count < self.required_characters_count:
                raise ValidationError(
                    _(
                        f"Password must contain at least {self.required_characters_count} of the following characters: {self.required_characters}"
                    )
                )

    def _validate_forbidden_characters(self, password: str):
        if self.forbidden_characters and any(
            char in self.forbidden_characters for char in password
        ):
            raise ValidationError(
                _(f"Password cannot contain the following characters: {self.forbidden_characters}.")
            )

    def _validate_digits(self, password: str):
        if not any(char.isdigit() for char in password):
            raise ValidationError(_("Password must contain at least one digit."))

    def _validate_upper_case_letter(self, password: str):
        if not any(char.isupper() for char in password):
            raise ValidationError(_("Password must contain at least one upper case letter."))

    def _validate_lower_case_letter(self, password: str):
        if not any(char.islower() for char in password):
            raise ValidationError(_("Password must contain at least one lower case letter."))

    def get_help_text(self):
        help_text = (
            f"Your password must be between {self.min_length} and {self.max_length} characters lenght.<br>"
            "Your password must contain at least one digit, one upper case and one lower case letters.<br>"
        )

        if self.required_characters:
            help_text += f"Your password must contain at least one of the following characters: {self.required_characters}<br>"

        if self.forbidden_characters:
            help_text += f"Your password cannot contain the following characters: {self.forbidden_characters}.<br>"

        return _(mark_safe(help_text))
