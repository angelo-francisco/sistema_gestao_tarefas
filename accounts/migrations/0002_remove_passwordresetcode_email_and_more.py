# Generated by Django 5.1.4 on 2024-12-20 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="passwordresetcode",
            name="email",
        ),
        migrations.AddField(
            model_name="passwordresetcode",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name="passwordresetcode",
            name="code",
            field=models.CharField(max_length=8, unique=True),
        ),
    ]