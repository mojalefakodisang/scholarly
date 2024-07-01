# Generated by Django 5.0.6 on 2024-07-01 15:58

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("contributor", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Content",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.TextField()),
                ("description", models.TextField()),
                (
                    "created_at",
                    models.DateTimeField(
                        default=datetime.datetime(2024, 7, 1, 15, 58, 10, 243094)
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contributor.contributor",
                    ),
                ),
            ],
        ),
    ]