# Generated by Django 5.0.6 on 2024-07-05 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("moderator", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="moderatorprofile",
            name="token",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
