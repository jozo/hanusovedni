# Generated by Django 2.2.9 on 2020-02-08 16:24

import modelcluster.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0009_auto_20200208_1523"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="speakers",
            field=modelcluster.fields.ParentalManyToManyField(
                blank=True,
                related_name="events",
                to="home.Speaker",
                verbose_name="rečník",
            ),
        ),
    ]
