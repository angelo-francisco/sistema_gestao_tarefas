from celery import shared_task
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from twilio.rest import Client


import logging

logger = logging.getLogger(__name__)

@shared_task
def welcome_new_user(userId):
    try:
        user = User.objects.get(id=userId)

        client = Client(settings.TWILIO_USERNAME, settings.TWILIO_PASSWORD)

        message = client.messages.create(
            body=f"Seja bem-vindo, {user.username}!",
            from_=settings.TWILIO_FROM,
            to=settings.TWILIO_TO,
        )

        return message.sid
    except Exception as e:
        logger.error(f"MSG Error, sending to user with ID {userId}, ERROR: {e}")


@shared_task
def email_user_reset_password(email, by, link=None, code=None):
    if by == "code":
        send_mail(
            subject="Verification Code",
            message=f"Your verification code {code}",
            from_email="ics20080729@gmail.com",
            recipient_list=[email],
        )
    elif by == "email":
        send_mail(
            subject="Reset Password Link",
            message=f"link {link}",
            from_email="ics20080729@gmail.com",
            recipient_list=[email],
        )
