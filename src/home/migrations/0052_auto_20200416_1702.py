# Generated by Django 3.0.4 on 2020-04-16 17:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0051_auto_20200410_2047"),
    ]

    operations = [
        migrations.AlterField(
            model_name="location",
            name="title_en",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AlterField(
            model_name="location",
            name="title_sk",
            field=models.CharField(default="", max_length=255),
        ),
    ]
