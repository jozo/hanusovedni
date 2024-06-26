# Generated by Django 4.1.8 on 2023-05-30 07:54

import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0122_event_image"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="programindexpage2",
            options={"verbose_name": "Program index page - created for BHD 2023"},
        ),
        migrations.AlterField(
            model_name="festivalpage",
            name="headline_sk",
            field=wagtail.fields.StreamField(
                [
                    (
                        "heading",
                        wagtail.blocks.StructBlock(
                            [
                                ("sk", wagtail.blocks.CharBlock()),
                                ("en", wagtail.blocks.CharBlock()),
                            ]
                        ),
                    ),
                    (
                        "headliner",
                        wagtail.blocks.StructBlock(
                            [
                                ("name", wagtail.blocks.CharBlock(required=False)),
                                ("photo", wagtail.images.blocks.ImageChooserBlock()),
                                ("link", wagtail.blocks.PageChooserBlock()),
                                (
                                    "description",
                                    wagtail.blocks.RichTextBlock(required=False),
                                ),
                            ]
                        ),
                    ),
                ],
                blank=True,
                null=True,
                use_json_field=True,
            ),
        ),
    ]
