from celery import shared_task
from django.core.mail import send_mail

from .models import Task

import logging

logger = logging.getLogger(__name__)


@shared_task
def email_notification(task_uid):
    try:
        task = Task.objects.get(uid=task_uid)

        send_mail(
            subject="Remember",
            message=f"Don't forgot your to do this: {task.title}",
            from_email="ics20080729@gmail.com",
            recipient_list=["ics20080729@gmail.com", ],
        )

        logger.info(f"Email sent to {task.user.username}, task uid: {task.uid}")
    except Task.DoesNotExist:
        logger.error(f"Task with UID {task_uid} not found.")
