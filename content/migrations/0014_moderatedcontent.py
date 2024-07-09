# Generated by Django 5.0.6 on 2024-07-09 19:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0013_alter_category_name"),
        ("moderator", "0002_moderatorprofile_token"),
    ]

    operations = [
        migrations.CreateModel(
            name="ModeratedContent",
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
                (
                    "content",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="moderated_content",
                        to="content.content",
                    ),
                ),
                (
                    "moderator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="moderated_content",
                        to="moderator.moderator",
                    ),
                ),
            ],
        ),
    ]