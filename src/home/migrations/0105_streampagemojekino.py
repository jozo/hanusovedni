# Generated by Django 3.1.7 on 2021-06-17 07:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0104_crowdfundingcandlepage_feed_url"),
    ]

    operations = [
        migrations.CreateModel(
            name="StreamPageMojeKino",
            fields=[
                (
                    "streampage_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="home.streampage",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("home.streampage",),
        ),
    ]
