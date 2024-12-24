import logging

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .tasks import welcome_new_user


logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def new_user_or_update_user(sender, instance, created, **kwargs):
    if created:
        welcome_new_user.delay(instance.id)
        logger.info(f"New message sent to {instance.username}")
