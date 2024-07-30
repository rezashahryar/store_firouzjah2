from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings

from user_panel import models

# create your signals and your receivers here


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_when_new_user_registered(instance, created, **kwargs):
    if created:
        models.Profile.objects.create(
            user=instance
        )
