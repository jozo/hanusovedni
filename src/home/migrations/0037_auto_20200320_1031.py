# Generated by Django 3.0.4 on 2020-03-20 10:31

import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0036_auto_20200319_1629"),
    ]

    operations = [
        migrations.AlterField(
            model_name="festivalpage",
            name="headline",
            field=wagtail.core.fields.StreamField(
                [
                    (
                        "headliner",
                        wagtail.core.blocks.StructBlock(
                            [
                                ("name", wagtail.core.blocks.CharBlock()),
                                ("photo", wagtail.images.blocks.ImageChooserBlock()),
                                (
                                    "link",
                                    wagtail.core.blocks.PageChooserBlock(
                                        page_type=["home.Speaker"]
                                    ),
                                ),
                                ("description", wagtail.core.blocks.RichTextBlock()),
                            ]
                        ),
                    )
                ],
                blank=True,
                null=True,
            ),
        ),
    ]
