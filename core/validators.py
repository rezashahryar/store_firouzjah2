from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_isdigit(value):
    if not value.isdigit():
        raise ValidationError(
            _(" باید فقط از اعداد تشکیل شده باشد"),
            params={"value": value},
        )
