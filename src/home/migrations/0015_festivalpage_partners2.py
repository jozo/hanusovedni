# Generated by Django 2.2.9 on 2020-02-24 16:01

import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0014_remove_videoinvite_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="festivalpage",
            name="partners2",
            field=wagtail.fields.StreamField(
                [
                    ("heading", wagtail.blocks.CharBlock(classname="full title")),
                    ("url", wagtail.blocks.URLBlock()),
                    ("logo", wagtail.images.blocks.ImageChooserBlock()),
                ],
                blank=True,
            ),
        ),
    ]
