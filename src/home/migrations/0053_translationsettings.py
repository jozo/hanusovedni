# Generated by Django 3.0.4 on 2020-04-17 10:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailcore", "0045_assign_unlock_grouppagepermission"),
        ("home", "0052_auto_20200416_1702"),
    ]

    operations = [
        migrations.CreateModel(
            name="TranslationSettings",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("watch_video_button_sk", models.TextField(blank=True)),
                ("watch_video_button_en", models.TextField(blank=True)),
                ("buy_ticket_button_sk", models.TextField(blank=True)),
                ("buy_ticket_button_en", models.TextField(blank=True)),
                (
                    "site",
                    models.OneToOneField(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="wagtailcore.Site",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
