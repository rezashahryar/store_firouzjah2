from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings

from panel.models import Profile

# create your receivers here


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_when_registered_new_user(instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance
        )
