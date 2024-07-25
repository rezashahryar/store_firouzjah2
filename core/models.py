from django.db import models
from django.contrib.auth.models import AbstractUser

from .validators import validate_isdigit
# Create your models here.


class User(AbstractUser):
    mobile = models.CharField(max_length=11, unique=True, validators=[validate_isdigit])
