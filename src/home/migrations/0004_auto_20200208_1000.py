# Generated by Django 2.2.9 on 2020-02-08 09:00

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "home",
            "0003_category_event_eventindexpage_festivalpage_headersettings_heroimage_location_partner_programindexpag",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="festivalpage",
            name="end_date",
            field=models.DateField(
                default=django.utils.timezone.now, verbose_name="koniec festivalu"
            ),
        ),
        migrations.AddField(
            model_name="festivalpage",
            name="logo",
            field=models.FileField(null=True, upload_to=""),
        ),
        migrations.AddField(
            model_name="festivalpage",
            name="place",
            field=models.CharField(
                default="Malá scéna STU", max_length=50, verbose_name="miesto"
            ),
        ),
        migrations.AddField(
            model_name="festivalpage",
            name="start_date",
            field=models.DateField(
                default=django.utils.timezone.now, verbose_name="začiatok festivalu"
            ),
        ),
    ]
