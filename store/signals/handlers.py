from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings

from store import models

# create your signals here


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer_when_registered_new_user(instance, created, *args, **kwargs):
    if created:
        models.Customer.objects.create(
            user=instance,
        )
