# Generated by Django 5.1.4 on 2024-12-20 19:54

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0005_alter_passwordresetcode_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="passwordresetcode",
            name="code_hash",
            field=models.UUIDField(blank=True, default=uuid.uuid4, null=True),
        ),
    ]
