# Generated by Django 3.1.3 on 2020-11-20 09:26

import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0094_auto_20201119_2327"),
    ]

    operations = [
        migrations.AlterField(
            model_name="festivalpage",
            name="headline_en",
            field=wagtail.fields.StreamField(
                [
                    (
                        "headliner",
                        wagtail.blocks.StructBlock(
                            [
                                ("name", wagtail.blocks.CharBlock()),
                                ("photo", wagtail.images.blocks.ImageChooserBlock()),
                                ("link", wagtail.blocks.PageChooserBlock()),
                                ("description", wagtail.blocks.RichTextBlock()),
                            ]
                        ),
                    )
                ],
                blank=True,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="festivalpage",
            name="headline_sk",
            field=wagtail.fields.StreamField(
                [
                    (
                        "headliner",
                        wagtail.blocks.StructBlock(
                            [
                                ("name", wagtail.blocks.CharBlock()),
                                ("photo", wagtail.images.blocks.ImageChooserBlock()),
                                ("link", wagtail.blocks.PageChooserBlock()),
                                ("description", wagtail.blocks.RichTextBlock()),
                            ]
                        ),
                    )
                ],
                blank=True,
                null=True,
            ),
        ),
    ]
