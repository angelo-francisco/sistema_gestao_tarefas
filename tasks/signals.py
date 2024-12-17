import logging

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Task

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Task, dispatch_uid="new_task_or_task_updated")
def new_task_or_task_updated(sender, instance, created, **kwargs):
    if created:
        return logger.info(
            msg=f"New task with ID {instance.id}, title: {instance.title}, creator: {instance.user.username} has been created"
        )
    return logger.info(
        msg=f"Task with ID {instance.id}, title: {instance.title}, creator: {instance.user.username} was modified."
    )


@receiver(post_delete, sender=Task, dispatch_uid="del_task_handler")
def del_task_handler(sender, instance, **kwargs):
    logger.info(
        f"Task with ID {instance.id}, title: {instance.title}, creator: {instance.user.username} was deleted"
    )
