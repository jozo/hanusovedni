# Generated by Django 4.1.7 on 2023-02-26 15:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0115_festivalpage_video_invites_en_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="category",
            field=models.ForeignKey(
                default=12,
                on_delete=django.db.models.deletion.PROTECT,
                to="home.category",
            ),
            preserve_default=False,
        ),
    ]