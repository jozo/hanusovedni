# Generated by Django 3.1.3 on 2020-11-26 17:56

import wagtail.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0096_auto_20201126_1752"),
    ]

    operations = [
        migrations.AddField(
            model_name="streampage",
            name="popup_donation_body_en",
            field=wagtail.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name="streampage",
            name="popup_donation_body_sk",
            field=wagtail.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name="streampage",
            name="popup_donation_button_en",
            field=models.CharField(default="", max_length=100),
        ),
        migrations.AddField(
            model_name="streampage",
            name="popup_donation_button_sk",
            field=models.CharField(default="", max_length=100),
        ),
    ]
