# Generated by Django 5.0.6 on 2024-07-05 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0012_content_approved"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField(default="Other", max_length=100),
        ),
    ]
