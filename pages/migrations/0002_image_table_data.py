# Generated by Django 5.0.2 on 2024-02-24 16:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="image",
            name="table_data",
            field=models.JSONField(default={}),
        ),
    ]
