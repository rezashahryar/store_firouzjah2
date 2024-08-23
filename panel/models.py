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
    

class RequestAddProduct(models.Model):

    class RequestStatus(models.TextChoices):
        APPROVED = 'a', 'تایید شده'
        WAITING = 'w', 'در انتظار تایید'
        NOT_APPROVED = 'n', 'عدم تایید'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='requests_add_product')
    product = models.ForeignKey(store_models.Product, on_delete=models.CASCADE, related_name='requests_add_product')

    description = models.TextField()

    status = models.CharField(max_length=1, choices=RequestStatus.choices, default=RequestStatus.WAITING)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-datetime_created', )


class SupportTicket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tickets')
    subject = models.CharField(max_length=255)
    text = models.TextField()
    annex = models.FileField(null=True, blank=True)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.subject}: {self.text[:20]}'
    

class AnswerSupportTicket(models.Model):
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='answer_tickets')
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField()
    annex = models.FileField(null=True, blank=True)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.reviewer} for ticket: {self.ticket.subject}'
