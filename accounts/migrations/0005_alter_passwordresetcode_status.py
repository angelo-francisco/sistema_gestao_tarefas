# Generated by Django 5.1.4 on 2024-12-20 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_alter_passwordresetcode_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="passwordresetcode",
            name="status",
            field=models.CharField(
                choices=[("A", "ACTIVE"), ("E", "EXPIRED"), ("U", "USED")],
                default="A",
                max_length=8,
            ),
        ),
    ]
