# Generated by Django 3.1.7 on 2021-05-25 14:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0101_auto_20210525_1452"),
    ]

    operations = [
        migrations.AlterField(
            model_name="hostconnection",
            name="speaker",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="host_connections",
                to="home.speaker",
            ),
        ),
    ]
