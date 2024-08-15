import django

from datetime import timedelta
from uuid import uuid4

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import integer_validator

from .validators import validate_isdigit
# Create your models here.


class User(AbstractUser):
    mobile = models.CharField(max_length=11, unique=True, validators=[integer_validator])


def get_datetime_now():
    return timezone.localtime(timezone.now()) + timedelta(minutes=3)


class OtpRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    mobile = models.CharField(max_length=11)
    otp_code = models.CharField(max_length=5)

    valid_from = models.DateTimeField(default=django.utils.timezone.now, null=True)
    valid_until = models.DateTimeField(default=get_datetime_now, null=True)
