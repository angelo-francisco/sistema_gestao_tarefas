# Generated by Django 5.1.4 on 2024-12-16 21:13

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0005_rename_desc_task_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="uid",
            field=models.UUIDField(
                auto_created=True,
                blank=True,
                default=uuid.uuid4,
                editable=False,
                null=True,
            ),
        ),
    ]
