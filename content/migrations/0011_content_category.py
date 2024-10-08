# Generated by Django 5.0.6 on 2024-07-04 23:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0010_alter_category_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="content",
            name="category",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="contents",
                to="content.category",
            ),
        ),
    ]
