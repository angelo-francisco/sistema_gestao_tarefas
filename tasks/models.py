from django.contrib.auth.models import User
from django.db import models
from uuid import uuid4


class Task(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="tasks"
    )
    title = models.CharField(max_length=200)
    desc = models.TextField(name="description", null=True, blank=True)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    notify_date = models.DateTimeField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    uid = models.UUIDField(default=uuid4, null=True, blank=True)
    
    class Meta:
        ordering = ("status", "-created_at")
