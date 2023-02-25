# Generated by Django 3.1.1 on 2020-09-20 22:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0091_auto_20200920_2226"),
    ]

    operations = [
        migrations.AlterField(
            model_name="speakerconnection",
            name="speaker",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="speaker_connections",
                to="home.speaker",
            ),
        ),
    ]
