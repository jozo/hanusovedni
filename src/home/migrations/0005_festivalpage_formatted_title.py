# Generated by Django 2.2.9 on 2020-02-08 09:44

import wagtail.core.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0004_auto_20200208_1000"),
    ]

    operations = [
        migrations.AddField(
            model_name="festivalpage",
            name="formatted_title",
            field=wagtail.core.fields.RichTextField(default=""),
        ),
    ]
