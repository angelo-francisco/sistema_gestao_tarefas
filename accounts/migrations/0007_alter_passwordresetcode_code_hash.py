# Generated by Django 5.1.4 on 2024-12-20 19:55

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0006_passwordresetcode_code_hash"),
    ]

    operations = [
        migrations.AlterField(
            model_name="passwordresetcode",
            name="code_hash",
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]