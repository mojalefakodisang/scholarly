# Generated by Django 5.0.6 on 2024-07-02 12:48

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0006_alter_content_created_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="content",
            name="title",
            field=models.CharField(default=None, max_length=255),
        ),
        migrations.AlterField(
            model_name="content",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
