# Generated by Django 5.1.4 on 2024-12-20 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_remove_passwordresetcode_email_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="passwordresetcode",
            name="status",
            field=models.CharField(
                choices=[("A", "ACTIVE"), ("I", "INACTIVE")], default="A", max_length=8
            ),
        ),
    ]
