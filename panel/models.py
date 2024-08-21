from django.db import models
from django.core.validators import validate_integer
from django.conf import settings

from store import models as store_models

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    mobile = models.CharField(max_length=11, validators=[validate_integer])


class SendingMethod(models.Model):
    store = models.ForeignKey(store_models.Store, on_delete=models.CASCADE, related_name='methods', null=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class ShipingRange(models.Model):
    store = models.ForeignKey(store_models.Store, on_delete=models.CASCADE, related_name='ranges', null=True)
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class ShipingCost(models.Model):
    store = models.ForeignKey(store_models.Store, on_delete=models.CASCADE, related_name='costs')
    sending_method = models.ForeignKey(SendingMethod, on_delete=models.CASCADE, related_name='sending_methods', null=True)

    origin = models.ForeignKey(store_models.Province, on_delete=models.CASCADE, related_name='costs')
    destination = models.ForeignKey(store_models.Province, on_delete=models.CASCADE)

    cost = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.origin} to {self.destination}, cost: {self.cost}'
