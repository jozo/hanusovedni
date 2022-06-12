# Generated by Django 3.0.4 on 2020-04-24 01:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailcore", "0045_assign_unlock_grouppagepermission"),
        ("home", "0075_remove_event_speakers"),
    ]

    operations = [
        migrations.AddField(
            model_name="streampage",
            name="donate_button_action",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="stream_page_donate",
                to="wagtailcore.Page",
            ),
        ),
        migrations.AddField(
            model_name="streampage",
            name="donate_button_text_en",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="streampage",
            name="donate_button_text_sk",
            field=models.CharField(max_length=100, null=True),
        ),
    ]
