# Generated by Django 5.0.6 on 2024-07-01 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("student", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="studentprofile",
            name="image",
            field=models.ImageField(default="default.jpg", upload_to="stud_pics"),
        ),
    ]
