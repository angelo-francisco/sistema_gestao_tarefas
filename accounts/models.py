from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import uuid

class PasswordResetCode(models.Model):
    STATUS_CHOICES = (
        ('A', 'ACTIVE'),
        ('E', 'EXPIRED'),
        ('U', 'USED')
    )

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    code = models.CharField(max_length=8, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    status = models.CharField(max_length=8, default='A', choices=STATUS_CHOICES)
    code_hash = models.UUIDField(default=uuid.uuid4, unique=True)

    def is_expired(self):
        return timezone.now() > (self.created_at + timedelta(minutes=5))


