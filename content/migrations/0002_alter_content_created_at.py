# Generated by Django 5.0.6 on 2024-07-01 15:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="content",
            name="created_at",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 7, 1, 15, 59, 51, 831173, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]