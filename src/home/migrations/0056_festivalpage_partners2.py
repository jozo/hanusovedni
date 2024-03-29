# Generated by Django 3.0.4 on 2020-04-18 18:44

import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0055_auto_20200417_1150"),
    ]

    operations = [
        migrations.AddField(
            model_name="festivalpage",
            name="partners2",
            field=wagtail.fields.StreamField(
                [
                    ("heading", wagtail.blocks.CharBlock(classname="full title")),
                    (
                        "partner",
                        wagtail.blocks.StructBlock(
                            [
                                ("url", wagtail.blocks.URLBlock()),
                                ("logo", wagtail.images.blocks.ImageChooserBlock()),
                            ]
                        ),
                    ),
                ],
                blank=True,
                null=True,
            ),
        ),
    ]
