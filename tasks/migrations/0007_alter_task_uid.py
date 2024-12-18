# Generated by Django 5.1.4 on 2024-12-16 21:20

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0006_task_uid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="uid",
            field=models.UUIDField(blank=True, default=uuid.uuid4, null=True),
        ),
    ]